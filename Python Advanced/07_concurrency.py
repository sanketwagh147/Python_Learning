"""
================================================================================
  CONCURRENCY — Threading, Multiprocessing, and Asyncio Mastery
================================================================================
  Author: Senior Software Engineer Practice Guide
  Goal:   Understand the GIL, know when to use threads vs processes vs async,
          write thread-safe code, and avoid concurrency bugs.
================================================================================
"""

# ─────────────────────────────────────────────────────────────────────────────
# SECTION 1: UNDER THE HOOD — GIL, Threads, Processes, and the Event Loop
# ─────────────────────────────────────────────────────────────────────────────
"""
THE GLOBAL INTERPRETER LOCK (GIL):
    CPython has a mutex (the GIL) that allows only ONE thread to execute
    Python bytecode at a time.  This means:

    ┌─────────────────────────────────────────────────────────────────────┐
    │  CPU-bound work → threads WON'T speed things up (GIL blocks them) │
    │  I/O-bound work → threads WILL help (GIL is released during I/O)  │
    └─────────────────────────────────────────────────────────────────────┘

WHEN TO USE WHAT:

    ┌──────────────────┬──────────────┬────────────────┬────────────────┐
    │  Scenario        │  threading   │ multiprocessing │ asyncio        │
    ├──────────────────┼──────────────┼────────────────┼────────────────┤
    │  HTTP requests   │  ✓ Good      │  Overkill      │  ✓✓ Best       │
    │  File I/O        │  ✓ Good      │  ✓ OK          │  ✓ Good        │
    │  CPU math/ML     │  ✗ No help   │  ✓✓ Best       │  ✗ No help     │
    │  Web scraping    │  ✓ Good      │  ✓ OK          │  ✓✓ Best       │
    │  DB queries      │  ✓ Good      │  ✓ OK          │  ✓✓ Best       │
    │  Image processing│  ✗ No help   │  ✓✓ Best       │  ✗ No help     │
    └──────────────────┴──────────────┴────────────────┴────────────────┘

    Rule of thumb:
    - I/O-bound + many connections → asyncio
    - I/O-bound + simple          → threading  
    - CPU-bound                   → multiprocessing

KEY DUNDER METHODS / PROTOCOLS:
    - threading: no dunders, but Thread.__init__(), .run(), .start(), .join()
    - asyncio:   __aenter__, __aexit__, __aiter__, __anext__
                 async def → returns a coroutine object
                 await     → yields control back to the event loop
    - Locks:     __enter__/__exit__ (used as context managers)
"""

import threading
import time
import queue
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor, as_completed


# ─────────────────────────────────────────────────────────────────────────────
# SECTION 2: PRODUCTION-READY EXAMPLES
# ─────────────────────────────────────────────────────────────────────────────

# ── Example 1: Thread-Safe Rate-Limited API Client ──────────────────────────

class RateLimitedClient:
    """
    Production-ready concurrent HTTP client with rate limiting.
    Uses ThreadPoolExecutor for I/O-bound HTTP requests with a
    semaphore to enforce max concurrent requests.
    """

    def __init__(self, max_concurrent: int = 5, max_per_second: float = 10):
        self._semaphore = threading.Semaphore(max_concurrent)
        self._rate_lock = threading.Lock()
        self._min_interval = 1.0 / max_per_second
        self._last_request_time = 0.0
        self._results_lock = threading.Lock()

    def _rate_wait(self):
        """Enforce rate limit using token bucket approach."""
        with self._rate_lock:
            now = time.monotonic()
            wait_time = self._min_interval - (now - self._last_request_time)
            if wait_time > 0:
                time.sleep(wait_time)
            self._last_request_time = time.monotonic()

    def _fetch_one(self, url: str) -> dict:
        """Fetch a single URL with rate limiting and concurrency control."""
        with self._semaphore:
            self._rate_wait()
            # Simulate HTTP request (replace with requests.get in production)
            time.sleep(0.05)  # simulate network latency
            return {"url": url, "status": 200, "thread": threading.current_thread().name}

    def fetch_all(self, urls: list, max_workers: int = 5) -> list:
        """Fetch all URLs concurrently, respecting rate limits."""
        results = []
        errors = []

        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            future_to_url = {executor.submit(self._fetch_one, url): url for url in urls}

            for future in as_completed(future_to_url):
                url = future_to_url[future]
                try:
                    result = future.result()
                    results.append(result)
                except Exception as exc:
                    errors.append({"url": url, "error": str(exc)})

        return {"results": results, "errors": errors}


