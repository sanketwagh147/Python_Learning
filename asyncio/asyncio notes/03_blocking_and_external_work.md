# Running Blocking / External Work with asyncio

Covers:
- `asyncio.to_thread()`
- `loop.run_in_executor()` with `ThreadPoolExecutor`
- `loop.run_in_executor()` with `ProcessPoolExecutor`
- When to use threads vs processes

---

## 1. The Problem: Blocking Code Freezes the Event Loop

```python
import asyncio
import time


def blocking_io() -> str:
    """Simulates a blocking I/O call (e.g., requests.get, file read)."""
    time.sleep(2.0)  # blocks the entire event loop!
    return "blocking result"


async def async_task(name: str) -> None:
    print(f"[{name}] started")
    await asyncio.sleep(1.0)
    print(f"[{name}] finished")


async def main() -> None:
    start = time.perf_counter()

    # BAD: blocking_io() freezes the event loop
    # async_task won't run concurrently!
    result = blocking_io()
    await async_task("A")

    elapsed = time.perf_counter() - start
    print(f"Total: {elapsed:.2f}s (should be ~2s but is ~3s because of blocking)")


if __name__ == "__main__":
    asyncio.run(main())
```

---

## 2. Thread Pool: asyncio.to_thread() (Python 3.9+)

`asyncio.to_thread(func, *args, **kwargs)` runs a sync function in a
separate thread, returning an awaitable. The event loop stays unblocked.

### 2.1 Basic example

```python
import asyncio
import time
import threading


def blocking_io(delay: float) -> str:
    thread = threading.current_thread().name
    print(f"  [blocking_io] sleeping {delay}s in thread {thread}")
    time.sleep(delay)
    return f"result after {delay}s"


async def async_task(name: str) -> None:
    print(f"  [async] {name} started")
    await asyncio.sleep(1.0)
    print(f"  [async] {name} finished")


async def main() -> None:
    start = time.perf_counter()

    # Run blocking I/O in a thread AND async task concurrently
    results = await asyncio.gather(
        asyncio.to_thread(blocking_io, 2.0),
        async_task("A"),
    )

    elapsed = time.perf_counter() - start
    print(f"Total: {elapsed:.2f}s (should be ~2s, not 3s)")
    print(f"Blocking result: {results[0]}")


if __name__ == "__main__":
    asyncio.run(main())
```

### 2.2 Multiple blocking calls concurrently

```python
import asyncio
import time


def sync_api_call(endpoint: str, delay: float) -> dict:
    """Simulates a blocking HTTP call."""
    time.sleep(delay)
    return {"endpoint": endpoint, "delay": delay, "status": "ok"}


async def main() -> None:
    start = time.perf_counter()

    # All 3 blocking calls run in separate threads concurrently
    results = await asyncio.gather(
        asyncio.to_thread(sync_api_call, "/users", 1.0),
        asyncio.to_thread(sync_api_call, "/posts", 1.5),
        asyncio.to_thread(sync_api_call, "/comments", 2.0),
    )

    elapsed = time.perf_counter() - start
    for r in results:
        print(f"  {r}")
    print(f"Total: {elapsed:.2f}s (should be ~2s, not 4.5s)")


if __name__ == "__main__":
    asyncio.run(main())
```

---

## 3. Custom ThreadPoolExecutor

`asyncio.to_thread` uses the default executor. For more control (e.g.,
limiting thread count), use `loop.run_in_executor()` with a custom pool.

```python
import asyncio
import time
from concurrent.futures import ThreadPoolExecutor


def blocking_download(url: str) -> str:
    time.sleep(1.0)
    return f"downloaded {url}"


async def main() -> None:
    loop = asyncio.get_running_loop()
    start = time.perf_counter()

    # Custom pool with max 3 threads
    with ThreadPoolExecutor(max_workers=3, thread_name_prefix="download") as pool:
        urls = [f"http://example.com/file{i}" for i in range(6)]

        # Schedule all downloads
        futures = [loop.run_in_executor(pool, blocking_download, url) for url in urls]

        # Print results as they complete
        for coro in asyncio.as_completed(futures):
            result = await coro
            print(f"  {result}")

    elapsed = time.perf_counter() - start
    print(f"Total: {elapsed:.2f}s (6 downloads, 3 at a time = ~2s)")


if __name__ == "__main__":
    asyncio.run(main())
```

---

## 4. Process Pool for CPU-Bound Work

Threads are limited by the GIL for CPU work. Use `ProcessPoolExecutor` for
true parallelism on CPU-bound tasks.

### 4.1 CPU-bound function

