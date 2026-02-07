from typing import Any
import requests
URL =   "http://localhost:8000/api/simulate-io-operation"


def simulate_io_operation(delay: float | None = None, url =URL) -> dict[str, Any]:

    """Call the simulate I/O endpoint synchronously and return the JSON response."""

    params = {"delay": delay} if delay is not None else None

    response = requests.get(url, params=params, timeout=10.0)

    response.raise_for_status()

    return response.json()
