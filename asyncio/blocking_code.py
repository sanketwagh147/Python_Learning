from typing import Any, cast

import httpx

URL = "http://localhost:8000/api/simulate-io-operation"


async def simulate_io_operation(delay: float | None = None, url: str = URL) -> dict[str, Any]:
    """Call the simulate I/O endpoint asynchronously and return the JSON response."""

    params = {"delay": delay} if delay is not None else None

    async with httpx.AsyncClient(timeout=10.0) as client:
        response = await client.get(url, params=params)
        response.raise_for_status()
        return cast(dict[str, Any], response.json())
