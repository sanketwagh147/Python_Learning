import asyncio
from typing import Any, cast

import httpx
import requests

URL = "http://localhost:8000/api/simulate-io-operation"


async def simulate_io_operation(name:str,delay: float | None = None, url: str = URL) -> dict[str, Any]:
    """Call the simulate I/O endpoint asynchronously and return the JSON response."""

    params = {"delay": delay} if delay is not None else None
    print(f"[ASYNC] Calling simulate_io_operation {name} with delay={delay}")

    async with httpx.AsyncClient(timeout=10.0) as client:
        response = await client.get(url+f"/{name}", params=params)
        response.raise_for_status()
        return cast(dict[str, Any], response.json())


def simulate_io_operation_sync(name:str, delay: float | None = None, url: str = URL) -> dict[str, Any]:
    """Call the simulate I/O endpoint synchronously and return the JSON response."""

    params = {"delay": delay} if delay is not None else None
    print(f"[SYNC] Calling simulate_io_operation_sync {name} with delay={delay}")

    response = requests.get(url+f"/{name}", params=params, timeout=10.0)
    response.raise_for_status()
    return cast(dict[str, Any], response.json())


async def simulate_http_error(error_code: int, url: str = "http://localhost:8000/api/simulate_http_error") -> dict[str, Any]:
    """Call the simulate HTTP error endpoint asynchronously."""

    print(f"[ASYNC] Calling simulate_http_error with error_code={error_code}")

    async with httpx.AsyncClient(timeout=10.0) as client:
        response = await client.get(f"{url}/{error_code}")
        response.raise_for_status()
        return cast(dict[str, Any], response.json())


def simulate_http_error_sync(error_code: int, url: str = "http://localhost:8000/api/simulate_http_error") -> dict[str, Any]:
    """Call the simulate HTTP error endpoint synchronously."""

    print(f"[SYNC] Calling simulate_http_error_sync with error_code={error_code}")

    response = requests.get(f"{url}/{error_code}", timeout=10.0)
    response.raise_for_status()
    return cast(dict[str, Any], response.json())


def simulate_cpu_bound_task(name: str, iterations: int) -> int:
    """Simulate a CPU-bound operation by performing a heavy calculation."""
    print(f"[CPU] Starting cpu_bound_task {name} with {iterations} iterations")

    result = 0
    # A simple CPU-intensive loop
    for i in range(iterations*50000000):
        result += i * i

    print(f"[CPU] Finished cpu_bound_task {name}")
    return result


if __name__ == "__main__":
    asyncio.run(simulate_io_operation("test"))