"""
Rate Limiting function
"""

import time
import threading
import functools
from collections import deque


def rate_limiter(max_call_count: int, period: float = 1.0):

    def decorator(fn):

        timestamps = deque()
        lock = threading.Lock()

        @functools.wraps(fn)
        def wrapper(*args, **kwargs):
            with lock:
                now = time.monotonic()

                while timestamps and timestamps[0] <= now - period:
                    timestamps.popleft()

                if len(timestamps) >= max_call_count:
                    sleep_time = period - (now - timestamps[0])

                    if sleep_time > 0:
                        print(
                            f"Rate_limit Throttling {fn.__name__} for {sleep_time:.3f}s"
                        )
                        time.sleep(sleep_time)

                    now = time.monotonic()
                    while timestamps and timestamps[0] <= now - period:
                        timestamps.popleft()

                timestamps.append(time.monotonic())
            return fn(*args, **kwargs)

        return wrapper

    return decorator


if __name__ == "__main__":

    @rate_limiter(max_call_count=3, period=2.0)
    def fetch_data(url: str) -> str:
        """Simulate an API call."""
        return f"Response from {url}"

    fetch_data("1")
    fetch_data("1")
    fetch_data("1")
    fetch_data("1")
    fetch_data("1")
    fetch_data("1")
    print(fetch_data.__name__)


def decorator(fn):

    @functools.wraps(fn)
    def wrapper(): ...

    return wrapper