```python
# You can add this to blocking_code.py

def count_primes(n: int) -> int:
    """Count primes up to n (CPU-heavy)."""
    count = 0
    for num in range(2, n + 1):
        if all(num % i != 0 for i in range(2, int(num ** 0.5) + 1)):
            count += 1
    return count
```

### 4.2 Running in a process pool

```python
import asyncio
import time
from concurrent.futures import ProcessPoolExecutor


def count_primes(n: int) -> int:
    count = 0
    for num in range(2, n + 1):
        if all(num % i != 0 for i in range(2, int(num ** 0.5) + 1)):
            count += 1
    return count


async def main() -> None:
    loop = asyncio.get_running_loop()
    numbers = [50_000, 60_000, 70_000, 80_000]

    start = time.perf_counter()

    with ProcessPoolExecutor() as pool:
        futures = [loop.run_in_executor(pool, count_primes, n) for n in numbers]

        for n, coro in zip(numbers, asyncio.as_completed(futures)):
            result = await coro
            print(f"  Primes up to {n:,}: {result}")

    elapsed = time.perf_counter() - start
    print(f"Total: {elapsed:.2f}s")


if __name__ == "__main__":
    asyncio.run(main())
```

---

## 5. When to Use Threads vs Processes

| Scenario | Use | Why |
|----------|-----|-----|
| Blocking I/O (HTTP, file, DB) | `to_thread` / `ThreadPoolExecutor` | I/O releases GIL; threads work great |
| CPU-bound (math, parsing, compression) | `ProcessPoolExecutor` | Bypasses GIL; true parallelism |
| Already async (httpx, aiohttp) | Neither -- just `await` | Already non-blocking |
| Mixed I/O + CPU | Threads for I/O, processes for CPU | Best of both worlds |

---

## 6. Timing Comparison: Sequential vs Threaded vs Async

```python
import asyncio
import time


def sync_call(i: int) -> str:
    time.sleep(1.0)
    return f"call-{i}"


async def async_call(i: int) -> str:
    await asyncio.sleep(1.0)
    return f"call-{i}"


async def main() -> None:
    N = 5

    # Sequential (blocking)
    start = time.perf_counter()
    for i in range(N):
        sync_call(i)
    print(f"Sequential:  {time.perf_counter() - start:.2f}s")

    # Threaded (concurrent blocking)
    start = time.perf_counter()
    await asyncio.gather(*(asyncio.to_thread(sync_call, i) for i in range(N)))
    print(f"Threaded:    {time.perf_counter() - start:.2f}s")

    # Pure async (concurrent non-blocking)
    start = time.perf_counter()
    await asyncio.gather(*(async_call(i) for i in range(N)))
    print(f"Pure async:  {time.perf_counter() - start:.2f}s")


if __name__ == "__main__":
    asyncio.run(main())
```

**Expected output:**
```
Sequential:  5.00s
Threaded:    1.00s
Pure async:  1.00s
```

---

## 7. Practice Problems

### Problem 1: Compare sequential vs threaded

Use `simulate_io_operation_sync` from your `blocking_code.py` module.
Run 4 calls sequentially, then with `asyncio.to_thread`. Print timing.

```python
import asyncio
import time
from blocking_code import simulate_io_operation_sync


async def main() -> None:
    delays = [1.0, 1.0, 1.0, 1.0]

    # Sequential
    start = time.perf_counter()
    for d in delays:
        simulate_io_operation_sync(delay=d)
    print(f"Sequential: {time.perf_counter() - start:.2f}s")

    # Threaded
    start = time.perf_counter()
    # TODO: run all calls via asyncio.to_thread concurrently
    ...
    print(f"Threaded: {time.perf_counter() - start:.2f}s")


if __name__ == "__main__":
    asyncio.run(main())
```

### Problem 2: Mixed I/O and CPU tasks

Run `simulate_io_operation` (async) and `count_primes` (CPU, in process pool)
concurrently in the same program. Time the total.

```python
import asyncio
import time
from concurrent.futures import ProcessPoolExecutor


def count_primes(n: int) -> int:
    count = 0
    for num in range(2, n + 1):
        if all(num % i != 0 for i in range(2, int(num ** 0.5) + 1)):
            count += 1
    return count


async def simulate_io(delay: float) -> str:
    await asyncio.sleep(delay)
    return f"io done after {delay}s"


async def main() -> None:
    loop = asyncio.get_running_loop()
    start = time.perf_counter()

    # TODO: run both I/O and CPU tasks concurrently
    # Hint: use asyncio.gather with create_task for I/O
    #       and run_in_executor for CPU
    ...

    print(f"Total: {time.perf_counter() - start:.2f}s")


if __name__ == "__main__":
    asyncio.run(main())
```
