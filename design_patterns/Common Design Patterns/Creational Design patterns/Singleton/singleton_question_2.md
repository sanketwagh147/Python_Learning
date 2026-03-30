# Singleton Pattern — Question 2 (Medium)

## Problem: Database Connection Pool (Thread-Safe Singleton)

A web server needs a single connection pool shared across all request-handling threads.

### Requirements

- `ConnectionPool` is a thread-safe singleton.
- Constructor takes `max_connections: int` (only used on first creation).
- Methods:
  - `get_connection() -> Connection` — returns a connection from the pool (or raises if pool exhausted).
  - `release_connection(conn)` — returns a connection to the pool.
  - `active_count() -> int` — number of connections currently checked out.

- `Connection` is a simple class with `id` and `is_active` flag.

### Expected Usage

```python
pool1 = ConnectionPool(max_connections=3)
pool2 = ConnectionPool(max_connections=10)  # ignored — already created with 3
print(pool1 is pool2)  # True

conn1 = pool1.get_connection()
conn2 = pool1.get_connection()
print(pool1.active_count())  # 2

pool1.release_connection(conn1)
print(pool1.active_count())  # 1
```

### Thread Safety Test

```python
import threading

def worker():
    pool = ConnectionPool(5)
    conn = pool.get_connection()
    # ... do work ...
    pool.release_connection(conn)

threads = [threading.Thread(target=worker) for _ in range(10)]
for t in threads:
    t.start()
for t in threads:
    t.join()

# Only ONE pool instance should exist across all threads
```

### Constraints

- Use `threading.Lock` to make `__new__` thread-safe.
- The pool itself should be thread-safe (use a Lock for get/release operations).
- Raise `RuntimeError` if all connections are checked out.

### Think About

- What's the **double-checked locking** pattern and why is it important here?
- What are the downsides of Singleton in testing? How would you mock this pool?
