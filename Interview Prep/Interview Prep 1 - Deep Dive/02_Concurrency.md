# 02. Concurrency & Parallelism

## 🔄 The Big Three: Overview

| Model | Module | Best For | Mechanism |
| :--- | :--- | :--- | :--- |
| **Multithreading** | `threading` | I/O Bound tasks (Network, Disk) | Pre-emptive switching by OS (limited by GIL) |
| **Multiprocessing** | `multiprocessing` | CPU Bound tasks (Computation) | Separate memory space, True parallelism |
| **Async IO** | `asyncio` | High concurrency I/O (Web servers) | Cooperative multitasking (Event loop) |

---

## 🧵 1. Multithreading (Deep Dive)

### Core Concept
Threads exist within a single process. They share the same memory space. In Python (CPython), only one thread can execute Python bytecode at a time due to the **GIL**. However, the GIL is released during I/O operations (sleep, read, write, waiting for network), making threading useful for I/O bound tasks.

### Synchronization Primitives
Race conditions occur when threads access shared data simultaneously.
- **Lock (Mutex):** Ensures only one thread accesses a block of code.
- **RLock (Reentrant Lock):** A thread can acquire the same lock multiple times without blocking itself.
- **Semaphore:** Allows a fixed number of threads to access a resource (e.g., limit DB connections).
- **Event:** Simple communication. One thread signals an event; others wait for it.

```python
import threading

lock = threading.Lock()
shared_counter = 0

def increment():
    global shared_counter
    with lock:  # Context manager acquires/releases lock
        shared_counter += 1
```

### Daemon Threads
- **Daemon:** Background thread that dies automatically when the main program exits (e.g., Log collection, heartbeat).
- **Non-Daemon:** The program waits for these threads to finish before exiting.

---

## ⚙️ 2. Multiprocessing (Deep Dive)

### Core Concept
Spawns new OS processes. Each process has its own Python interpreter and memory space.
- **Pros:** Bypasses GIL. True parallelism on multi-core CPUs.
- **Cons:** High overhead to create processes. Harder to share data.

### Inter-Process Communication (IPC)
Since memory isn't shared, you need special mechanisms:
- **Queue:** Thread/Process safe FIFO queue.
- **Pipe:** Two-way connection between two processes.
- **Value/Array:** Shared memory maps (faster but riskier).

### Process Pool (`Pool`)
Best for "Data Parallelism" (applying a function to a list of items).
```python
from multiprocessing import Pool

def square(x):
    return x * x

if __name__ == '__main__':
    with Pool(processes=4) as pool:
        print(pool.map(square, [1, 2, 3, 4, 5]))
```

---

## ⚡ 3. Asyncio (Deep Dive)

### Core Concept
**Cooperative Multitasking.** Single-threaded. Code yields control explicitly (`await`) when waiting for I/O.
- **Event Loop:** The central scheduler that executes tasks.
- **Coroutine:** A function defined with `async def`. It can be paused and resumed.
- **Task:** A wrapper for a coroutine to schedule it in the event loop.

### Key Syntax
- `async def`: Defines a native coroutine.
- `await`: Pauses execution until the awaitable (Future/Task) completes.
- `asyncio.gather()`: Run multiple things concurrently.

### When to use Asyncio?
- High-concurrency network applications (WebSockets, Chat servers, API aggregators).
- 10,000+ connections handling.

```python
import asyncio

async def fetch_data(id):
    print(f"Start {id}")
    await asyncio.sleep(1) # Simulates I/O
    print(f"End {id}")
    return {"id": id}

async def main():
    # Run 3 fetches concurrently
    results = await asyncio.gather(fetch_data(1), fetch_data(2), fetch_data(3))
    print(results)

# asyncio.run(main())
```

---

## 🔧 4. `concurrent.futures` Module (Deep Dive)

### Core Concept
A high-level interface for asynchronously executing callables using threads or processes.
- **ThreadPoolExecutor:** For I/O-bound tasks.
- **ProcessPoolExecutor:** For CPU-bound tasks.

### Key API
```python
from concurrent.futures import ThreadPoolExecutor, as_completed

def fetch_url(url):
    return f"Fetched {url}"

urls = ["url1", "url2", "url3"]

with ThreadPoolExecutor(max_workers=5) as executor:
    future_to_url = {executor.submit(fetch_url, url): url for url in urls}
    
    for future in as_completed(future_to_url):
        url = future_to_url[future]
        try:
            data = future.result()
            print(data)
        except Exception as exc:
            print(f'{url} generated an exception: {exc}')
```

### `executor.map()` vs `executor.submit()`
- **`map(fn, iterable)`:** Returns results in order. Raises exception on first failure.
- **`submit(fn, *args)`:** Returns `Future` objects. More control over individual tasks.

---

## ❓ Interview Questions & Answers

**Q1: What is a Race Condition?**
> **A:** A situation where the system's behavior depends on the uncontrolled timing or ordering of events (e.g., two threads trying to update a bank balance simultaneously).

**Q2: Why can't we just use Multiprocessing for everything?**
> **A:** Creating processes is expensive (memory + CPU overhead). IPC is complex. For simple I/O tasks, threading or asyncio is much lighter.

**Q3: How do you handle exceptions in Asyncio?**
> **A:** Standard `try/except` blocks inside coroutines work. `asyncio.gather()` has a `return_exceptions=True` flag to prevent one failure from crashing all tasks.

**Q4: What happens if a CPU-bound task is run in an asyncio loop?**
> **A:** It blocks the loop. No other async task can run until it finishes. **Solution:** Run the CPU task in a separate thread/process using `loop.run_in_executor()`.

**Q5: Can you mix threads and asyncio?**
> **A:** Yes, but be careful. Asyncio is not thread-safe. You typically run the event loop in the main thread and offload blocking legacy code to a thread pool executor.

---

## 🔗 Recommended Resources

- **Article:** [Real Python: Async IO in Python: A Complete Walkthrough](https://realpython.com/async-io-python/)
- **Documentation:** [Python Standard Library: Concurrent Execution](https://docs.python.org/3/library/concurrency.html)
- **Discussion:** [SuperFastPython - Concurrency focus](https://superfastpython.com/)
