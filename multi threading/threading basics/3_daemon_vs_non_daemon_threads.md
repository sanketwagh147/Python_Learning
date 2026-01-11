# Daemon vs Non-Daemon Threads

Understanding the difference between daemon and non-daemon threads is crucial for proper application shutdown behavior.

## Key Differences

| Feature | Non-Daemon Thread | Daemon Thread |
|---------|------------------|---------------|
| Program Exit | Blocks program exit until complete | Does not block program exit |
| Default | Yes (daemon=False) | No (daemon=True) |
| Use Case | Critical tasks that must complete | Background services/monitoring |
| Setting | `daemon=False` or default | `daemon=True` |

## When to Use Each

### Non-Daemon Threads (daemon=False)
- **Critical operations** that must complete
- **Data processing** tasks
- **File I/O** operations
- **Database transactions**
- Any task where incomplete execution could cause data loss

### Daemon Threads (daemon=True)
- **Background monitoring**
- **Logging services**
- **Periodic cleanup tasks**
- **Health checks**
- Any task that can be safely interrupted

## Example 1: Basic Daemon vs Non-Daemon

```python
import threading
import time

def critical_task(name):
    """This task must complete"""
    print(f"{name} started (critical)")
    time.sleep(3)
    print(f"{name} completed (critical)")

def background_task(name):
    """This task can be interrupted"""
    print(f"{name} started (background)")
    time.sleep(3)
    print(f"{name} completed (background)")

# Non-daemon thread (must complete)
thread1 = threading.Thread(target=critical_task, args=("Task-1",), daemon=False)

# Daemon thread (can be interrupted)
thread2 = threading.Thread(target=background_task, args=("Task-2",), daemon=True)

thread1.start()
thread2.start()

print("Main thread finishing...")
# Program will wait for thread1 but not thread2
```

**Output:**
```
Task-1 started (critical)
Task-2 started (background)
Main thread finishing...
Task-1 completed (critical)
```
Note: Task-2 completion message may not print because the daemon thread is killed when main exits.

## Example 2: File Writing (Non-Daemon)

```python
import threading
import time

def write_important_data():
    """Critical: Must complete to avoid data loss"""
    print("Starting to write important data...")
    time.sleep(2)
    # Simulating file write
    with open("important_data.txt", "w") as f:
        f.write("Critical data that must be saved")
    print("Data written successfully!")

def monitor_system():
    """Non-critical: Can be interrupted"""
    print("System monitor started...")
    while True:
        print("Monitoring system...")
        time.sleep(1)

# Non-daemon: Must complete
writer_thread = threading.Thread(target=write_important_data, daemon=False)

# Daemon: Can be interrupted
monitor_thread = threading.Thread(target=monitor_system, daemon=True)

writer_thread.start()
monitor_thread.start()

time.sleep(1)
print("Main thread exiting...")
# Will wait for writer_thread but not monitor_thread
```

**Output:**
```
Starting to write important data...
System monitor started...
Monitoring system...
Main thread exiting...
Monitoring system...
Data written successfully!
```

## Example 3: Explicit Join for Daemon Thread

```python
import threading
import time

def daemon_worker():
    print("Daemon worker started")
    time.sleep(3)
    print("Daemon worker completed")

# Create daemon thread
thread = threading.Thread(target=daemon_worker, daemon=True)
thread.start()

print("Waiting for daemon thread...")
thread.join()  # Explicitly wait for daemon thread
print("Main thread exiting")
```

**Output:**
```
Daemon worker started
Waiting for daemon thread...
Daemon worker completed
Main thread exiting
```
Note: Even daemon threads can be waited for with `join()`.

## Example 4: Background Service Pattern

