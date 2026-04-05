"""Database session management with sync and async support."""

import os
import re
from contextlib import contextmanager, asynccontextmanager
from typing import Generator, AsyncGenerator

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import Session, sessionmaker

load_dotenv()

# =============================================================================
# CONFIGURATION
# =============================================================================

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise EnvironmentError("DATABASE_URL is required. Set it in .env file.")

# Reliably replace any PostgreSQL driver with asyncpg
ASYNC_DATABASE_URL = re.sub(r'^postgresql(\+\w+)?://', 'postgresql+asyncpg://', DATABASE_URL)

_POOL_SIZE = int(os.getenv("DB_POOL_SIZE", "5"))
_MAX_OVERFLOW = int(os.getenv("DB_MAX_OVERFLOW", "10"))
_POOL_PRE_PING = os.getenv("DB_POOL_PRE_PING", "true").lower() == "true"
_ECHO = os.getenv("DB_ECHO", "false").lower() == "true"
_ASYNC_POOL_SIZE = int(os.getenv("DB_ASYNC_POOL_SIZE", "10"))
_ASYNC_MAX_OVERFLOW = int(os.getenv("DB_ASYNC_MAX_OVERFLOW", "20"))


# =============================================================================
# SYNC ENGINE & SESSION
# =============================================================================

engine = create_engine(
    DATABASE_URL,
    pool_size=_POOL_SIZE,
    max_overflow=_MAX_OVERFLOW,
    pool_pre_ping=_POOL_PRE_PING,
    echo=_ECHO,
)

SessionFactory = sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)


def get_session() -> Session:
    """Get a new sync session. Caller must close it."""
    return SessionFactory()


@contextmanager
def session_scope() -> Generator[Session, None, None]:
    """Transactional scope: auto-commit on success, rollback on error."""
    session = SessionFactory()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


# =============================================================================
# ASYNC ENGINE & SESSION
# =============================================================================

async_engine = create_async_engine(
    ASYNC_DATABASE_URL,
    pool_size=_ASYNC_POOL_SIZE,
    max_overflow=_ASYNC_MAX_OVERFLOW,
    pool_pre_ping=_POOL_PRE_PING,
    echo=_ECHO,
)

AsyncSessionFactory = async_sessionmaker(
    bind=async_engine, class_=AsyncSession, autoflush=False, expire_on_commit=False
)


async def get_async_session() -> AsyncSession:
    """Get a new async session. Caller must close it."""
    return AsyncSessionFactory()


@asynccontextmanager
async def async_session_scope() -> AsyncGenerator[AsyncSession, None]:
    """Async transactional scope: auto-commit on success, rollback on error."""
    session = AsyncSessionFactory()
    try:
        yield session
        await session.commit()
    except Exception:
        await session.rollback()
        raise
    finally:
        await session.close()


# =============================================================================
# DATABASE MANAGER (for custom configurations)
# =============================================================================

class DatabaseManager:
    """Database manager for custom engine configurations."""

    def __init__(self, sync_url: str | None = None, async_url: str | None = None):
        self.sync_url = sync_url or DATABASE_URL
        self.async_url = async_url or ASYNC_DATABASE_URL

        self.engine = create_engine(self.sync_url, pool_pre_ping=True)
        self.session_factory = sessionmaker(bind=self.engine, autoflush=False)

        self.async_engine = create_async_engine(self.async_url, pool_pre_ping=True)
        self.async_session_factory = async_sessionmaker(
            bind=self.async_engine, class_=AsyncSession, autoflush=False
        )

    @contextmanager
    def session_scope(self) -> Generator[Session, None, None]:
        session = self.session_factory()
        try:
            yield session
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()

    @asynccontextmanager
    async def async_session_scope(self) -> AsyncGenerator[AsyncSession, None]:
        session = self.async_session_factory()
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()

    def dispose(self) -> None:
        self.engine.dispose()

    async def async_dispose(self) -> None:
        await self.async_engine.dispose()
