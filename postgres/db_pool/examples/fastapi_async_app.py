"""Example: Async FastAPI + SQLAlchemy pool dependency.

Run:
  pip install fastapi uvicorn sqlalchemy asyncpg
  uvicorn postgres.db_pool.examples.fastapi_async_app:app --reload
"""

from __future__ import annotations

from fastapi import Depends, FastAPI
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from postgres.db_pool import (
    AsyncSQLAlchemyDatabase,
    DatabaseConfig,
    make_async_session_dependency,
    make_fastapi_lifespan,
)

cfg = DatabaseConfig(
    url="postgresql+asyncpg://user:password@localhost:5432/postgres",
    pool_size=5,
    max_overflow=10,
    pool_pre_ping=True,
)

db = AsyncSQLAlchemyDatabase(cfg)

app = FastAPI(lifespan=make_fastapi_lifespan(db))
get_session = make_async_session_dependency(db)


@app.get("/health/db")
async def db_health(session: AsyncSession = Depends(get_session)):
    value = await session.scalar(text("SELECT 1"))
    return {"ok": value == 1}
