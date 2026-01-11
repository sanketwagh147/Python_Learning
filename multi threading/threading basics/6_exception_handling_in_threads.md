# Exception Handling in Threads

Understanding how exceptions work in threads is crucial because exceptions in threads behave differently than in single-threaded code.

## Key Differences

1. **Exceptions in threads don't propagate to the main thread**
2. **Unhandled exceptions terminate only that thread, not the program**
3. **Main thread doesn't know if a worker thread raised an exception**
4. **Need explicit mechanisms to capture and handle exceptions**

## Example 1: Basic Exception in Thread (Unhandled)

```python
import threading
import time

def worker_with_error():
    print("Worker started")
    time.sleep(1)
    raise ValueError("Something went wrong in worker!")
    print("This line never executes")

# Create and start thread
thread = threading.Thread(target=worker_with_error)
thread.start()

# Main thread continues
time.sleep(2)
print("Main thread: Did I know about the exception? No!")

thread.join()
print("Main thread: Thread completed (but crashed)")
```

**Output:**
```
Worker started
Exception in thread Thread-1:
Traceback (most recent call last):
  ...
ValueError: Something went wrong in worker!
Main thread: Did I know about the exception? No!
Main thread: Thread completed (but crashed)
```

**Problem**: The exception is printed but not caught or handled by the main thread!

## Example 2: Catching Exception Inside Thread

```python
import threading
import time

def worker_with_handler():
    try:
        print("Worker started")
        time.sleep(1)
        raise ValueError("Error occurred")
    except ValueError as e:
        print(f"Worker caught exception: {e}")
        # Handle the error appropriately
        return None  # Or take other action

thread = threading.Thread(target=worker_with_handler)
thread.start()
thread.join()

print("Main thread: Worker completed cleanly")
```

**Output:**
```
Worker started
Worker caught exception: Error occurred
Main thread: Worker completed cleanly
```

✅ Exception handled inside the thread!

## Example 3: Returning Exception to Main Thread

```python
import threading
import sys

class ThreadWithException(threading.Thread):
    def __init__(self, target):
        super().__init__()
        self.target = target
        self.exception = None
    
    def run(self):
        try:
            self.target()
        except Exception as e:
            self.exception = e
    
    def join(self, timeout=None):
        super().join(timeout)
        if self.exception:
            raise self.exception

def worker_that_fails():
    print("Worker doing work...")
    raise RuntimeError("Worker failed!")

# Create and start thread
thread = ThreadWithException(target=worker_that_fails)
thread.start()

# Join and handle exception
try:
    thread.join()
except RuntimeError as e:
    print(f"Main thread caught: {e}")
```

**Output:**
```
Worker doing work...
Main thread caught: Worker failed!
```

✅ Exception propagated to main thread!

## Example 4: Using Queue to Communicate Exceptions

```python
import threading
import queue
import time

def worker(task_id, result_queue):
    try:
        print(f"Task {task_id} started")
        time.sleep(1)
        
        if task_id == 2:
            raise ValueError(f"Task {task_id} failed!")
        
        result_queue.put((task_id, "success", None))
    except Exception as e:
        result_queue.put((task_id, "error", e))

# Create queue for results
result_queue = queue.Queue()

# Start multiple threads
threads = []
for i in range(4):
    t = threading.Thread(target=worker, args=(i, result_queue))
    threads.append(t)
    t.start()

# Wait for all threads
for t in threads:
    t.join()

# Check results
print("\nResults:")
while not result_queue.empty():
    task_id, status, error = result_queue.get()
    if status == "error":
        print(f"Task {task_id}: ❌ Error - {error}")
    else:
        print(f"Task {task_id}: ✅ Success")
```

**Output:**
```
Task 0 started
Task 1 started
Task 2 started
Task 3 started

Results:
Task 0: ✅ Success
Task 1: ✅ Success
Task 2: ❌ Error - Task 2 failed!
Task 3: ✅ Success
```

## Example 5: Thread Pool with Exception Handling

```python
import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

def task_with_potential_error(task_id):
    print(f"Task {task_id} starting")
    time.sleep(1)
    
    if task_id % 3 == 0:
        raise ValueError(f"Task {task_id} encountered an error!")
    
    return f"Task {task_id} completed successfully"

# Using ThreadPoolExecutor for better exception handling
with ThreadPoolExecutor(max_workers=4) as executor:
    # Submit tasks
    futures = [executor.submit(task_with_potential_error, i) for i in range(6)]
    
    # Process results
    for future in as_completed(futures):
        try:
            result = future.result()  # This will raise exception if task failed
            print(f"✅ {result}")
        except ValueError as e:
            print(f"❌ Exception caught: {e}")
```

**Output:**
```
Task 0 starting
Task 1 starting
Task 2 starting
Task 3 starting
Task 4 starting
Task 5 starting
❌ Exception caught: Task 0 encountered an error!
✅ Task 1 completed successfully
✅ Task 2 completed successfully
❌ Exception caught: Task 3 encountered an error!
✅ Task 4 completed successfully
✅ Task 5 completed successfully
```

## Example 6: Global Exception Hook

