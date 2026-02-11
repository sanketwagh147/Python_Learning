# asyncio Queues and Backpressure

Covers:
- `asyncio.Queue`
- `asyncio.PriorityQueue`
- `asyncio.LifoQueue`
- Backpressure patterns
- Graceful shutdown

---

## 1. asyncio.Queue (FIFO)

The most common async queue. Supports `put()`, `get()`, `task_done()`, and `join()`.

### 1.1 Simple producer-consumer

```python
import asyncio
import time


async def producer(queue: asyncio.Queue, items: list[str]) -> None:
    for item in items:
        await asyncio.sleep(0.2)  # simulate producing work
        await queue.put(item)
        print(f"  [producer] put: {item} | queue size: {queue.qsize()}")

    # Signal end-of-data
    await queue.put(None)


async def consumer(queue: asyncio.Queue, name: str) -> None:
    while True:
        item = await queue.get()
        if item is None:
            queue.task_done()
            print(f"  [{name}] received stop signal")
            break

        print(f"  [{name}] processing: {item}")
        await asyncio.sleep(0.5)  # simulate work
        queue.task_done()
        print(f"  [{name}] done: {item}")


async def main() -> None:
    queue: asyncio.Queue[str | None] = asyncio.Queue()
    items = ["task-A", "task-B", "task-C", "task-D"]

    start = time.perf_counter()

    await asyncio.gather(
        producer(queue, items),
        consumer(queue, "worker-1"),
    )

    elapsed = time.perf_counter() - start
    print(f"\nDone in {elapsed:.2f}s")


if __name__ == "__main__":
    asyncio.run(main())
```

### 1.2 Understanding task_done() and join()

- Call `queue.task_done()` after you finish processing each item from `get()`
- `await queue.join()` blocks until every `put()` has a matching `task_done()`
- This lets the producer know all items have been fully processed

```python
import asyncio


async def producer(queue: asyncio.Queue) -> None:
    for i in range(5):
        await queue.put(i)
        print(f"  produced {i}")


async def consumer(queue: asyncio.Queue) -> None:
    while True:
        item = await queue.get()
        await asyncio.sleep(0.3)
        print(f"  consumed {item}")
        queue.task_done()


async def main() -> None:
    queue: asyncio.Queue[int] = asyncio.Queue()

    # Start consumer as a background task
    consumer_task = asyncio.create_task(consumer(queue))

    # Produce items
    await producer(queue)

    # Wait until all items are processed
    await queue.join()
    print("All items processed!")

    # Cancel the consumer (it's stuck waiting on get())
    consumer_task.cancel()


if __name__ == "__main__":
    asyncio.run(main())
```

---

## 2. Backpressure with maxsize

Without `maxsize`, a fast producer can flood memory. Setting `maxsize`
makes `put()` block when the queue is full, naturally slowing the producer.

```python
import asyncio
import time


async def fast_producer(queue: asyncio.Queue) -> None:
    for i in range(10):
        await queue.put(i)
        print(f"  [{time.perf_counter():.1f}] produced {i} | qsize: {queue.qsize()}")


async def slow_consumer(queue: asyncio.Queue) -> None:
    while True:
        item = await queue.get()
        await asyncio.sleep(0.5)  # slow processing
        print(f"  [{time.perf_counter():.1f}] consumed {item}")
        queue.task_done()


async def main() -> None:
    # Only 3 items can be in the queue at a time
    queue: asyncio.Queue[int] = asyncio.Queue(maxsize=3)

    consumer_task = asyncio.create_task(slow_consumer(queue))
    await fast_producer(queue)    # blocks when queue is full
    await queue.join()
    consumer_task.cancel()
    print("Done! Producer was slowed by backpressure.")


if __name__ == "__main__":
    asyncio.run(main())
```

---

## 3. Multiple Consumers (Worker Pool Pattern)

Scale throughput by adding more consumers:

```python
import asyncio
import random
import time


async def producer(queue: asyncio.Queue, num_items: int) -> None:
    for i in range(num_items):
        delay = random.uniform(0.1, 0.3)
        await asyncio.sleep(delay)
        await queue.put(f"item-{i}")
        print(f"  [producer] put item-{i}")


async def worker(queue: asyncio.Queue, name: str) -> None:
    while True:
        item = await queue.get()
        work_time = random.uniform(0.3, 1.0)
        print(f"  [{name}] processing {item} ({work_time:.2f}s)")
        await asyncio.sleep(work_time)
        print(f"  [{name}] done {item}")
        queue.task_done()


async def main() -> None:
    queue: asyncio.Queue[str] = asyncio.Queue(maxsize=5)
    num_workers = 3
    num_items = 10

    start = time.perf_counter()

    # Create workers
    workers = [asyncio.create_task(worker(queue, f"W{i}")) for i in range(num_workers)]

    # Produce all items
    await producer(queue, num_items)

    # Wait for all items to be processed
    await queue.join()

    # Cancel workers (they're waiting on get())
    for w in workers:
        w.cancel()

    elapsed = time.perf_counter() - start
    print(f"\n{num_items} items processed by {num_workers} workers in {elapsed:.2f}s")


if __name__ == "__main__":
    asyncio.run(main())
```

---

## 4. asyncio.PriorityQueue

Items are retrieved in priority order (lowest number = highest priority).