# ── Example 2: Producer-Consumer with Thread-Safe Queue ─────────────────────

class DataPipeline:
    """
    Production producer-consumer pattern using queue.Queue.
    
    Queue is ALREADY thread-safe (uses internal locks).
    This is the RIGHT way to share data between threads.
    """

    def __init__(self, num_workers: int = 3):
        self._task_queue = queue.Queue(maxsize=100)
        self._result_queue = queue.Queue()
        self._num_workers = num_workers
        self._workers = []
        self._shutdown = threading.Event()

    def _worker(self, worker_id: int):
        """Worker thread — processes tasks from queue."""
        while not self._shutdown.is_set():
            try:
                task = self._task_queue.get(timeout=0.5)
            except queue.Empty:
                continue

            if task is None:  # Poison pill → shut down
                self._task_queue.task_done()
                break

            try:
                result = self._process(task, worker_id)
                self._result_queue.put(result)
            except Exception as e:
                self._result_queue.put({"task": task, "error": str(e)})
            finally:
                self._task_queue.task_done()

    def _process(self, task: dict, worker_id: int) -> dict:
        """Process a single task. Override in subclass for real work."""
        time.sleep(0.01)  # simulate work
        return {
            "task_id": task.get("id"),
            "result": task.get("data", 0) * 2,
            "worker": worker_id,
        }

    def start(self):
        """Start worker threads."""
        for i in range(self._num_workers):
            t = threading.Thread(target=self._worker, args=(i,), daemon=True)
            t.start()
            self._workers.append(t)

    def submit(self, task: dict):
        """Submit a task to the pipeline."""
        self._task_queue.put(task)

    def shutdown(self, wait: bool = True):
        """Graceful shutdown — send poison pills and wait."""
        for _ in self._workers:
            self._task_queue.put(None)
        if wait:
            for w in self._workers:
                w.join(timeout=5.0)
        self._shutdown.set()

    def get_results(self) -> list:
        """Collect all available results."""
        results = []
        while not self._result_queue.empty():
            try:
                results.append(self._result_queue.get_nowait())
            except queue.Empty:
                break
        return results


# ── Example 3: Async Context Manager for DB Connection Pool ─────────────────

import asyncio


class AsyncConnectionPool:
    """
    Async connection pool using __aenter__/__aexit__.
    
    Demonstrates:
    - async context manager protocol
    - asyncio.Semaphore for concurrency control
    - asyncio.Queue for connection reuse
    """

    def __init__(self, max_size: int = 5, dsn: str = "postgresql://localhost/db"):
        self._dsn = dsn
        self._max_size = max_size
        self._semaphore = asyncio.Semaphore(max_size)
        self._pool: asyncio.Queue = asyncio.Queue(maxsize=max_size)
        self._size = 0
        self._lock = asyncio.Lock()

    async def _create_connection(self):
        """Simulate creating a DB connection."""
        await asyncio.sleep(0.01)  # simulate connection time
        self._size += 1
        conn_id = self._size
        return {"id": conn_id, "dsn": self._dsn, "active": True}

    async def acquire(self):
        """Get a connection from pool (or create new one)."""
        await self._semaphore.acquire()
        try:
            conn = self._pool.get_nowait()
        except asyncio.QueueEmpty:
            conn = await self._create_connection()
        return conn

    async def release(self, conn):
        """Return connection to pool."""
        try:
            self._pool.put_nowait(conn)
        except asyncio.QueueFull:
            pass  # discard if pool is full
        finally:
            self._semaphore.release()

    async def __aenter__(self):
        """Acquire a connection when entering async with block."""
        self._conn = await self.acquire()
        return self._conn

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Release connection when exiting async with block."""
        await self.release(self._conn)
        return False  # don't suppress exceptions


# Usage pattern (in an async context):
# async def query_db():
#     pool = AsyncConnectionPool(max_size=10)
#     async with pool as conn:
#         result = await execute_query(conn, "SELECT * FROM users")
#     # Connection automatically returned to pool


# ── Example 4: CPU-Bound Work with multiprocessing ─────────────────────────

def cpu_heavy_task(n: int) -> dict:
    """Simulate CPU-bound work (e.g., image processing, ML inference)."""
    total = sum(i * i for i in range(n))
    return {"n": n, "result": total}


def parallel_compute(tasks: list, max_workers: int = None) -> list:
    """
    Run CPU-bound tasks in parallel using ProcessPoolExecutor.
    Each task runs in a SEPARATE process with its own GIL.
    """
    results = []
    with ProcessPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(cpu_heavy_task, n): n for n in tasks}
        for future in as_completed(futures):
            try:
                results.append(future.result())
            except Exception as e:
                results.append({"error": str(e)})
    return results


# ─────────────────────────────────────────────────────────────────────────────
# SECTION 3: COMMON PITFALLS — Top 3 Bugs Juniors Introduce
# ─────────────────────────────────────────────────────────────────────────────
"""
PITFALL 1: Race conditions with shared mutable state
───────────────────────────────────────────────────────────────────────────
    counter = 0
    def increment():
        global counter
        counter += 1   # NOT atomic!  Read → Modify → Write can interleave
    
    FIX: Use threading.Lock(), or use queue.Queue, or use atomic types
         from the `atomics` package, or avoid sharing state entirely.


