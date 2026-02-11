# Cancellation, Timeouts, and Shielding

Covers:
- `task.cancel()` and `CancelledError`
- `asyncio.timeout()` (3.11+)
- `asyncio.wait_for()`
- `asyncio.shield()`

Python version: **3.11+** for `asyncio.timeout()`.

---

## 1. Cancellation Basics

Any awaiting task can be cancelled. When cancelled, the next `await` inside
that task raises `asyncio.CancelledError`.

### 1.1 Cancelling a task manually

```python
import asyncio


async def long_running() -> str:
    print("long_running: started")
    try:
        await asyncio.sleep(10)
        return "done"
    except asyncio.CancelledError:
        print("long_running: I was cancelled!")
        # You can do cleanup here (close connections, flush buffers, etc.)
        raise  # Always re-raise CancelledError unless you have a good reason


async def main() -> None:
    task = asyncio.create_task(long_running())

    await asyncio.sleep(1)       # let it run for 1 second
    task.cancel()                 # request cancellation
    print(f"cancel requested: {task.cancelled()}")

    try:
        await task                # CancelledError propagates here
    except asyncio.CancelledError:
        print("main: caught CancelledError")


if __name__ == "__main__":
    asyncio.run(main())
```

**Output:**
```
long_running: started
cancel requested: False
long_running: I was cancelled!
main: caught CancelledError
```

### 1.2 Key points about cancellation

- `task.cancel()` does NOT immediately stop the task — it schedules a `CancelledError`
- The error is raised at the next `await` point inside the task
- You can catch `CancelledError` for cleanup, but always re-raise it
- `task.cancelled()` returns `True` only after the task has actually finished with cancellation

---

## 2. asyncio.timeout() — Context Manager (3.11+)

`asyncio.timeout(seconds)` creates a scope. If the code inside doesn't
complete within the given time, it raises `TimeoutError`.

```python
import asyncio


async def slow_operation(delay: float) -> str:
    print(f"slow_operation: sleeping {delay}s...")
    await asyncio.sleep(delay)
    return f"completed after {delay}s"


async def main() -> None:
    # Case 1: completes in time
    try:
        async with asyncio.timeout(3.0):
            result = await slow_operation(1.0)
            print(f"Success: {result}")
    except TimeoutError:
        print("Timed out!")

    print("---")

    # Case 2: times out
    try:
        async with asyncio.timeout(1.0):
            result = await slow_operation(5.0)
            print(f"Success: {result}")  # never reached
    except TimeoutError:
        print("Timed out! (expected)")


if __name__ == "__main__":
    asyncio.run(main())
```

**Output:**
```
slow_operation: sleeping 1.0s...
Success: completed after 1.0s
---
slow_operation: sleeping 5.0s...
Timed out! (expected)
```

### 2.1 Reschedule a timeout

You can adjust the deadline dynamically:

```python
import asyncio


async def main() -> None:
    try:
        async with asyncio.timeout(2.0) as cm:
            print(f"Original deadline: {cm.when():.2f}")

            # Extend the deadline by 3 more seconds
            cm.reschedule(cm.when() + 3.0)
            print(f"New deadline: {cm.when():.2f}")

            await asyncio.sleep(4.0)  # would have timed out without reschedule
            print("Completed!")
    except TimeoutError:
        print("Timed out!")


if __name__ == "__main__":
    asyncio.run(main())
```

---

## 3. asyncio.wait_for()

`wait_for(coro, timeout)` wraps a coroutine with a timeout.
**It cancels the underlying task** if the timeout expires.

### 3.1 Difference from asyncio.timeout()

| Feature | `asyncio.timeout()` | `asyncio.wait_for()` |
|---------|---------------------|----------------------|
| Syntax | Context manager | Function wrapping a coroutine |
| Scope | Can cover multiple awaits | Wraps exactly one coroutine |
| Reschedule | Yes (`cm.reschedule()`) | No |
| Cancels inner task | Yes | Yes |

### 3.2 Example

```python
import asyncio


async def slow_api_call() -> dict:
    print("API call started...")
    await asyncio.sleep(5.0)
    return {"status": "ok"}


async def main() -> None:
    # Give the API call 2 seconds max
    try:
        result = await asyncio.wait_for(slow_api_call(), timeout=2.0)
        print(f"Got result: {result}")
    except asyncio.TimeoutError:
        print("API call timed out after 2s")


if __name__ == "__main__":
    asyncio.run(main())
```

### 3.3 Retry pattern with wait_for