```python
import threading
import time
import random

class BackgroundLogger:
    def __init__(self):
        self.running = True
        self.log_count = 0
    
    def log_service(self):
        """Background logging service (daemon)"""
        while self.running:
            self.log_count += 1
            print(f"[LOG #{self.log_count}] System check at {time.time():.2f}")
            time.sleep(2)

def main_work():
    """Main application work (non-daemon)"""
    print("Main work started")
    for i in range(3):
        print(f"Processing item {i+1}")
        time.sleep(1.5)
    print("Main work completed")

# Create logger service as daemon
logger = BackgroundLogger()
logger_thread = threading.Thread(target=logger.log_service, daemon=True)
logger_thread.start()

# Create main work as non-daemon
work_thread = threading.Thread(target=main_work, daemon=False)
work_thread.start()

work_thread.join()
print("Application shutting down...")
# Logger daemon will be automatically killed
```

**Output:**
```
Main work started
[LOG #1] System check at 1704992000.12
Processing item 1
[LOG #2] System check at 1704992002.12
Processing item 2
[LOG #3] System check at 1704992004.12
Processing item 3
Main work completed
Application shutting down...
```

## Example 5: Setting Daemon Status

```python
import threading
import time

def worker():
    current = threading.current_thread()
    print(f"Thread: {current.name}, Daemon: {current.daemon}")
    time.sleep(2)

# Method 1: Set via constructor
thread1 = threading.Thread(target=worker, name="Thread-1", daemon=True)

# Method 2: Set via property (before start())
thread2 = threading.Thread(target=worker, name="Thread-2")
thread2.daemon = True  # Must be set before start()

# Method 3: Default (non-daemon)
thread3 = threading.Thread(target=worker, name="Thread-3")

print("Starting threads...")
thread1.start()
thread2.start()
thread3.start()

time.sleep(1)
print("Main thread exiting...")
# Only thread3 will block program exit
```

**Output:**
```
Starting threads...
Thread: Thread-1, Daemon: True
Thread: Thread-2, Daemon: True
Thread: Thread-3, Daemon: False
Main thread exiting...
```

## Important Rules

### Cannot Change Daemon Status After Start

```python
thread = threading.Thread(target=worker)
thread.start()
# thread.daemon = True  # ❌ RuntimeError: cannot set daemon status of active thread
```

### Daemon Threads Cannot Create Non-Daemon Threads

```python
def daemon_creator():
    # This will create a daemon thread by default (inherits from parent)
    child = threading.Thread(target=some_function)
    child.start()

daemon_thread = threading.Thread(target=daemon_creator, daemon=True)
daemon_thread.start()
# child thread will also be daemon by default
```

### Check Daemon Status

```python
thread = threading.Thread(target=worker, daemon=True)
print(f"Is daemon: {thread.daemon}")  # True
print(f"Is daemon: {thread.isDaemon()}")  # True (older method)
```

## Best Practices

1. **Use non-daemon for critical operations** - Prevent data loss or corruption
2. **Use daemon for services** - Background tasks that can be safely interrupted
3. **Set daemon before start()** - Cannot change after thread starts
4. **Explicitly join when needed** - Even daemon threads can be waited for
5. **Document your choice** - Make it clear why a thread is daemon or not
6. **Default is non-daemon** - Safer default for most use cases

## Common Patterns

### Pattern 1: Service with Graceful Shutdown
```python
class Service:
    def __init__(self):
        self.running = True
        self.thread = threading.Thread(target=self.run, daemon=True)
    
    def start(self):
        self.thread.start()
    
    def stop(self):
        self.running = False
        self.thread.join()  # Wait even though it's daemon
    
    def run(self):
        while self.running:
            # Do work
            pass
```

### Pattern 2: Critical Task with Timeout
```python
thread = threading.Thread(target=critical_task, daemon=False)
thread.start()
thread.join(timeout=10)
if thread.is_alive():
    print("Warning: Critical task still running!")
```

## Summary

- **Non-daemon threads**: Program waits for them to complete before exiting
- **Daemon threads**: Program can exit while they're still running
- **Default**: Non-daemon (safer)
- **Setting**: Must be done before `start()`
- **Use case**: Daemon for background services, non-daemon for critical tasks
