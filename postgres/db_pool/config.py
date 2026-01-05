from __future__ import annotations

import os
from dataclasses import dataclass, field
from typing import Any, Mapping


@dataclass(frozen=True, slots=True)
class DatabaseConfig:
    """Database/engine configuration.

    Works with any database supported by SQLAlchemy by supplying the appropriate
    SQLAlchemy URL (sync or async driver).

    Notes:
    - For SQLite or other DBs that don't support/need pooling, set pool fields to None.
    - Extra driver-specific args can be passed via `connect_args`.
    - Any SQLAlchemy engine option can be passed via `engine_kwargs`.
    """

    url: str

    echo: bool = False

    # Pooling (set to None to omit the option).
    pool_size: int | None = 5
    max_overflow: int | None = 10
    pool_timeout: int | None = 30
    pool_recycle: int | None = 1800
    pool_pre_ping: bool | None = True

    connect_args: Mapping[str, Any] = field(default_factory=dict)
    engine_kwargs: Mapping[str, Any] = field(default_factory=dict)

    @staticmethod
    def _parse_bool(value: str | None, *, default: bool) -> bool:
        if value is None:
            return default
        return value.strip().lower() in {"1", "true", "yes", "y", "on"}

    @staticmethod
    def _parse_int_or_none(value: str | None) -> int | None:
        if value is None:
            return None
        value = value.strip()
        if value == "":
            return None
        return int(value)

    @classmethod
    def from_env(cls, *, prefix: str = "DB_") -> "DatabaseConfig":
        """Create a config from environment variables.

        Supported keys (with default prefix `DB_`):
        - `DB_URL`
        - `DB_ECHO`
        - `DB_POOL_SIZE`, `DB_MAX_OVERFLOW`, `DB_POOL_TIMEOUT`, `DB_POOL_RECYCLE`
        - `DB_POOL_PRE_PING`
        """

        url = os.environ.get(f"{prefix}URL")
        if not url:
            raise ValueError(f"Missing required env var: {prefix}URL")

        return cls(
            url=url,
            echo=cls._parse_bool(os.environ.get(f"{prefix}ECHO"), default=False),
            pool_size=cls._parse_int_or_none(os.environ.get(f"{prefix}POOL_SIZE")),
            max_overflow=cls._parse_int_or_none(os.environ.get(f"{prefix}MAX_OVERFLOW")),
            pool_timeout=cls._parse_int_or_none(os.environ.get(f"{prefix}POOL_TIMEOUT")),
            pool_recycle=cls._parse_int_or_none(os.environ.get(f"{prefix}POOL_RECYCLE")),
            pool_pre_ping=cls._parse_bool(
                os.environ.get(f"{prefix}POOL_PRE_PING"), default=True
            ),
        )

    def to_engine_kwargs(self) -> dict[str, Any]:
        """Convert config into kwargs for `create_engine` / `create_async_engine`."""
        kwargs: dict[str, Any] = {
            "url": self.url,
            "echo": self.echo,
            "connect_args": dict(self.connect_args),
        }

        if self.pool_size is not None:
            kwargs["pool_size"] = self.pool_size
        if self.max_overflow is not None:
            kwargs["max_overflow"] = self.max_overflow
        if self.pool_timeout is not None:
            kwargs["pool_timeout"] = self.pool_timeout
        if self.pool_recycle is not None:
            kwargs["pool_recycle"] = self.pool_recycle
        if self.pool_pre_ping is not None:
            kwargs["pool_pre_ping"] = self.pool_pre_ping

        # Allow caller to override anything.
        kwargs.update(dict(self.engine_kwargs))
        return kwargs
