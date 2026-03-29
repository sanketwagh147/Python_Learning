"""
Inventory Repository — Dependency Inversion + Repository Pattern
================================================================
Abstracts inventory data access so InventoryHandler depends on an
interface, not a concrete database. This follows:

  • Dependency Inversion Principle (DIP)
  • Repository Pattern (same pattern used in multi threading/fastapi/repository/)

Two implementations:
  1. DBInventoryRepository  — reads from temp.inventory via an injected Session
  2. InMemoryInventoryRepository — in-memory dict for testing / offline use

Key DIP point:
  DBInventoryRepository does NOT create its own engine or session.
  The Session is injected from outside — the caller (FastAPI dependency,
  script, CLI) decides how to create & manage the DB connection.
"""

from __future__ import annotations
from abc import ABC, abstractmethod

from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session, sessionmaker


# ── Abstraction ─────────────────────────────────────────────

class InventoryRepository(ABC):
    """Interface that InventoryHandler depends on (DIP)."""

    @abstractmethod
    def get_stock(self, item_name: str) -> int:
        """Return available quantity for the given item, 0 if not found."""


# ── Concrete: PostgreSQL via injected SQLAlchemy Session ────

class DBInventoryRepository(InventoryRepository):
    """Fetches inventory from temp.inventory.

    The Session is *injected* — this class has no idea where the
    connection comes from, which DB engine is used, or how the
    session lifecycle is managed.  That's the caller's job.

    In FastAPI:  session comes from Depends(get_db)
    In a script: session comes from get_session() helper below
    In tests:    session can be an in-memory SQLite session
    """

    def __init__(self, session: Session):
        self._session = session

    def get_stock(self, item_name: str) -> int:
        row = self._session.execute(
            text("SELECT quantity FROM temp.inventory WHERE item_name = :name"),
            {"name": item_name},
        ).fetchone()
        return row[0] if row else 0


# ── Concrete: In-Memory (for tests / no DB available) ──────

class InMemoryInventoryRepository(InventoryRepository):
    """Simple dict-backed repository — no database needed."""

    def __init__(self, stock: dict[str, int] | None = None):
        self._stock = stock or {"laptop": 5, "keyboard": 50, "monitor": 0}

    def get_stock(self, item_name: str) -> int:
        return self._stock.get(item_name, 0)


# ── Session helper (for standalone scripts / CLI) ───────────

DATABASE_URL = "postgresql://sanketwagh@localhost/local_db"

_engine = create_engine(DATABASE_URL)
_SessionFactory = sessionmaker(bind=_engine)


def get_session() -> Session:
    """Create a new Session for standalone (non-FastAPI) usage.

    Caller is responsible for closing it, e.g.:
        with get_session() as session:
            repo = DBInventoryRepository(session)
    """
    return _SessionFactory()


# ── How this would look in FastAPI ──────────────────────────
#
#   # database.py
#   engine = create_engine(settings.DATABASE_URL)
#   SessionLocal = sessionmaker(bind=engine)
#
#   def get_db():
#       db = SessionLocal()
#       try:
#           yield db
#       finally:
#           db.close()
#
#   # routes/orders.py
#   @router.post("/orders")
#   def create_order(order: OrderSchema, db: Session = Depends(get_db)):
#       repo = DBInventoryRepository(db)        # ← session injected
#       pipeline = build_order_pipeline(repo)
#       return pipeline.handle(order)
#
# The chain, the repository, and the DB session are all
# composed at the edge (the route handler). Nothing hidden.