PITFALL 2: Deadlocks from inconsistent lock ordering
───────────────────────────────────────────────────────────────────────────
    Thread A: lock1.acquire() → lock2.acquire() → done
    Thread B: lock2.acquire() → lock1.acquire() → done
    
    If A grabs lock1 and B grabs lock2 simultaneously → DEADLOCK.
    
    FIX: Always acquire locks in the SAME ORDER across all threads.
         Use contextlib.ExitStack for dynamic lock ordering.
         Use timeout: lock.acquire(timeout=5)


PITFALL 3: Using threads for CPU-bound work (GIL trap)
───────────────────────────────────────────────────────────────────────────
    # This is SLOWER than single-threaded due to GIL contention:
    with ThreadPoolExecutor(max_workers=8) as pool:
        pool.map(heavy_cpu_function, data)
    
    FIX: Use ProcessPoolExecutor for CPU-bound work.
         Use ThreadPoolExecutor ONLY for I/O-bound work.
"""


# ─────────────────────────────────────────────────────────────────────────────
# SECTION 4: BROKEN CODE CHALLENGES — Fix These!
# ─────────────────────────────────────────────────────────────────────────────

# ── Challenge 1: Race condition in bank transfer ────────────────────────────
"""
PROBLEM: Two threads transferring money simultaneously cause balance
         corruption.  The total money in the system changes!

HINT:    - The read-modify-write on balances is not atomic
         - You need to lock BOTH accounts, but watch out for deadlocks
         - Use consistent lock ordering (always lock lower account ID first)
"""


class BrokenBankAccount:
    def __init__(self, account_id: int, balance: float):
        self.account_id = account_id
        self.balance = balance

    def deposit(self, amount: float):
        self.balance += amount  # BUG: not atomic

    def withdraw(self, amount: float):
        self.balance -= amount  # BUG: not atomic


def broken_transfer(from_acct, to_acct, amount):
    """BUG: No locking → race condition."""
    if from_acct.balance >= amount:
        # BUG: Another thread could change balance between check and modify
        time.sleep(0.001)  # simulate slow operation
        from_acct.withdraw(amount)
        to_acct.deposit(amount)


# ── Challenge 2: Async code that accidentally blocks ───────────────────────
"""
PROBLEM: This "async" code blocks the event loop, making all other
         coroutines wait.

HINT:    - time.sleep() blocks the ENTIRE thread (including event loop)
         - Use asyncio.sleep() for async delays
         - For CPU-bound work in async, use loop.run_in_executor()
         - For blocking I/O, wrap in asyncio.to_thread() (Python 3.9+)
"""


async def broken_fetch_data(url: str) -> dict:
    """BUG: Blocks the event loop!"""
    # BUG 1: time.sleep blocks the event loop
    time.sleep(1)  # should be: await asyncio.sleep(1)

    # BUG 2: CPU-bound work blocks event loop
    result = sum(i * i for i in range(1000000))

    # BUG 3: Synchronous file I/O blocks event loop
    # with open("data.txt") as f:
    #     data = f.read()   # should use aiofiles or run_in_executor

    return {"url": url, "result": result}


async def broken_main():
    """All three fetches run SEQUENTIALLY because of blocking."""
    urls = ["http://api1.com", "http://api2.com", "http://api3.com"]
    # BUG: These don't actually run concurrently
    tasks = [broken_fetch_data(url) for url in urls]
    # Should be: tasks = [asyncio.create_task(fetch(url)) for url in urls]
    results = []
    for task in tasks:
        results.append(await task)
    return results


# ── Challenge 3: Thread pool that leaks threads ────────────────────────────
"""
PROBLEM: This server creates threads without bounds and never cleans them up.
         Under load, it creates thousands of threads and crashes.

