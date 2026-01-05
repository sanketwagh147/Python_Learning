"""Example: Sync FastAPI + SQLAlchemy pool dependency.

Run:
  pip install fastapi uvicorn sqlalchemy psycopg2-binary
  uvicorn postgres.db_pool.examples.fastapi_sync_app:app --reload
"""

from __future__ import annotations

from fastapi import Depends, FastAPI
from sqlalchemy import text
from sqlalchemy.orm import Session

from postgres.db_pool import (
    DatabaseConfig,
    SQLAlchemyDatabase,
    make_fastapi_lifespan,
    make_sync_session_dependency,
)

cfg = DatabaseConfig(
    url="postgresql+psycopg2://user:password@localhost:5432/postgres",
    pool_size=5,
    max_overflow=10,
    pool_pre_ping=True,
)

db = SQLAlchemyDatabase(cfg)

app = FastAPI(lifespan=make_fastapi_lifespan(db))
get_session = make_sync_session_dependency(db)


@app.get("/health/db")
def db_health(session: Session = Depends(get_session)):
    value = session.scalar(text("SELECT 1"))
    return {"ok": value == 1}
