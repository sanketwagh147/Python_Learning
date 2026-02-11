# Advanced asyncio Concepts

This guide builds on your existing `asyncio` practice and the 
[blocking_code.py](blocking_code.py) module. It focuses on:

- `asyncio.TaskGroup` (structured concurrency)
- Using a **thread pool** to run blocking I/O (`simulate_io_operation_sync`) without blocking the event loop
- Using a **process pool** for CPU‑bound work
- Practice problems with boilerplate code

Python version assumed: **3.11+** (for `asyncio.TaskGroup`).

---

## 1. TaskGroup (Structured Concurrency)

`asyncio.TaskGroup` lets you manage a group of tasks as a single unit:

- All tasks are started together inside a `with` block
- If one task raises an exception, the others are **cancelled**
- The `with` block only exits when **all** tasks are finished or cancelled

### 1.1 Basic TaskGroup Example

This example uses the async function from [blocking_code.py](blocking_code.py):

```python
# blocking_code.py
# async def simulate_io_operation(delay: float | None = None, url: str = URL) -> dict[str, Any]:
#     ...
```

```python
import asyncio
from blocking_code import simulate_io_operation


async def call_api_with_taskgroup() -> None:
    async with asyncio.TaskGroup() as tg:
        task1 = tg.create_task(simulate_io_operation(delay=1.0))
        task2 = tg.create_task(simulate_io_operation(delay=2.0))
        task3 = tg.create_task(simulate_io_operation(delay=3.0))

    # When we reach here, all tasks are done or cancelled.
    # You can still inspect their results/exceptions:
    print("task1 done:", task1.done())
    print("task2 done:", task2.done())
    print("task3 done:", task3.done())
    print("task1 result:", task1.result())  # may raise if it failed


async def main() -> None:
    await call_api_with_taskgroup()


if __name__ == "__main__":
    asyncio.run(main())
```

### 1.2 Handling Exceptions in TaskGroup

If any task raises, `TaskGroup` will cancel the others and re‑raise at the end of the block.

```python
import asyncio
from blocking_code import simulate_io_operation


async def maybe_failing_call(delay: float | None) -> dict:
    # Just an example: treat delay > 2 as an error
    if delay is not None and delay > 2:
        raise ValueError(f"Bad delay: {delay}")
    return await simulate_io_operation(delay=delay)


async def taskgroup_with_errors() -> None:
    try:
        async with asyncio.TaskGroup() as tg:
            tg.create_task(maybe_failing_call(1.0))
            tg.create_task(maybe_failing_call(3.0))  # will raise
            tg.create_task(maybe_failing_call(0.5))
    except* ValueError as eg:
        # ExceptionGroup in Python 3.11+
        print("Caught ValueError group:", eg)


if __name__ == "__main__":
    asyncio.run(taskgroup_with_errors())
```

---

### 1.3 Practice Problem – TaskGroup

**Problem:**

You are given a list of delays. For each delay, call `simulate_io_operation(delay=...)` concurrently using `TaskGroup`.

Requirements:

- Start one task per delay
- Print when **each task finishes** with its delay value
- If any call raises an exception, cancel the remaining tasks and log which delay failed

**Boilerplate:**

```python
import asyncio
from blocking_code import simulate_io_operation


async def fetch_all_with_taskgroup(delays: list[float | None]) -> None:
    async with asyncio.TaskGroup() as tg:
        # TODO: create a task per delay
        # Hint: capture the delay so you can print it in a done-callback or after join
        ...


async def main() -> None:
    delays = [0.5, 1.0, 2.5, 3.5]
    await fetch_all_with_taskgroup(delays)


if __name__ == "__main__":
    asyncio.run(main())
```

Try solving this by:

- Attaching a `task.add_done_callback(...)` and passing the delay as metadata, or
- Keeping a list of `(delay, task)` pairs and printing after the `TaskGroup` finishes.

---

## 2. Thread Pool – Running Blocking I/O without Blocking the Event Loop

Your `blocking_code.py` module already has a **synchronous** version:

```python
# blocking_code.py
# def simulate_io_operation_sync(delay: float | None = None, url: str = URL) -> dict[str, Any]:
#     ...  # uses requests.get(...)
```

This is **blocking I/O**. If you call it directly in an async function, it will block the event loop.

Instead, use a **thread pool**:

- `asyncio.to_thread(func, *args, **kwargs)` (Python 3.9+), or
- `loop.run_in_executor(ThreadPoolExecutor, func, *args)`

### 2.1 Using asyncio.to_thread with simulate_io_operation_sync