```python
import asyncio
from dataclasses import dataclass, field


@dataclass(order=True)
class PrioritizedTask:
    priority: int
    name: str = field(compare=False)
    data: dict = field(compare=False, default_factory=dict)


async def producer(queue: asyncio.PriorityQueue) -> None:
    tasks = [
        PrioritizedTask(priority=3, name="low-priority-backup"),
        PrioritizedTask(priority=1, name="critical-alert"),
        PrioritizedTask(priority=2, name="normal-log"),
        PrioritizedTask(priority=1, name="critical-payment"),
    ]

    for task in tasks:
        await queue.put(task)
        print(f"  [producer] queued: {task.name} (priority={task.priority})")


async def consumer(queue: asyncio.PriorityQueue) -> None:
    while not queue.empty():
        task = await queue.get()
        print(f"  [consumer] processing: {task.name} (priority={task.priority})")
        await asyncio.sleep(0.3)
        queue.task_done()


async def main() -> None:
    queue: asyncio.PriorityQueue = asyncio.PriorityQueue()

    await producer(queue)
    print("\nProcessing in priority order:")
    await consumer(queue)


if __name__ == "__main__":
    asyncio.run(main())
```

**Output order:**
```
Processing in priority order:
  [consumer] processing: critical-alert (priority=1)
  [consumer] processing: critical-payment (priority=1)
  [consumer] processing: normal-log (priority=2)
  [consumer] processing: low-priority-backup (priority=3)
```

---

## 5. asyncio.LifoQueue (Stack)

Last-in, first-out. Useful for processing the most recent items first.

```python
import asyncio


async def main() -> None:
    stack: asyncio.LifoQueue[str] = asyncio.LifoQueue()

    # Push items
    for item in ["old-1", "old-2", "recent-3", "latest-4"]:
        await stack.put(item)
        print(f"  pushed: {item}")

    print("\nPopping (LIFO order):")
    while not stack.empty():
        item = await stack.get()
        print(f"  popped: {item}")
        stack.task_done()


if __name__ == "__main__":
    asyncio.run(main())
```

**Output:**
```
  pushed: old-1
  pushed: old-2
  pushed: recent-3
  pushed: latest-4

Popping (LIFO order):
  popped: latest-4
  popped: recent-3
  popped: old-2
  popped: old-1
```

---

## 6. Graceful Shutdown Pattern

A robust pattern for shutting down producers and consumers cleanly:

```python
import asyncio


async def producer(queue: asyncio.Queue, shutdown: asyncio.Event) -> None:
    i = 0
    while not shutdown.is_set():
        await queue.put(f"item-{i}")
        print(f"  [producer] put item-{i}")
        i += 1
        await asyncio.sleep(0.3)

    print("  [producer] shutting down")


async def consumer(queue: asyncio.Queue, name: str, shutdown: asyncio.Event) -> None:
    while True:
        try:
            item = await asyncio.wait_for(queue.get(), timeout=1.0)
        except asyncio.TimeoutError:
            if shutdown.is_set():
                print(f"  [{name}] shutting down")
                break
            continue

        print(f"  [{name}] processing {item}")
        await asyncio.sleep(0.5)
        queue.task_done()


async def main() -> None:
    queue: asyncio.Queue[str] = asyncio.Queue(maxsize=5)
    shutdown = asyncio.Event()

    # Simulate shutdown after 3 seconds
    async def trigger_shutdown():
        await asyncio.sleep(3.0)
        print("\n--- Shutdown signal received ---")
        shutdown.set()

    await asyncio.gather(
        producer(queue, shutdown),
        consumer(queue, "W1", shutdown),
        consumer(queue, "W2", shutdown),
        trigger_shutdown(),
    )

    await queue.join()
    print("All done!")


if __name__ == "__main__":
    asyncio.run(main())
```

---

## 7. Quick Reference

| Queue Type | Order | Use Case |
|-----------|-------|----------|
| `Queue` | FIFO | General task distribution |
| `PriorityQueue` | By priority | Alert systems, job schedulers |
| `LifoQueue` | LIFO (stack) | Process most recent items first |

| Parameter | Purpose |
|-----------|---------|
| `maxsize=N` | Apply backpressure; block `put()` when full |
| `task_done()` | Signal that a `get()`-ed item is fully processed |
| `join()` | Wait until all items are processed |
| `qsize()` | Current number of items in the queue |

---

## 8. Practice Problems

### Problem 1: Worker pool with stats

Create a system with 1 producer and 3 consumers. Track and print:
- How many items each consumer processed
- Average processing time per consumer
- Total elapsed time

```python
import asyncio
import random
import time


async def producer(queue: asyncio.Queue, count: int) -> None:
    for i in range(count):
        await queue.put(i)
    print(f"Producer done: {count} items queued")


async def worker(queue: asyncio.Queue, name: str, stats: dict) -> None:
    # TODO: process items, track count and total time in stats dict
    ...


async def main() -> None:
    queue: asyncio.Queue[int] = asyncio.Queue(maxsize=5)
    stats: dict[str, dict] = {}
    num_items = 20

    # TODO: create producer and 3 workers, gather, print stats
    ...


if __name__ == "__main__":
    asyncio.run(main())
```

### Problem 2: Priority retry queue

Failed API calls go back into a `PriorityQueue` with higher priority.
Successful calls are printed.

```python
import asyncio
import random


async def unreliable_api(item: str) -> str:
    if random.random() < 0.4:
        raise ConnectionError(f"Failed: {item}")
    await asyncio.sleep(0.3)
    return f"Success: {item}"


async def worker(queue: asyncio.PriorityQueue, name: str) -> None:
    # TODO: get items, call API, re-queue failures with higher priority
    ...


async def main() -> None:
    queue: asyncio.PriorityQueue = asyncio.PriorityQueue()
    items = ["req-A", "req-B", "req-C", "req-D"]

    # Initial priority = 5 (low)
    for item in items:
        await queue.put((5, item))

    # TODO: run workers until queue is empty
    ...


if __name__ == "__main__":
    asyncio.run(main())
```
