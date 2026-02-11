# asyncio Synchronization Primitives

Covers:
- `asyncio.Lock`
- `asyncio.Semaphore` / `asyncio.BoundedSemaphore`
- `asyncio.Event`
- `asyncio.Condition`
- `asyncio.Barrier` (3.11+)

---

## When Do You Need Synchronization in asyncio?

asyncio is single-threaded, so you don't have race conditions on CPU
operations. But you DO need synchronization when:

- Multiple tasks read/write shared state with `await` in between
- You want to limit how many tasks access a resource concurrently
- Tasks need to coordinate (wait for a signal, rendezvous point)

---

## 1. asyncio.Lock

Ensures only one task at a time executes a critical section.

### 1.1 Problem without a lock

```python
import asyncio

balance = 100


async def withdraw(amount: float) -> None:
    global balance
    current = balance
    await asyncio.sleep(0.1)  # simulate processing
    # Another task can modify balance during this await!
    balance = current - amount
    print(f"  Withdrew {amount}, balance: {balance}")


async def main() -> None:
    # Both tasks read balance=100, then both write
    await asyncio.gather(withdraw(60), withdraw(60))
    print(f"Final balance: {balance}")  # Should be -20 but might be 40!


if __name__ == "__main__":
    asyncio.run(main())
```

### 1.2 Fixed with a lock

```python
import asyncio

balance = 100
lock = asyncio.Lock()


async def withdraw(amount: float) -> None:
    global balance
    async with lock:  # only one task at a time
        current = balance
        await asyncio.sleep(0.1)
        balance = current - amount
        print(f"  Withdrew {amount}, balance: {balance}")


async def main() -> None:
    await asyncio.gather(withdraw(60), withdraw(60))
    print(f"Final balance: {balance}")  # Correctly -20


if __name__ == "__main__":
    asyncio.run(main())
```

### 1.3 Lock as a decorator pattern

```python
import asyncio
from functools import wraps
from typing import Callable, ParamSpec, TypeVar

P = ParamSpec("P")
T = TypeVar("T")

_lock = asyncio.Lock()


def with_lock(func: Callable[P, T]) -> Callable[P, T]:
    @wraps(func)
    async def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
        async with _lock:
            return await func(*args, **kwargs)
    return wrapper


@with_lock
async def critical_operation(name: str) -> None:
    print(f"  {name} entered critical section")
    await asyncio.sleep(1.0)
    print(f"  {name} leaving critical section")


async def main() -> None:
    await asyncio.gather(
        critical_operation("A"),
        critical_operation("B"),
        critical_operation("C"),
    )


if __name__ == "__main__":
    asyncio.run(main())
```

---

## 2. asyncio.Semaphore / BoundedSemaphore

A semaphore allows up to N tasks to enter a section concurrently.

### 2.1 Rate limiting API calls

```python
import asyncio
import time

sem = asyncio.Semaphore(3)  # max 3 concurrent API calls


async def call_api(i: int) -> str:
    async with sem:
        print(f"  [{time.perf_counter():.1f}] Task {i} calling API...")
        await asyncio.sleep(1.0)  # simulate API call
        print(f"  [{time.perf_counter():.1f}] Task {i} done")
        return f"result-{i}"


async def main() -> None:
    start = time.perf_counter()

    # 9 tasks, but only 3 run at a time
    tasks = [asyncio.create_task(call_api(i)) for i in range(9)]
    results = await asyncio.gather(*tasks)

    elapsed = time.perf_counter() - start
    print(f"\nAll done in {elapsed:.2f}s (9 tasks, 3 at a time = ~3s)")


if __name__ == "__main__":
    asyncio.run(main())
```

### 2.2 Semaphore vs BoundedSemaphore

```python
import asyncio

# Semaphore: release() can increase count above initial value (no error)
sem = asyncio.Semaphore(2)
sem.release()  # count is now 3 -- no error

# BoundedSemaphore: release() raises ValueError if count exceeds initial value
bsem = asyncio.BoundedSemaphore(2)
# bsem.release()  # ValueError: BoundedSemaphore released too many times
```

Use `BoundedSemaphore` to catch bugs where you accidentally release too many times.

---

## 3. asyncio.Event

A simple boolean flag. Tasks can wait for it to be set.

### 3.1 Startup coordination

```python
import asyncio


async def database_ready(event: asyncio.Event) -> None:
    """Simulates database initialization."""
    print("DB: initializing...")
    await asyncio.sleep(2.0)
    print("DB: ready!")
    event.set()


async def web_server(event: asyncio.Event) -> None:
    """Web server waits for DB before accepting requests."""
    print("Server: waiting for database...")
    await event.wait()
    print("Server: database is ready, accepting requests!")
    await asyncio.sleep(1.0)
    print("Server: handled a request")


async def worker(event: asyncio.Event, name: str) -> None:
    """Worker waits for DB before processing jobs."""
    print(f"Worker-{name}: waiting for database...")
    await event.wait()
    print(f"Worker-{name}: processing jobs!")


async def main() -> None:
    db_event = asyncio.Event()

    await asyncio.gather(
        database_ready(db_event),
        web_server(db_event),
        worker(db_event, "1"),
        worker(db_event, "2"),
    )


if __name__ == "__main__":
    asyncio.run(main())
```

### 3.2 Event.clear() for repeated signaling

