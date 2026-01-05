from __future__ import annotations

from contextlib import asynccontextmanager
from typing import Any, AsyncIterator, Callable, Iterator, Protocol, TypeVar

from .sqlalchemy_pool import AsyncSQLAlchemyDatabase, SQLAlchemyDatabase


class _SupportsDispose(Protocol):
    async def dispose(self) -> Any: ...


TDb = TypeVar("TDb", SQLAlchemyDatabase, AsyncSQLAlchemyDatabase)


def make_sync_session_dependency(
    db: SQLAlchemyDatabase,
) -> Callable[[], Iterator[Any]]:
    """Create a FastAPI dependency that yields a sync Session."""

    def _dep() -> Iterator[Any]:
        with db.session() as session:
            yield session

    return _dep


def make_async_session_dependency(
    db: AsyncSQLAlchemyDatabase,
) -> Callable[[], AsyncIterator[Any]]:
    """Create a FastAPI dependency that yields an AsyncSession."""

    async def _dep() -> AsyncIterator[Any]:
        async with db.session() as session:
            yield session

    return _dep


def make_fastapi_lifespan(db: TDb):
    """Create a FastAPI lifespan handler for DB engine lifecycle.

    FastAPI will call this on startup/shutdown.

    - Sync DB: engine is lazily created on first use; shutdown calls `dispose()`.
    - Async DB: engine is lazily created on first use; shutdown calls `await dispose()`.
    """

    @asynccontextmanager
    async def lifespan(app):  # type: ignore[no-untyped-def]
        # Ensure engine is created early if you prefer fail-fast:
        _ = db.engine
        try:
            yield
        finally:
            if isinstance(db, AsyncSQLAlchemyDatabase):
                await db.dispose()
            else:
                db.dispose()

    return lifespan
