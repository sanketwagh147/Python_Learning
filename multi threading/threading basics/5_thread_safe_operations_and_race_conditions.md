# Thread-Safe Operations and Race Conditions

Understanding which operations are thread-safe and which are not is crucial for writing correct multithreaded code.

## What is Thread Safety?

An operation or data structure is **thread-safe** if it can be safely used by multiple threads simultaneously without causing data corruption or unexpected behavior.

## Atomic Operations in Python

Thanks to the Global Interpreter Lock (GIL), some operations in Python are atomic (indivisible):

### Thread-Safe (Atomic) Operations
```python
# Simple assignments
x = 5                    # ✅ Atomic
x = []                   # ✅ Atomic
x = {}                   # ✅ Atomic

# Simple reads
y = x                    # ✅ Atomic

# List operations
list.append(item)        # ✅ Atomic
list.pop()               # ✅ Atomic (with no index)

# Dict operations
dict[key] = value        # ✅ Atomic
x = dict[key]            # ✅ Atomic
dict.get(key)            # ✅ Atomic
```

### NOT Thread-Safe Operations
```python
# Read-modify-write
x += 1                   # ❌ Not atomic (read, add, write)
x -= 1                   # ❌ Not atomic
counter += 1             # ❌ Not atomic

# Complex operations
list.extend([1, 2, 3])   # ❌ Not atomic
dict.update(other_dict)  # ❌ Not atomic

# Multiple operations
if key in dict:          # ❌ Race condition (check-then-act)
    dict[key] += 1
```

## Example 1: Demonstrating Race Condition

```python
import threading

counter = 0

def increment_unsafe():
    global counter
    for _ in range(100000):
        counter += 1  # Read-Modify-Write: NOT atomic!

threads = []
for _ in range(10):
    t = threading.Thread(target=increment_unsafe)
    threads.append(t)
    t.start()

for t in threads:
    t.join()

print(f"Counter: {counter} (Expected: 1000000)")
```

**Output (varies):**
```
Counter: 742891 (Expected: 1000000)
```

**Why?** The operation `counter += 1` is actually three operations:
1. Read current value of counter
2. Add 1 to that value
3. Write the new value back

Multiple threads can interleave these steps, causing lost updates.

## Example 2: List Append (Thread-Safe)

```python
import threading

shared_list = []

def append_to_list(thread_id):
    for i in range(1000):
        shared_list.append(f"T{thread_id}-{i}")  # ✅ append() is atomic

threads = []
for i in range(10):
    t = threading.Thread(target=append_to_list, args=(i,))
    threads.append(t)
    t.start()

for t in threads:
    t.join()

print(f"List length: {len(shared_list)}")
print(f"Expected: {10 * 1000}")
```

**Output:**
```
List length: 10000
Expected: 10000
```
✅ Works correctly because `list.append()` is atomic!

## Example 3: Dictionary Assignment (Thread-Safe)

```python
import threading

shared_dict = {}

def add_to_dict(thread_id):
    for i in range(1000):
        key = f"T{thread_id}-{i}"
        shared_dict[key] = i  # ✅ Dict assignment is atomic

threads = []
for i in range(10):
    t = threading.Thread(target=add_to_dict, args=(i,))
    threads.append(t)
    t.start()

for t in threads:
    t.join()

print(f"Dictionary size: {len(shared_dict)}")
print(f"Expected: {10 * 1000}")
```

**Output:**
```
Dictionary size: 10000
Expected: 10000
```
✅ Works correctly because dict assignment is atomic!

## Example 4: Check-Then-Act Race Condition

```python
import threading
import time

shared_dict = {}

def update_dict_unsafe(key):
    # Check-then-act: NOT thread-safe!
    if key in shared_dict:  # Check
        time.sleep(0.0001)  # Simulate delay
        shared_dict[key] += 1  # Act
    else:
        shared_dict[key] = 1

# Multiple threads updating same key
threads = []
for _ in range(100):
    t = threading.Thread(target=update_dict_unsafe, args=("counter",))
    threads.append(t)
    t.start()

for t in threads:
    t.join()

print(f"Counter value: {shared_dict.get('counter', 0)}")
print(f"Expected: 100")
```

**Output (varies):**
```
Counter value: 87
Expected: 100
```
❌ Race condition between check and act!

## Example 5: Fixed with Lock

```python
import threading

shared_dict = {}
lock = threading.Lock()

def update_dict_safe(key):
    with lock:
        if key in shared_dict:
            shared_dict[key] += 1
        else:
            shared_dict[key] = 1

threads = []
for _ in range(100):
    t = threading.Thread(target=update_dict_safe, args=("counter",))
    threads.append(t)
    t.start()

for t in threads:
    t.join()

print(f"Counter value: {shared_dict.get('counter', 0)}")
print(f"Expected: 100")
```

**Output:**
```
Counter value: 100
Expected: 100
```
✅ Fixed with lock!

## Example 6: Thread-Safe Counter Class

