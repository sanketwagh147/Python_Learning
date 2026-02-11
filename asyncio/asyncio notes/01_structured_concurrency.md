# Structured Concurrency in asyncio

Covers:
- `asyncio.TaskGroup`
- `ExceptionGroup` and `except*`

Python version: **3.11+**

---

## 1. What is Structured Concurrency?

Traditional asyncio lets you scatter tasks anywhere:

```python
# Unstructured: tasks float around, you manage their lifetime manually
task1 = asyncio.create_task(do_something())
task2 = asyncio.create_task(do_something_else())
# ... who cancels these if something fails? You have to handle it yourself.
await task1
await task2
```

**Structured concurrency** ties the lifetime of tasks to a scope. When the scope
exits, all tasks are guaranteed to be done or cancelled. No leaked tasks.

---

## 2. asyncio.TaskGroup

### 2.1 Basic example

```python
import asyncio
import time


async def fetch(name: str, delay: float) -> str:
    print(f"  [{name}] started  (delay={delay}s)")
    await asyncio.sleep(delay)
    print(f"  [{name}] finished")
    return f"{name}-result"


async def main() -> None:
    start = time.perf_counter()

    async with asyncio.TaskGroup() as tg:
        t1 = tg.create_task(fetch("A", 1.0))
        t2 = tg.create_task(fetch("B", 2.0))
        t3 = tg.create_task(fetch("C", 1.5))

    # All tasks are done here
    elapsed = time.perf_counter() - start
    print(f"\nResults: {t1.result()}, {t2.result()}, {t3.result()}")
    print(f"Total time: {elapsed:.2f}s (should be ~2s, not 4.5s)")


if __name__ == "__main__":
    asyncio.run(main())
```

**Expected output:**
```
  [A] started  (delay=1.0s)
  [B] started  (delay=2.0s)
  [C] started  (delay=1.5s)
  [A] finished
  [C] finished
  [B] finished

Results: A-result, B-result, C-result
Total time: 2.00s (should be ~2s, not 4.5s)
```

### 2.2 Key rules

| Rule | Detail |
|------|--------|
| Tasks are created with `tg.create_task()` | Not `asyncio.create_task()` |
| Block waits for ALL tasks | Even if one finishes early |
| Exception in any task → others cancelled | Re-raised as `ExceptionGroup` |
| You can still read `task.result()` after the block | For tasks that succeeded |

---

## 3. ExceptionGroup and except*

### 3.1 What happens when a task fails

```python
import asyncio


async def good_task(name: str) -> str:
    await asyncio.sleep(0.5)
    return f"{name} OK"


async def bad_task(name: str) -> str:
    await asyncio.sleep(0.3)
    raise ValueError(f"{name} failed!")


async def main() -> None:
    try:
        async with asyncio.TaskGroup() as tg:
            tg.create_task(good_task("A"))
            tg.create_task(bad_task("B"))       # raises ValueError
            tg.create_task(good_task("C"))
    except* ValueError as eg:
        # eg is an ExceptionGroup containing all ValueErrors
        print(f"Caught {len(eg.exceptions)} ValueError(s):")
        for exc in eg.exceptions:
            print(f"  - {exc}")


if __name__ == "__main__":
    asyncio.run(main())
```

**What happens step by step:**

1. All three tasks start concurrently
2. `bad_task("B")` raises after 0.3s
3. `TaskGroup` cancels `good_task("A")` and `good_task("C")`
4. After all tasks finish/cancel, `TaskGroup` raises an `ExceptionGroup`
5. `except* ValueError` catches only ValueErrors from the group

### 3.2 Multiple exception types

```python
import asyncio


async def raise_value_error() -> None:
    await asyncio.sleep(0.1)
    raise ValueError("bad value")


async def raise_runtime_error() -> None:
    await asyncio.sleep(0.2)
    raise RuntimeError("something broke")


async def main() -> None:
    try:
        async with asyncio.TaskGroup() as tg:
            tg.create_task(raise_value_error())
            tg.create_task(raise_runtime_error())
    except* ValueError as eg:
        print("ValueErrors:")
        for exc in eg.exceptions:
            print(f"  - {exc}")
    except* RuntimeError as eg:
        print("RuntimeErrors:")
        for exc in eg.exceptions:
            print(f"  - {exc}")


if __name__ == "__main__":
    asyncio.run(main())
```

**Output:**
```
ValueErrors:
  - bad value
RuntimeErrors:
  - something broke
```

Both `except*` blocks run because the `ExceptionGroup` contains both types.

---

## 4. TaskGroup vs asyncio.gather — When to Use Which

| Feature | `TaskGroup` | `asyncio.gather()` |
|---------|-------------|---------------------|
| Scope | Structured — tasks tied to `async with` block | Unstructured — tasks float in the event loop |
| Error handling | Cancels all tasks, raises `ExceptionGroup` | With `return_exceptions=True`, returns exceptions as values; otherwise first exception propagates |
| Cancellation | Automatic for sibling tasks on failure | Manual — you handle it yourself |
| Adding tasks dynamically | Yes, inside the `async with` block | No — you pass all coroutines upfront |
| Python version | 3.11+ | 3.4+ |

**Rule of thumb:**
- Use `TaskGroup` when tasks are related and should fail/cancel together
- Use `gather` when you just need to run independent things concurrently and handle results individually

---

## 5. Dynamic task creation in TaskGroup

You can create tasks conditionally inside the block:

```python
import asyncio


async def fetch(url: str) -> str:
    await asyncio.sleep(0.5)
    return f"data from {url}"


async def main() -> None:
    urls = [
        "http://api.example.com/users",
        "http://api.example.com/posts",
        "http://api.example.com/comments",
    ]

    results: dict[str, str] = {}

    async with asyncio.TaskGroup() as tg:
        tasks = {}
        for url in urls:
            task = tg.create_task(fetch(url))
            tasks[url] = task

    # All done — collect results
    for url, task in tasks.items():
        results[url] = task.result()
        print(f"{url} → {results[url]}")


if __name__ == "__main__":
    asyncio.run(main())
```

---

## 6. Practice Problems

### Problem 1: TaskGroup with done callbacks

Use `TaskGroup` to start 4 API calls with different delays. Attach a
`add_done_callback` to each task that prints which delay finished.

```python
import asyncio
from functools import partial


async def simulate(delay: float) -> dict:
    await asyncio.sleep(delay)
    return {"delay": delay, "status": "ok"}


def on_done(task: asyncio.Task, delay: float) -> None:
    # TODO: print the delay and whether the task succeeded or failed
    ...


async def main() -> None:
    delays = [0.5, 1.0, 1.5, 2.0]

    async with asyncio.TaskGroup() as tg:
        for delay in delays:
            task = tg.create_task(simulate(delay))
            # TODO: attach callback with delay as metadata
            ...


if __name__ == "__main__":
    asyncio.run(main())
```

### Problem 2: Exception classification

Create tasks that raise different exception types. Handle each type in a
separate `except*` block and print a summary.

```python
import asyncio


async def flaky_operation(op_id: int) -> str:
    await asyncio.sleep(0.1 * op_id)
    if op_id % 3 == 0:
        raise ConnectionError(f"op {op_id}: connection lost")
    if op_id % 3 == 1:
        raise TimeoutError(f"op {op_id}: timed out")
    return f"op {op_id}: success"


async def main() -> None:
    # TODO: run flaky_operation(1) through flaky_operation(6) in a TaskGroup
    # TODO: handle ConnectionError and TimeoutError separately with except*
    ...


if __name__ == "__main__":
    asyncio.run(main())
```
