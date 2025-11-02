from typing import Optional, Dict, Any
from pydantic import BaseModel, Field
import httpx
from fastapi import FastAPI


class TimeoutConfig(BaseModel):
    """Timeout configuration for HTTP client."""

    connect: float = Field(default=5.0, description="Connection timeout in seconds")
    read: float = Field(default=30.0, description="Read timeout in seconds")
    write: float = Field(default=30.0, description="Write timeout in seconds")
    pool: float = Field(default=30.0, description="Pool timeout in seconds")

    def to_httpx_timeout(self) -> httpx.Timeout:
        """Convert to httpx.Timeout instance."""
        return httpx.Timeout(**self.model_dump())


class PoolConfig(BaseModel):
    """Connection pool configuration."""

    max_connections: int = Field(
        default=100, description="Maximum number of connections"
    )
    max_keepalive: int = Field(
        default=20, description="Maximum number of idle connections"
    )
    keepalive_expiry: float = Field(
        default=30.0, description="Time in seconds to keep idle connections"
    )


class RetryConfig(BaseModel):
    """Retry configuration."""

    max_retries: int = Field(default=3, description="Maximum number of retry attempts")
    backoff_factor: float = Field(
        default=0.1,
        description="Each retry will wait {factor} * (2 ** {retry}) seconds",
    )


class ClientConfig(BaseModel):
    """Complete HTTP client configuration."""

    timeout: TimeoutConfig = Field(default_factory=TimeoutConfig)
    pool: PoolConfig = Field(default_factory=PoolConfig)
    retry: RetryConfig = Field(default_factory=RetryConfig)
    http2: bool = Field(default=True, description="Enable HTTP/2 support")
    verify_ssl: bool = Field(default=True, description="Verify SSL certificates")
    follow_redirects: bool = Field(
        default=True, description="Automatically follow redirects"
    )


class HttpxRestClientPool:
    """A singleton HTTP client pool manager for FastAPI applications.

    Manages a shared httpx.AsyncClient instance with connection pooling
    and lifecycle management integrated with FastAPI.
    """

    _client: Optional[httpx.AsyncClient] = None
    _config: ClientConfig = ClientConfig()

    @classmethod
    def configure(cls, config: Optional[ClientConfig] = None) -> None:
        """Configure the client pool with custom settings."""
        if config is not None:
            cls._config = config

    @classmethod
    def get_client(cls) -> httpx.AsyncClient:
        """Get the shared HTTP client instance"""
        if cls._client is None:
            transport = httpx.AsyncHTTPTransport(
                # Retry configuration
                retries=cls._config.retry.max_retries,
                retry_backoff_factor=cls._config.retry.backoff_factor,
                # Connection pooling
                max_connections=cls._config.pool.max_connections,
                max_keepalive_connections=cls._config.pool.max_keepalive,
                keepalive_expiry=cls._config.pool.keepalive_expiry,
                # HTTP/2 support
                http2=cls._config.http2,
            )

            cls._client = httpx.AsyncClient(
                transport=transport,
                timeout=cls._config.timeout.to_httpx_timeout(),
                verify=cls._config.verify_ssl,
                follow_redirects=cls._config.follow_redirects,
            )
        return cls._client

    @classmethod
    async def dispose(cls) -> None:
        """Release all resources held by the HTTP client."""
        if cls._client is not None:
            await cls._client.aclose()
            cls._client = None


def setup_http_pool(app: FastAPI, config: Optional[ClientConfig] = None) -> None:
    """Configure HTTP pool lifecycle hooks for a FastAPI application.

    Args:
        app: FastAPI application instance
        config: Optional custom client configuration
    """
    # Configure the client pool with custom settings if provided
    if config is not None:
        HttpxRestClientPool.configure(config)

    @app.on_event("startup")
    async def initialize_http_pool():
        # Initialize the client pool on startup
        HttpxRestClientPool.get_client()

    @app.on_event("shutdown")
    async def cleanup_http_pool():
        # Ensure all connections are properly closed
        await HttpxRestClientPool.dispose()


async def fetch_url(url: str, method: str = "GET", **kwargs: Any) -> Dict[str, Any]:
    """Make an HTTP request using the shared connection pool.

    The client is configured with automatic retries using exponential backoff.
    Retries are handled by httpx's transport layer automatically.

    Args:
        url: The URL to request
        method: HTTP method to use (default: GET)
        **kwargs: Additional arguments to pass to httpx request

    Returns:
        dict: Response details including status code, headers, and URL

    Examples:
        >>> # Basic GET request
        >>> response = await fetch_url("https://api.example.com/data")

        >>> # POST request with custom headers
        >>> response = await fetch_url(
        ...     "https://api.example.com/data",
        ...     method="POST",
        ...     json={"key": "value"},
        ...     headers={"Authorization": "Bearer token"}
        ... )
    """
    client = HttpxRestClientPool.get_client()
    async with client.stream(method, url, **kwargs) as response:
        return {
            "status": response.status_code,
            "headers": dict(response.headers),
            "url": str(response.url),
        }