```python
import asyncio
from blocking_code import simulate_io_operation_sync


async def call_sync_in_thread(delay: float | None) -> dict:
    # Runs simulate_io_operation_sync in a thread, non-blocking for the event loop
    result = await asyncio.to_thread(simulate_io_operation_sync, delay)
    return result


async def main() -> None:
    # Fire multiple blocking calls concurrently
    tasks = [
        asyncio.create_task(call_sync_in_thread(1.0)),
        asyncio.create_task(call_sync_in_thread(2.0)),
        asyncio.create_task(call_sync_in_thread(3.0)),
    ]

    for i, task in enumerate(asyncio.as_completed(tasks), start=1):
        result = await task
        print(f"Thread-pool task {i} completed: {result}")


if __name__ == "__main__":
    asyncio.run(main())
```

### 2.2 Practice Problem – Thread Pool

**Problem:**

Use a thread pool to call `simulate_io_operation_sync` concurrently for a list of delays, and compare total elapsed time vs. calling them sequentially.

**Boilerplate:**

```python
import asyncio
import time
from blocking_code import simulate_io_operation_sync


def call_sync_sequential(delays: list[float | None]) -> None:
    start = time.time()
    for delay in delays:
        simulate_io_operation_sync(delay=delay)
    print(f"Sequential took: {time.time() - start:.2f}s")


async def call_sync_with_threads(delays: list[float | None]) -> None:
    start = time.time()
    # TODO: use asyncio.to_thread to run simulate_io_operation_sync for each delay concurrently
    ...
    print(f"Threaded took: {time.time() - start:.2f}s")


async def main() -> None:
    delays = [1.0, 1.5, 2.0]
    call_sync_sequential(delays)
    await call_sync_with_threads(delays)


if __name__ == "__main__":
    asyncio.run(main())
```

Goal: observe the time difference between sequential and threaded execution.

---

## 3. Process Pool – Offloading CPU-Bound Work

Threads are great for **I/O-bound** code. For **CPU-bound** tasks (heavy computation), use a **process pool** so that work can run in parallel on multiple CPU cores.

We will define a CPU-bound function (you can put this in a new module, or at the bottom of `blocking_code.py`):

```python
# Example CPU-bound function

def cpu_bound_operation(n: int) -> int:
    """Naive CPU-heavy function: count primes up to n."""
    def is_prime(x: int) -> bool:
        if x < 2:
            return False
        for i in range(2, int(x ** 0.5) + 1):
            if x % i == 0:
                return False
        return True

    return sum(1 for i in range(n + 1) if is_prime(i))
```

### 3.1 Using ProcessPoolExecutor with asyncio

```python
import asyncio
from concurrent.futures import ProcessPoolExecutor
from typing import Iterable

from blocking_code import cpu_bound_operation  # define this as shown above


async def run_cpu_bound_in_process_pool(numbers: Iterable[int]) -> list[int]:
    loop = asyncio.get_running_loop()

    # Use a shared ProcessPoolExecutor (ideally one per app, not per call)
    with ProcessPoolExecutor() as pool:
        tasks = [
            loop.run_in_executor(pool, cpu_bound_operation, n)
            for n in numbers
        ]
        results = await asyncio.gather(*tasks)

    return results


async def main() -> None:
    numbers = [50_000, 60_000, 70_000]
    results = await run_cpu_bound_in_process_pool(numbers)
    for n, primes in zip(numbers, results, strict=True):
        print(f"Up to {n}, found {primes} primes")


if __name__ == "__main__":
    asyncio.run(main())
```

### 3.2 Practice Problem – Process Pool

**Problem:**

Given a list of integers, use a process pool to compute `cpu_bound_operation(n)` for each number concurrently, and then:

- Print them in the order **they complete**, not the original order
- Measure and print total time taken

**Boilerplate:**

```python
import asyncio
import time
from concurrent.futures import ProcessPoolExecutor

from blocking_code import cpu_bound_operation  # implement as shown earlier


async def run_cpu_tasks(numbers: list[int]) -> None:
    loop = asyncio.get_running_loop()
    start = time.time()

    with ProcessPoolExecutor() as pool:
        futures = [
            loop.run_in_executor(pool, cpu_bound_operation, n)
            for n in numbers
        ]

        # TODO: print results as soon as each finishes (hint: asyncio.as_completed)
        ...

    print(f"Process pool took: {time.time() - start:.2f}s")


async def main() -> None:
    numbers = [80_000, 100_000, 120_000]
    await run_cpu_tasks(numbers)


if __name__ == "__main__":
    asyncio.run(main())
```

---

## 4. Summary / What to Practice Next

Ideas for further practice using this file and `blocking_code.py`:

- Combine `TaskGroup` with a thread pool: some tasks use `simulate_io_operation`, others wrap `simulate_io_operation_sync` via `asyncio.to_thread`.
- Add cancellation: cancel the whole `TaskGroup` if any task takes longer than a timeout.
- Add logging inside your callback functions (like you did) to trace start/finish times for each task.

As you implement the boilerplate sections (`...`), try to:

- Avoid blocking calls directly in async functions
- Use `TaskGroup` instead of manual task lists when starting groups of related tasks
- Use thread pools for I/O‑bound sync code and process pools for CPU‑bound work
