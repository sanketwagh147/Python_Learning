# Thread Naming & Identification

Understanding how to name and identify threads is essential for debugging and managing multiple threads in your application.

## Key Concepts

- **Thread Name**: Every thread has a name that can be set for identification
- **Current Thread**: Get reference to the currently executing thread
- **Thread ID**: Each thread has a unique identifier

## Methods

```python
threading.current_thread()  # Get current thread object
thread.name                  # Get or set thread name
thread.ident                 # Get thread identifier (assigned when started)
threading.active_count()     # Get number of active threads
threading.enumerate()        # Get list of all active thread objects
```

## Example 1: Basic Thread Naming

```python
import threading
import time

def worker():
    current = threading.current_thread()
    print(f"Thread Name: {current.name}")
    print(f"Thread ID: {current.ident}")
    time.sleep(2)
    print(f"{current.name} finished")

# Create threads with custom names
thread1 = threading.Thread(target=worker, name="Worker-1")
thread2 = threading.Thread(target=worker, name="Worker-2")

thread1.start()
thread2.start()

thread1.join()
thread2.join()
```

**Output:**
```
Thread Name: Worker-1
Thread ID: 123145512345600
Thread Name: Worker-2
Thread ID: 123145517608960
Worker-1 finished
Worker-2 finished
```

## Example 2: Listing All Active Threads

```python
import threading
import time

def task(duration):
    time.sleep(duration)

# Main thread info
print(f"Main thread: {threading.current_thread().name}")
print(f"Active threads at start: {threading.active_count()}\n")

# Create multiple threads
threads = []
for i in range(3):
    t = threading.Thread(target=task, args=(2,), name=f"Task-{i+1}")
    threads.append(t)
    t.start()

# List all active threads
print("Active threads:")
for thread in threading.enumerate():
    print(f"  - {thread.name} (ID: {thread.ident})")

print(f"\nTotal active threads: {threading.active_count()}")

# Wait for all threads to complete
for t in threads:
    t.join()

print(f"\nActive threads after completion: {threading.active_count()}")
```

**Output:**
```
Main thread: MainThread
Active threads at start: 1

Active threads:
  - MainThread (ID: 4543021568)
  - Task-1 (ID: 123145512345600)
  - Task-2 (ID: 123145517608960)
  - Task-3 (ID: 123145522872320)

Total active threads: 4

Active threads after completion: 1
```

## Example 3: Dynamic Thread Naming

```python
import threading
import time

class DatabaseWorker:
    def __init__(self, db_name):
        self.db_name = db_name
    
    def process(self):
        current = threading.current_thread()
        print(f"[{current.name}] Connecting to {self.db_name}")
        time.sleep(1)
        print(f"[{current.name}] Processing data from {self.db_name}")
        time.sleep(1)
        print(f"[{current.name}] Completed {self.db_name}")

# Create worker threads for different databases
databases = ["UserDB", "ProductDB", "OrderDB"]
threads = []

for db in databases:
    worker = DatabaseWorker(db)
    thread = threading.Thread(
        target=worker.process,
        name=f"DBThread-{db}"
    )
    threads.append(thread)
    thread.start()

for thread in threads:
    thread.join()

print("All database operations completed")
```

**Output:**
```
[DBThread-UserDB] Connecting to UserDB
[DBThread-ProductDB] Connecting to ProductDB
[DBThread-OrderDB] Connecting to OrderDB
[DBThread-UserDB] Processing data from UserDB
[DBThread-ProductDB] Processing data from ProductDB
[DBThread-OrderDB] Processing data from OrderDB
[DBThread-UserDB] Completed UserDB
[DBThread-ProductDB] Completed ProductDB
[DBThread-OrderDB] Completed OrderDB
All database operations completed
```

## Best Practices

1. **Always name your threads** - Makes debugging much easier
2. **Use descriptive names** - Indicate what the thread does (e.g., "FileWriter", "NetworkHandler")
3. **Include identifiers** - Add numbers or IDs when creating multiple similar threads
4. **Log thread names** - Include thread names in log messages for traceability

## Common Pitfalls

- Thread names are not required to be unique (but should be for clarity)
- Thread ID (`ident`) is `None` until the thread is started
- Default thread names are like "Thread-1", "Thread-2", etc. if not specified