```python
import asyncio


async def traffic_light(event: asyncio.Event) -> None:
    for _ in range(3):
        event.set()
        print("  GREEN")
        await asyncio.sleep(1.0)
        event.clear()
        print("  RED")
        await asyncio.sleep(1.0)


async def car(event: asyncio.Event, name: str) -> None:
    while True:
        await event.wait()
        print(f"  {name}: driving!")
        await asyncio.sleep(0.5)
        if not event.is_set():
            print(f"  {name}: stopping")
            break


async def main() -> None:
    light = asyncio.Event()
    try:
        async with asyncio.timeout(5.0):
            await asyncio.gather(
                traffic_light(light),
                car(light, "Car-A"),
            )
    except TimeoutError:
        pass


if __name__ == "__main__":
    asyncio.run(main())
```

---

## 4. asyncio.Condition

Combines a `Lock` with the ability to wait for and signal notifications.
Use when tasks need to wait for a specific state change.

### 4.1 Producer-Consumer with Condition

```python
import asyncio

buffer: list[int] = []
MAX_BUFFER = 3
condition = asyncio.Condition()


async def producer(name: str, count: int) -> None:
    for i in range(count):
        async with condition:
            while len(buffer) >= MAX_BUFFER:
                print(f"  [{name}] buffer full, waiting...")
                await condition.wait()

            buffer.append(i)
            print(f"  [{name}] produced {i} | buffer: {buffer}")
            condition.notify_all()

        await asyncio.sleep(0.1)


async def consumer(name: str) -> None:
    consumed = 0
    while consumed < 5:
        async with condition:
            while not buffer:
                print(f"  [{name}] buffer empty, waiting...")
                await condition.wait()

            item = buffer.pop(0)
            consumed += 1
            print(f"  [{name}] consumed {item} | buffer: {buffer}")
            condition.notify_all()

        await asyncio.sleep(0.2)  # simulate processing


async def main() -> None:
    await asyncio.gather(
        producer("P1", 5),
        consumer("C1"),
    )
    print(f"Final buffer: {buffer}")


if __name__ == "__main__":
    asyncio.run(main())
```

### 4.2 Condition.wait_for() shorthand

Instead of `while not condition: await cond.wait()`, use `wait_for`:

```python
import asyncio

data_ready = False
condition = asyncio.Condition()


async def provider() -> None:
    global data_ready
    await asyncio.sleep(1.0)
    async with condition:
        data_ready = True
        print("Provider: data is ready")
        condition.notify_all()


async def consumer(name: str) -> None:
    async with condition:
        # wait_for replaces the while-loop pattern
        await condition.wait_for(lambda: data_ready)
        print(f"{name}: got data!")


async def main() -> None:
    await asyncio.gather(
        provider(),
        consumer("C1"),
        consumer("C2"),
    )


if __name__ == "__main__":
    asyncio.run(main())
```

---

## 5. asyncio.Barrier (3.11+)

`asyncio.Barrier` blocks tasks until a specific number of them have arrived.

```python
import asyncio


async def worker(barrier: asyncio.Barrier, name: str) -> None:
    print(f"  {name}: doing setup work...")
    await asyncio.sleep(0.5)

    print(f"  {name}: waiting at barrier")
    await barrier.wait()

    print(f"  {name}: barrier released, proceeding!")


async def main() -> None:
    barrier = asyncio.Barrier(3)  # wait until 3 tasks arrive

    await asyncio.gather(
        worker(barrier, "A"),
        worker(barrier, "B"),
        worker(barrier, "C"),
    )


if __name__ == "__main__":
    asyncio.run(main())
```

---

## 6. Quick Reference: When to Use Which

| Primitive | Use When... | Example |
|-----------|------------|---------|
| `Lock` | Only 1 task should access a resource | Shared bank balance |
| `Semaphore` | At most N tasks concurrently | Rate-limit API calls |
| `Event` | Tasks wait for a one-time signal | DB ready, config loaded |
| `Condition` | Tasks wait for a state change | Producer-consumer buffer |
| `Barrier` | Tasks must all reach a point before continuing | Phased computation |

---

## 7. Practice Problems

### Problem 1: Rate-limited downloader

Use a `Semaphore(3)` to download 10 URLs concurrently but with at most
3 active downloads at once. Print timing.

```python
import asyncio
import time


async def download(url: str, sem: asyncio.Semaphore) -> str:
    # TODO: acquire semaphore, simulate download, return result
    ...


async def main() -> None:
    urls = [f"http://example.com/file{i}" for i in range(10)]
    sem = asyncio.Semaphore(3)
    start = time.perf_counter()

    # TODO: create tasks, gather results
    ...

    print(f"Total: {time.perf_counter() - start:.2f}s")


if __name__ == "__main__":
    asyncio.run(main())
```

### Problem 2: Multi-phase computation with Barrier

Three workers each compute a partial result. They must all finish phase 1
before starting phase 2.

```python
import asyncio


async def worker(barrier: asyncio.Barrier, name: str) -> None:
    # Phase 1
    print(f"  {name}: phase 1 computing...")
    await asyncio.sleep(1.0)
    print(f"  {name}: phase 1 done, waiting for others")

    await barrier.wait()

    # Phase 2
    print(f"  {name}: phase 2 computing...")
    await asyncio.sleep(0.5)
    print(f"  {name}: phase 2 done")


async def main() -> None:
    # TODO: create barrier and run 3 workers
    ...


if __name__ == "__main__":
    asyncio.run(main())
```
