"""Reusable DB pool + session dependencies for FastAPI.

This module is intentionally instance-based (no globals) so it can be reused
across apps and tests and follows SOLID principles.

Primary entry points:
- `DatabaseConfig`
- `SQLAlchemyDatabase` (sync)
- `AsyncSQLAlchemyDatabase` (async)
- `make_fastapi_lifespan`
- `make_sync_session_dependency` / `make_async_session_dependency`
"""

from .config import DatabaseConfig
from .sqlalchemy_pool import AsyncSQLAlchemyDatabase, SQLAlchemyDatabase
from .fastapi import (
    make_async_session_dependency,
    make_fastapi_lifespan,
    make_sync_session_dependency,
)

__all__ = [
    "DatabaseConfig",
    "SQLAlchemyDatabase",
    "AsyncSQLAlchemyDatabase",
    "make_fastapi_lifespan",
    "make_sync_session_dependency",
    "make_async_session_dependency",
]