```python
import threading

class ThreadSafeCounter:
    def __init__(self):
        self._value = 0
        self._lock = threading.Lock()
    
    def increment(self):
        with self._lock:
            self._value += 1
    
    def decrement(self):
        with self._lock:
            self._value -= 1
    
    def get_value(self):
        with self._lock:
            return self._value

# Usage
counter = ThreadSafeCounter()

def worker():
    for _ in range(10000):
        counter.increment()

threads = []
for _ in range(10):
    t = threading.Thread(target=worker)
    threads.append(t)
    t.start()

for t in threads:
    t.join()

print(f"Final counter: {counter.get_value()}")
print(f"Expected: 100000")
```

**Output:**
```
Final counter: 100000
Expected: 100000
```

## Example 7: Thread-Safe vs Unsafe List Operations

```python
import threading

# Unsafe: list.extend() is NOT atomic
shared_list_unsafe = []

def extend_unsafe():
    for _ in range(1000):
        shared_list_unsafe.extend([1, 2, 3])  # ❌ Not atomic

# Safe: list.append() IS atomic
shared_list_safe = []

def append_safe():
    for _ in range(1000):
        shared_list_safe.append([1, 2, 3])  # ✅ Atomic

# Test unsafe
threads = []
for _ in range(5):
    t = threading.Thread(target=extend_unsafe)
    threads.append(t)
    t.start()
for t in threads:
    t.join()

print(f"Unsafe list length: {len(shared_list_unsafe)} (Expected: 15000)")

# Test safe
threads = []
for _ in range(5):
    t = threading.Thread(target=append_safe)
    threads.append(t)
    t.start()
for t in threads:
    t.join()

print(f"Safe list length: {len(shared_list_safe)} (Expected: 5000)")
```

## Common Race Condition Patterns

### Pattern 1: Read-Modify-Write
```python
# ❌ Unsafe
counter += 1

# ✅ Safe
with lock:
    counter += 1
```

### Pattern 2: Check-Then-Act
```python
# ❌ Unsafe
if key in dict:
    dict[key] += 1

# ✅ Safe
with lock:
    if key in dict:
        dict[key] += 1
```

### Pattern 3: Compound Operations
```python
# ❌ Unsafe
list.sort()
list.reverse()

# ✅ Safe
with lock:
    list.sort()
    list.reverse()
```

## Thread-Safe Data Structures in Python

Python provides thread-safe alternatives:

### 1. queue.Queue (Thread-Safe)
```python
from queue import Queue

q = Queue()

# Thread-safe operations
q.put(item)      # ✅ Thread-safe
q.get()          # ✅ Thread-safe
q.qsize()        # ✅ Thread-safe
```

### 2. collections.deque (Mostly Thread-Safe)
```python
from collections import deque

d = deque()

# Thread-safe operations
d.append(item)       # ✅ Atomic
d.appendleft(item)   # ✅ Atomic
d.pop()              # ✅ Atomic
d.popleft()          # ✅ Atomic
```

### 3. threading.local (Thread-Local Storage)
```python
import threading

thread_local = threading.local()

def worker():
    # Each thread has its own copy
    thread_local.value = threading.current_thread().name
    print(thread_local.value)
```

## Best Practices

1. **Identify shared mutable state** - This is where race conditions occur
2. **Use atomic operations when possible** - Simpler than locks
3. **Protect compound operations** - Use locks for multi-step operations
4. **Minimize shared state** - Less sharing = fewer race conditions
5. **Use thread-safe data structures** - Queue, deque for common patterns
6. **Document thread safety** - Make it clear what's protected and how
7. **Test thoroughly** - Race conditions are intermittent and hard to reproduce

## Testing for Race Conditions

```python
import threading

def test_thread_safety(func, expected, iterations=1000, threads=10):
    """Helper to test thread safety"""
    results = []
    
    for _ in range(iterations):
        # Reset state for each test
        # Run with multiple threads
        ts = []
        for _ in range(threads):
            t = threading.Thread(target=func)
            ts.append(t)
            t.start()
        
        for t in ts:
            t.join()
        
        # Check result
        results.append(check_result() == expected)
    
    success_rate = sum(results) / len(results) * 100
    print(f"Success rate: {success_rate}%")
    
    if success_rate < 100:
        print("⚠️  Thread safety issue detected!")
```

## Summary

### Thread-Safe in Python:
- Simple assignments: `x = value`
- Reading variables: `y = x`
- `list.append()`, `list.pop()` (no index)
- `dict[key] = value`, `dict.get(key)`

### NOT Thread-Safe:
- Read-modify-write: `x += 1`
- Check-then-act: `if key in dict: dict[key] += 1`
- Complex operations: `list.extend()`, `dict.update()`
- Multiple operations without locking

### Solutions:
1. Use locks for compound operations
2. Use atomic operations when possible
3. Use thread-safe data structures (Queue, deque)
4. Minimize shared mutable state