HINT:    - Use a bounded thread pool (ThreadPoolExecutor)
         - Add proper shutdown handling
         - Consider using a semaphore to limit concurrency
"""


class BrokenServer:
    def __init__(self):
        self.running = True

    def handle_request(self, request_data):
        """Handle a single request."""
        time.sleep(0.1)  # simulate work
        return f"Processed: {request_data}"

    def serve(self, requests):
        """BUG: Unbounded thread creation!"""
        threads = []
        for req in requests:
            # BUG: Creates a new thread per request with no limit
            t = threading.Thread(target=self.handle_request, args=(req,))
            t.start()
            threads.append(t)
            # BUG: Never joins threads, never checks if they're done
        # BUG: threads list grows forever


# ─────────────────────────────────────────────────────────────────────────────
# SECTION 5: REFACTORING CHALLENGE
# ─────────────────────────────────────────────────────────────────────────────
"""
REFACTORING CHALLENGE: Sequential Web Scraper → Concurrent
───────────────────────────────────────────────────────────

The function below scrapes URLs sequentially (one at a time).
Refactor it to:
    1. Use ThreadPoolExecutor for concurrent I/O
    2. Add a rate limit (max 5 requests per second)
    3. Add proper error handling per URL (don't let one failure stop all)
    4. Add a timeout per request
    5. Collect results in a thread-safe manner
"""


def messy_scraper(urls: list) -> list:
    """Sequential scraper — refactor me for concurrency!"""
    results = []
    for url in urls:
        try:
            # Simulate HTTP request
            time.sleep(0.5)  # pretend this is requests.get(url)
            response_data = f"Data from {url}"

            # Simulate parsing
            time.sleep(0.1)  # pretend this is BeautifulSoup parsing
            parsed = response_data.upper()

            # Simulate saving
            time.sleep(0.05)  # pretend this is writing to DB
            results.append({"url": url, "data": parsed, "status": "ok"})
            print(f"  Scraped: {url}")
        except Exception as e:
            results.append({"url": url, "error": str(e), "status": "failed"})
            print(f"  Failed: {url} — {e}")
            # BUG: If we raise here, all remaining URLs are skipped
    return results


# ─────────────────────────────────────────────────────────────────────────────
# QUICK SELF-TEST
# ─────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("=" * 60)
    print("  07_concurrency.py — Self Test")
    print("=" * 60)

    # Test rate-limited client
    print("\n[Test] RateLimitedClient:")
    client = RateLimitedClient(max_concurrent=3, max_per_second=20)
    urls = [f"http://api.example.com/item/{i}" for i in range(6)]
    result = client.fetch_all(urls, max_workers=3)
    print(f"  Fetched {len(result['results'])} URLs, {len(result['errors'])} errors")
    assert len(result['results']) == 6

    # Test producer-consumer pipeline
    print("\n[Test] DataPipeline (producer-consumer):")
    pipeline = DataPipeline(num_workers=2)
    pipeline.start()
    for i in range(5):
        pipeline.submit({"id": i, "data": i * 10})
    time.sleep(0.5)  # let workers process
    pipeline.shutdown(wait=True)
    results = pipeline.get_results()
    print(f"  Processed {len(results)} tasks")
    assert len(results) == 5

    # Test async context manager
    print("\n[Test] AsyncConnectionPool:")
    async def test_pool():
        pool = AsyncConnectionPool(max_size=3)
        async with pool as conn:
            assert conn["active"] is True
            return conn["id"]

    conn_id = asyncio.run(test_pool())
    print(f"  Got connection id: {conn_id}")

    # Note: Skipping ProcessPoolExecutor test (heavy for self-test)
    print("\n[Test] CPU parallel (skipped in self-test — use ProcessPoolExecutor)")

    print("\n✓ All concurrency tests passed!")
    print("=" * 60)
