from __future__ import annotations

from contextlib import asynccontextmanager, contextmanager
from typing import Any, AsyncIterator, Callable, Iterator, Protocol, cast

from .config import DatabaseConfig


def _require_sqlalchemy() -> None:
    try:
        import sqlalchemy  # noqa: F401
    except ImportError as exc:  # pragma: no cover
        raise ImportError(
            "SQLAlchemy is required. Install with: pip install sqlalchemy"
        ) from exc


class _SyncSessionFactory(Protocol):
    def __call__(self) -> Any: ...


class _AsyncSessionFactory(Protocol):
    def __call__(self) -> Any: ...


class SQLAlchemyDatabase:
    """Sync SQLAlchemy engine + session factory.

    Instance-based (no global state) so it composes cleanly with FastAPI DI.
    """

    def __init__(
        self,
        config: DatabaseConfig,
        *,
        engine_factory: Callable[[dict[str, Any]], Any] | None = None,
    ) -> None:
        _require_sqlalchemy()
        self._config = config

        if engine_factory is None:
            from sqlalchemy import create_engine

            engine_factory = lambda kwargs: create_engine(**kwargs)

        self._engine_factory = engine_factory
        self._engine: Any | None = None
        self._sessionmaker: _SyncSessionFactory | None = None

    @property
    def config(self) -> DatabaseConfig:
        return self._config

    @property
    def engine(self):
        if self._engine is None:
            kwargs = self._config.to_engine_kwargs()
            self._engine = self._engine_factory(kwargs)
        return self._engine

    @property
    def sessionmaker(self) -> _SyncSessionFactory:
        if self._sessionmaker is None:
            from sqlalchemy.orm import Session, sessionmaker

            self._sessionmaker = sessionmaker(
                bind=self.engine,
                autoflush=False,
                autocommit=False,
                expire_on_commit=False,
                class_=Session,
            )
        assert self._sessionmaker is not None
        return cast(_SyncSessionFactory, self._sessionmaker)

    def dispose(self) -> None:
        if self._engine is not None:
            self._engine.dispose()
        self._engine = None
        self._sessionmaker = None

    @contextmanager
    def session(self) -> Iterator[Any]:
        """Provide a per-use Session; roll back on exceptions."""
        session = self.sessionmaker()
        try:
            yield session
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()


class AsyncSQLAlchemyDatabase:
    """Async SQLAlchemy engine + session factory."""

    def __init__(
        self,
        config: DatabaseConfig,
        *,
        engine_factory: Callable[[dict[str, Any]], Any] | None = None,
    ) -> None:
        _require_sqlalchemy()
        self._config = config

        if engine_factory is None:
            from sqlalchemy.ext.asyncio import create_async_engine

            engine_factory = lambda kwargs: create_async_engine(**kwargs)

        self._engine_factory = engine_factory
        self._engine: Any | None = None
        self._sessionmaker: _AsyncSessionFactory | None = None

    @property
    def config(self) -> DatabaseConfig:
        return self._config

    @property
    def engine(self):
        if self._engine is None:
            kwargs = self._config.to_engine_kwargs()
            self._engine = self._engine_factory(kwargs)
        return self._engine

    @property
    def sessionmaker(self) -> _AsyncSessionFactory:
        if self._sessionmaker is None:
            from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

            self._sessionmaker = async_sessionmaker(
                bind=self.engine,
                autoflush=False,
                expire_on_commit=False,
                class_=AsyncSession,
            )
        assert self._sessionmaker is not None
        return cast(_AsyncSessionFactory, self._sessionmaker)

    async def dispose(self) -> None:
        if self._engine is not None:
            await self._engine.dispose()
        self._engine = None
        self._sessionmaker = None

    @asynccontextmanager
    async def session(self) -> AsyncIterator[Any]:
        """Provide a per-use AsyncSession; roll back on exceptions."""
        async with self.sessionmaker() as session:
            try:
                yield session
            except Exception:
                await session.rollback()
                raise
