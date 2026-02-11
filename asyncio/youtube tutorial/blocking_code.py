import asyncio
from typing import Any, cast

import httpx
import requests

URL = "http://localhost:8000/api/simulate-io-operation"


async def simulate_io_operation(delay: float | None = None, url: str = URL) -> dict[str, Any]:
    """Call the simulate I/O endpoint asynchronously and return the JSON response."""

    params = {"delay": delay} if delay is not None else None
    print(f"[ASYNC] Calling simulate_io_operation with delay={delay}")

    async with httpx.AsyncClient(timeout=10.0) as client:
        response = await client.get(url, params=params)
        response.raise_for_status()
        return cast(dict[str, Any], response.json())


def simulate_io_operation_sync(delay: float | None = None, url: str = URL) -> dict[str, Any]:
    """Call the simulate I/O endpoint synchronously and return the JSON response."""

    params = {"delay": delay} if delay is not None else None
    print(f"[SYNC] Calling simulate_io_operation_sync with delay={delay}")

    response = requests.get(url, params=params, timeout=10.0)
    response.raise_for_status()
    return cast(dict[str, Any], response.json())

if __name__ == "__main__":
    asyncio.run(simulate_io_operation())