```python
import threading
import sys
import time

# Store original exception hook
original_exception_hook = sys.excepthook

def global_exception_handler(exc_type, exc_value, exc_traceback):
    """Custom handler for all exceptions"""
    if threading.current_thread() is threading.main_thread():
        print("Exception in main thread:")
    else:
        print(f"Exception in thread {threading.current_thread().name}:")
    
    print(f"  Type: {exc_type.__name__}")
    print(f"  Message: {exc_value}")
    
    # Call original handler for traceback
    original_exception_hook(exc_type, exc_value, exc_traceback)

# Set global exception hook
sys.excepthook = global_exception_handler

# For Python 3.8+: Set threading exception hook
def threading_exception_handler(args):
    print(f"\n🔥 Thread Exception Handler:")
    print(f"  Thread: {args.thread.name}")
    print(f"  Exception: {args.exc_type.__name__}")
    print(f"  Message: {args.exc_value}")

threading.excepthook = threading_exception_handler

def worker_with_error(name):
    time.sleep(1)
    raise RuntimeError(f"Error in {name}")

# Create threads
threads = []
for i in range(3):
    t = threading.Thread(target=worker_with_error, args=(f"Worker-{i}",), name=f"Thread-{i}")
    threads.append(t)
    t.start()

for t in threads:
    t.join()

print("\nMain thread continues...")
```

**Output (Python 3.8+):**
```
🔥 Thread Exception Handler:
  Thread: Thread-0
  Exception: RuntimeError
  Message: Error in Worker-0

🔥 Thread Exception Handler:
  Thread: Thread-1
  Exception: RuntimeError
  Message: Error in Worker-1

🔥 Thread Exception Handler:
  Thread: Thread-2
  Exception: RuntimeError
  Message: Error in Worker-2

Main thread continues...
```

## Example 7: Retry Pattern with Exception Handling

```python
import threading
import time
import random

def unreliable_operation(task_id):
    """Simulates an operation that might fail"""
    if random.random() < 0.5:
        raise ConnectionError(f"Task {task_id} failed to connect")
    return f"Task {task_id} success"

def worker_with_retry(task_id, max_retries=3):
    """Worker that retries on failure"""
    for attempt in range(max_retries):
        try:
            result = unreliable_operation(task_id)
            print(f"✅ {result} (attempt {attempt + 1})")
            return result
        except ConnectionError as e:
            print(f"⚠️  Attempt {attempt + 1} failed: {e}")
            if attempt < max_retries - 1:
                time.sleep(0.5)  # Wait before retry
            else:
                print(f"❌ Task {task_id} failed after {max_retries} attempts")
                raise

# Create threads with retry logic
threads = []
for i in range(5):
    t = threading.Thread(target=worker_with_retry, args=(i,))
    threads.append(t)
    t.start()

for t in threads:
    t.join()

print("\nAll tasks completed (some may have failed)")
```

## Example 8: Thread-Safe Error Collection

```python
import threading
import time

class ErrorCollector:
    def __init__(self):
        self.errors = []
        self.lock = threading.Lock()
    
    def add_error(self, thread_name, error):
        with self.lock:
            self.errors.append({
                'thread': thread_name,
                'error': str(error),
                'type': type(error).__name__
            })
    
    def get_errors(self):
        with self.lock:
            return self.errors.copy()
    
    def has_errors(self):
        with self.lock:
            return len(self.errors) > 0

def worker(task_id, error_collector):
    try:
        print(f"Task {task_id} running")
        time.sleep(1)
        
        if task_id % 2 == 0:
            raise ValueError(f"Error in task {task_id}")
        
        print(f"Task {task_id} completed")
    except Exception as e:
        error_collector.add_error(threading.current_thread().name, e)

# Create error collector
error_collector = ErrorCollector()

# Start threads
threads = []
for i in range(5):
    t = threading.Thread(target=worker, args=(i, error_collector), name=f"Worker-{i}")
    threads.append(t)
    t.start()

# Wait for all threads
for t in threads:
    t.join()

# Report errors
if error_collector.has_errors():
    print("\n❌ Errors occurred:")
    for error in error_collector.get_errors():
        print(f"  Thread {error['thread']}: {error['type']} - {error['error']}")
else:
    print("\n✅ All tasks completed successfully")
```

## Best Practices

1. **Always handle exceptions inside threads** - Don't rely on propagation
2. **Use try-except in thread target functions** - Catch expected exceptions
3. **Communicate errors to main thread** - Use queues, custom Thread classes, or concurrent.futures
4. **Log exceptions** - Use logging module for thread-safe logging
5. **Set threading.excepthook** - For Python 3.8+ global thread exception handling
6. **Use ThreadPoolExecutor** - Built-in exception handling with futures
7. **Implement retry logic** - For transient errors
8. **Clean up resources** - Use finally blocks even in threads

## Common Patterns

### Pattern 1: Try-Except in Thread
```python
def worker():
    try:
        # Do work
        pass
    except SpecificException as e:
        # Handle error
        pass
```

### Pattern 2: Queue for Error Reporting
```python
def worker(error_queue):
    try:
        # Do work
        pass
    except Exception as e:
        error_queue.put(e)
```

### Pattern 3: Custom Thread Class
```python
class SafeThread(threading.Thread):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.exception = None
    
    def run(self):
        try:
            super().run()
        except Exception as e:
            self.exception = e
```

## Summary

- **Exceptions don't propagate** from threads to main thread automatically
- **Handle exceptions inside threads** with try-except blocks
- **Use queues or custom Thread classes** to communicate errors
- **ThreadPoolExecutor provides better exception handling** than raw threads
- **Python 3.8+ has `threading.excepthook`** for global thread exception handling
- **Always clean up resources** even when exceptions occur (use finally)
- **Log exceptions** for debugging multithreaded applications
