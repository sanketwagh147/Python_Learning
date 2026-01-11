# Thread States and Lifecycle

Understanding the lifecycle and states of a thread is crucial for effective thread management.

## Thread Lifecycle

```
Created → Started → Running → Finished
```

1. **Created**: Thread object is created but not yet started
2. **Started**: `start()` is called, thread is scheduled to run
3. **Running**: Thread is actively executing its target function
4. **Finished**: Thread has completed execution

## Key Method: `is_alive()`

```python
thread.is_alive()  # Returns True if thread is running, False otherwise
```

## Example 1: Monitoring Thread State

```python
import threading
import time

def worker(duration):
    print(f"Worker started, will run for {duration} seconds")
    time.sleep(duration)
    print("Worker finished")

# Create thread
thread = threading.Thread(target=worker, args=(3,), name="Worker")

# State 1: Created (not started)
print(f"Before start - Is alive? {thread.is_alive()}")

# State 2: Started
thread.start()
print(f"After start - Is alive? {thread.is_alive()}")

# State 3: Running (check periodically)
time.sleep(1)
print(f"During execution - Is alive? {thread.is_alive()}")

# State 4: Wait for completion
thread.join()
print(f"After join - Is alive? {thread.is_alive()}")
```

**Output:**
```
Before start - Is alive? False
Worker started, will run for 3 seconds
After start - Is alive? True
During execution - Is alive? True
Worker finished
After join - Is alive? False
```

## Example 2: Monitoring Multiple Threads

```python
import threading
import time

def task(task_id, duration):
    print(f"Task {task_id} started")
    time.sleep(duration)
    print(f"Task {task_id} completed")

# Create threads with different durations
threads = []
for i in range(3):
    t = threading.Thread(target=task, args=(i+1, (i+1)*2), name=f"Task-{i+1}")
    threads.append(t)
    t.start()

# Monitor thread states
while any(t.is_alive() for t in threads):
    alive_threads = [t.name for t in threads if t.is_alive()]
    print(f"Still running: {', '.join(alive_threads)}")
    time.sleep(1)

print("All threads completed!")
```

**Output:**
```
Task 1 started
Task 2 started
Task 3 started
Still running: Task-1, Task-2, Task-3
Still running: Task-1, Task-2, Task-3
Task 1 completed
Still running: Task-2, Task-3
Still running: Task-2, Task-3
Task 2 completed
Still running: Task-3
Still running: Task-3
Task 3 completed
All threads completed!
```

## Example 3: Thread Timeout with State Checking

```python
import threading
import time

def long_running_task():
    print("Starting long task...")
    time.sleep(10)
    print("Long task completed!")

# Start the thread
thread = threading.Thread(target=long_running_task, name="LongTask")
thread.start()

# Wait with timeout
timeout = 3
print(f"Waiting for thread (timeout: {timeout} seconds)")
thread.join(timeout)

# Check if still running
if thread.is_alive():
    print(f"Thread is still running after {timeout} seconds")
    print("Continuing with other work...")
    # In real scenarios, you might want to handle this
    # (can't force kill threads in Python)
else:
    print("Thread completed within timeout")
```

**Output:**
```
Starting long task...
Waiting for thread (timeout: 3 seconds)
Thread is still running after 3 seconds
Continuing with other work...
Long task completed!
```

## Example 4: Progress Monitor

```python
import threading
import time

class ProgressTask:
    def __init__(self):
        self.progress = 0
        self.running = False
    
    def run(self):
        self.running = True
        for i in range(1, 11):
            time.sleep(0.5)
            self.progress = i * 10
        self.running = False
    
    def get_progress(self):
        return self.progress

# Create and start task
task = ProgressTask()
thread = threading.Thread(target=task.run, name="ProgressTask")
thread.start()

# Monitor progress
while thread.is_alive():
    print(f"Progress: {task.get_progress()}%")
    time.sleep(1)

thread.join()
print(f"Final Progress: {task.get_progress()}%")
print("Task completed!")
```

**Output:**
```
Progress: 0%
Progress: 20%
Progress: 40%
Progress: 60%
Progress: 80%
Final Progress: 100%
Task completed!
```

## Important Notes

### `join()` with Timeout

```python
thread.join(timeout=5)  # Wait up to 5 seconds
if thread.is_alive():
    print("Thread is still running after timeout")
```

### Cannot Restart a Thread

```python
thread = threading.Thread(target=worker)
thread.start()
thread.join()

# This will raise RuntimeError
# thread.start()  # ❌ Cannot start the same thread twice
```

### Multiple `join()` Calls

```python
thread.start()
thread.join()  # ✓ Waits for completion
thread.join()  # ✓ Returns immediately (already finished)
```

## Best Practices

1. **Check `is_alive()` before operations** - Avoid assumptions about thread state
2. **Use timeouts with `join()`** - Prevent indefinite blocking
3. **Don't reuse thread objects** - Create new thread instances for new tasks
4. **Monitor long-running threads** - Implement progress tracking mechanisms
5. **Handle thread failures gracefully** - Check state before assuming success

## Common State Patterns

### Pattern 1: Wait with Timeout
```python
thread.join(timeout=10)
if thread.is_alive():
    # Handle timeout scenario
    pass
```

### Pattern 2: Check Before Join
```python
if thread.is_alive():
    thread.join()
```

### Pattern 3: Periodic State Check
```python
while thread.is_alive():
    # Do periodic work
    time.sleep(1)
```
