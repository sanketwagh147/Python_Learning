import asyncio
import threading
from typing import Any, AsyncGenerator
import requests
from contextlib import asynccontextmanager
URL =   "http://localhost:8000/api/simulate-io-operation"


def call_simulate_io_operation_sync(delay: float | None = None, url =URL) -> dict[str, Any]:

    """Call the simulate I/O endpoint synchronously and return the JSON response."""

    print(f"Calling simulate_io_operation with {delay=}")
    params = {"delay": delay} if delay is not None else None

    response = requests.get(url, params=params, timeout=10.0)

    response.raise_for_status()

    return response.json()

class ServiceOperationError(Exception):
    pass

@asynccontextmanager
async def get_service_data(url: str, delay: float = 2.0) -> AsyncGenerator[dict[str, Any], None]:
    """
    Handles the lifecycle of a remote data fetch operation.
    Wraps a blocking call in a thread-safe async context.
    """
    print(f"Starting request to {url}")
    
    try:
        data = await asyncio.to_thread(call_simulate_io_operation_sync, delay, url)
        
        yield data
        
    except requests.RequestException as e:
        print(f"Network error occurred: {e}")
        raise ServiceOperationError(f"Failed to fetch data: {e}")
    finally:
        # 4. Teardown Phase (Always runs)
        print("Cleaning up resources or closing connection...")

async def main():
    target_url = "http://localhost:8000/api/simulate-io-operation"
    
    try:
        async with get_service_data(target_url) as data:
            # Process the data while the context is active
            print(f"Received: {data}")
            # Logic here is protected by the context manager's error handling
    except ServiceOperationError:
        print("Gracefully handled service failure.")

if __name__ == "__main__":
    asyncio.run(main())