```python
import asyncio


async def unreliable_operation() -> str:
    await asyncio.sleep(3.0)  # sometimes slow
    return "success"


async def retry_with_timeout(max_retries: int = 3, timeout: float = 1.0) -> str | None:
    for attempt in range(1, max_retries + 1):
        try:
            result = await asyncio.wait_for(unreliable_operation(), timeout=timeout)
            print(f"  Attempt {attempt}: success!")
            return result
        except asyncio.TimeoutError:
            backoff = timeout * attempt
            print(f"  Attempt {attempt}: timed out, retrying in {backoff}s...")
            await asyncio.sleep(backoff)

    print("  All retries exhausted")
    return None


async def main() -> None:
    result = await retry_with_timeout(max_retries=3, timeout=1.0)
    print(f"Final result: {result}")


if __name__ == "__main__":
    asyncio.run(main())
```

---

## 4. asyncio.shield()

`asyncio.shield()` protects a coroutine from cancellation of the *outer* task.
Even if the outer task is cancelled, the shielded coroutine keeps running.

### 4.1 When to use shield

- Critical operations that **must complete**: database commits, payment processing, file flushes
- You want to notify the caller that we "timed out" but still finish the work in the background

### 4.2 Example: shielded database save

```python
import asyncio


async def save_to_database(data: str) -> str:
    """Critical operation — must not be interrupted."""
    print(f"  DB save started for: {data}")
    await asyncio.sleep(3.0)  # simulate slow DB write
    print(f"  DB save completed for: {data}")
    return "saved"


async def process_request(data: str) -> None:
    try:
        # shield() prevents cancellation of save_to_database
        result = await asyncio.wait_for(
            asyncio.shield(save_to_database(data)),
            timeout=1.0,
        )
        print(f"Request completed: {result}")
    except asyncio.TimeoutError:
        print("Request timed out, but DB save continues in background!")


async def main() -> None:
    await process_request("user-data-123")

    # Wait a bit so the shielded operation can finish
    print("Waiting for background operations...")
    await asyncio.sleep(3.0)
    print("Done")


if __name__ == "__main__":
    asyncio.run(main())
```

**Output:**
```
  DB save started for: user-data-123
Request timed out, but DB save continues in background!
Waiting for background operations...
  DB save completed for: user-data-123
Done
```

### 4.3 Common mistake with shield

If you don't keep the event loop alive, the shielded coroutine won't complete:

```python
# BAD: program exits before shielded operation completes
async def main() -> None:
    try:
        await asyncio.wait_for(asyncio.shield(save_to_database("x")), timeout=1.0)
    except asyncio.TimeoutError:
        print("Timed out")
    # Program exits here — shielded task never finishes!
```

Always ensure the event loop stays alive long enough for shielded tasks.

---

## 5. Combining timeout + TaskGroup

```python
import asyncio


async def fetch(name: str, delay: float) -> str:
    await asyncio.sleep(delay)
    return f"{name} done"


async def main() -> None:
    try:
        async with asyncio.timeout(2.5):
            async with asyncio.TaskGroup() as tg:
                tg.create_task(fetch("A", 1.0))
                tg.create_task(fetch("B", 2.0))
                tg.create_task(fetch("C", 5.0))  # this will cause timeout
    except TimeoutError:
        print("TaskGroup timed out — all tasks cancelled")


if __name__ == "__main__":
    asyncio.run(main())
```

---

## 6. Practice Problems

### Problem 1: Retry with exponential backoff

Implement a function that calls a flaky API (simulate with `asyncio.sleep`
that sometimes exceeds the timeout). Retry up to N times with exponential
backoff.

```python
import asyncio
import random


async def flaky_api() -> str:
    delay = random.uniform(0.5, 3.0)
    await asyncio.sleep(delay)
    return f"response (took {delay:.2f}s)"


async def fetch_with_retry(max_retries: int = 3, timeout: float = 1.0) -> str | None:
    # TODO: implement retry loop with asyncio.wait_for and exponential backoff
    ...


if __name__ == "__main__":
    asyncio.run(fetch_with_retry())
```

### Problem 2: Shield a critical operation

Write a function that processes items from a list. Each item has a "save"
step. Use `shield()` to ensure saving always completes even if the overall
processing is cancelled.

```python
import asyncio


async def save_item(item: str) -> None:
    print(f"  Saving {item}...")
    await asyncio.sleep(2.0)
    print(f"  Saved {item}")


async def process_items(items: list[str], timeout: float) -> None:
    # TODO: process each item with a timeout
    # TODO: use shield() on save_item so it completes even if timed out
    ...


if __name__ == "__main__":
    asyncio.run(process_items(["A", "B", "C"], timeout=1.0))
```
