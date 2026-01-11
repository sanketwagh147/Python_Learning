# Thread Synchronization: Locks

When multiple threads access shared resources, synchronization is needed to prevent race conditions and data corruption.

## The Problem: Race Conditions

A **race condition** occurs when multiple threads access and modify shared data simultaneously, leading to unpredictable results.

## Solution: Locks

A **Lock** (also called mutex - mutual exclusion) ensures that only one thread can access a shared resource at a time.

## Lock Methods

```python
lock = threading.Lock()

lock.acquire()      # Acquire the lock (blocks if already held)
lock.release()      # Release the lock
lock.locked()       # Returns True if lock is currently held

# Context manager (recommended)
with lock:
    # Critical section
    pass
```

## Example 1: Race Condition (Without Lock)

```python
import threading
import time

# Shared resource
counter = 0

def increment():
    global counter
    for _ in range(100000):
        # Race condition: Read-Modify-Write
        temp = counter  # Read
        temp += 1       # Modify
        counter = temp  # Write

# Create threads
threads = []
for _ in range(5):
    t = threading.Thread(target=increment)
    threads.append(t)
    t.start()

# Wait for all threads
for t in threads:
    t.join()

print(f"Final counter value: {counter}")
print(f"Expected value: {5 * 100000}")
```

**Output (varies each run):**
```
Final counter value: 137294
Expected value: 500000
```
❌ **Problem**: Lost updates due to race condition!

## Example 2: Fixed with Lock

```python
import threading

counter = 0
lock = threading.Lock()  # Create a lock

def increment_safe():
    global counter
    for _ in range(100000):
        with lock:  # Acquire lock
            counter += 1
        # Lock automatically released here

# Create threads
threads = []
for _ in range(5):
    t = threading.Thread(target=increment_safe)
    threads.append(t)
    t.start()

# Wait for all threads
for t in threads:
    t.join()

print(f"Final counter value: {counter}")
print(f"Expected value: {5 * 100000}")
```

**Output:**
```
Final counter value: 500000
Expected value: 500000
```
✅ **Solution**: Lock ensures thread-safe access!

## Example 3: Bank Account (Without Lock)

```python
import threading
import time
import random

class BankAccount:
    def __init__(self, balance):
        self.balance = balance
    
    def withdraw(self, amount):
        print(f"Thread {threading.current_thread().name} attempting to withdraw ${amount}")
        
        if self.balance >= amount:
            print(f"Thread {threading.current_thread().name} checking balance: ${self.balance}")
            time.sleep(0.1)  # Simulate processing time
            
            self.balance -= amount
            print(f"Thread {threading.current_thread().name} withdrew ${amount}. New balance: ${self.balance}")
        else:
            print(f"Thread {threading.current_thread().name} insufficient funds!")

# Create account with $100
account = BankAccount(100)

# Two threads try to withdraw $60 each
threads = []
for i in range(2):
    t = threading.Thread(target=account.withdraw, args=(60,), name=f"Customer-{i+1}")
    threads.append(t)
    t.start()

for t in threads:
    t.join()

print(f"\nFinal balance: ${account.balance}")
```

**Output (Race Condition):**
```
Thread Customer-1 attempting to withdraw $60
Thread Customer-1 checking balance: $100
Thread Customer-2 attempting to withdraw $60
Thread Customer-2 checking balance: $100
Thread Customer-1 withdrew $60. New balance: $40
Thread Customer-2 withdrew $60. New balance: $-20

Final balance: $-20
```
❌ **Problem**: Negative balance! Both threads checked balance before either withdrew.

## Example 4: Bank Account (With Lock)

```python
import threading
import time

class BankAccountSafe:
    def __init__(self, balance):
        self.balance = balance
        self.lock = threading.Lock()
    
    def withdraw(self, amount):
        with self.lock:  # Critical section protected
            print(f"Thread {threading.current_thread().name} attempting to withdraw ${amount}")
            
            if self.balance >= amount:
                print(f"Thread {threading.current_thread().name} checking balance: ${self.balance}")
                time.sleep(0.1)  # Simulate processing time
                
                self.balance -= amount
                print(f"Thread {threading.current_thread().name} withdrew ${amount}. New balance: ${self.balance}")
            else:
                print(f"Thread {threading.current_thread().name} insufficient funds!")

# Create account with $100
account = BankAccountSafe(100)

# Two threads try to withdraw $60 each
threads = []
for i in range(2):
    t = threading.Thread(target=account.withdraw, args=(60,), name=f"Customer-{i+1}")
    threads.append(t)
    t.start()

for t in threads:
    t.join()

print(f"\nFinal balance: ${account.balance}")
```

**Output:**
```
Thread Customer-1 attempting to withdraw $60
Thread Customer-1 checking balance: $100
Thread Customer-1 withdrew $60. New balance: $40
Thread Customer-2 attempting to withdraw $60
Thread Customer-2 insufficient funds!

Final balance: $40
```
✅ **Solution**: Lock ensures only one thread accesses account at a time!

## Example 5: Lock with acquire() and release()

```python
import threading

counter = 0
lock = threading.Lock()

def increment_manual():
    global counter
    for _ in range(100000):
        lock.acquire()  # Manually acquire
        try:
            counter += 1
        finally:
            lock.release()  # Always release, even if exception occurs

threads = []
for _ in range(5):
    t = threading.Thread(target=increment_manual)
    threads.append(t)
    t.start()

for t in threads:
    t.join()

print(f"Final counter: {counter}")
```

**Note**: Using `with lock:` is preferred as it automatically releases the lock even if an exception occurs.

## Example 6: Checking Lock Status

```python
import threading
import time

lock = threading.Lock()

def check_lock_status():
    print(f"Lock held? {lock.locked()}")
    
    with lock:
        print(f"Inside critical section - Lock held? {lock.locked()}")
        time.sleep(1)
    
    print(f"After critical section - Lock held? {lock.locked()}")

thread = threading.Thread(target=check_lock_status)
thread.start()
thread.join()
```

**Output:**
```
Lock held? False
Inside critical section - Lock held? True
After critical section - Lock held? False
```

## Example 7: Deadlock Warning

```python
import threading
import time

lock1 = threading.Lock()
lock2 = threading.Lock()

def thread1():
    with lock1:
        print("Thread 1: Acquired lock1")
        time.sleep(0.1)
        
        print("Thread 1: Waiting for lock2...")
        with lock2:
            print("Thread 1: Acquired lock2")

def thread2():
    with lock2:
        print("Thread 2: Acquired lock2")
        time.sleep(0.1)
        
        print("Thread 2: Waiting for lock1...")
        with lock1:
            print("Thread 2: Acquired lock1")

# This will cause deadlock!
t1 = threading.Thread(target=thread1)
t2 = threading.Thread(target=thread2)

t1.start()
t2.start()

t1.join(timeout=2)
t2.join(timeout=2)

if t1.is_alive() or t2.is_alive():
    print("\n⚠️  DEADLOCK DETECTED!")
```

**Output:**
```
Thread 1: Acquired lock1
Thread 2: Acquired lock2
Thread 1: Waiting for lock2...
Thread 2: Waiting for lock1...

⚠️  DEADLOCK DETECTED!
```

## Avoiding Deadlock

```python
def thread1_fixed():
    with lock1:
        print("Thread 1: Acquired lock1")
        time.sleep(0.1)
        with lock2:  # Always acquire locks in same order
            print("Thread 1: Acquired lock2")

def thread2_fixed():
    with lock1:  # Same order as thread1
        print("Thread 2: Acquired lock1")
        time.sleep(0.1)
        with lock2:
            print("Thread 2: Acquired lock2")
```

## Best Practices

1. **Use context manager (`with lock:`)** - Automatic release, exception-safe
2. **Keep critical sections small** - Hold locks for minimum time necessary
3. **Consistent lock ordering** - Prevents deadlocks
4. **One lock per resource** - Fine-grained locking for better concurrency
5. **Avoid nested locks** - Increases deadlock risk
6. **Document lock usage** - Make it clear what each lock protects

## When to Use Locks

✅ **Use locks when:**
- Multiple threads access shared mutable data
- Read-modify-write operations on shared variables
- Maintaining invariants across multiple variables
- Implementing thread-safe data structures

❌ **Don't use locks when:**
- Only reading immutable data
- Each thread has its own data (no sharing)
- Using thread-safe data structures (Queue, etc.)

## Performance Considerations

```python
import threading
import time

# Bad: Lock held too long
def bad_pattern():
    with lock:
        # Critical operation
        data = shared_data
        # Non-critical operation (should be outside lock!)
        time.sleep(1)  # Long operation
        result = process(data)
        shared_data = result

# Good: Minimize critical section
def good_pattern():
    with lock:
        # Only critical operation inside lock
        data = shared_data
    
    # Non-critical operation outside lock
    result = process(data)
    
    with lock:
        shared_data = result
```

## Summary

- **Race Condition**: Multiple threads accessing shared data unsafely
- **Lock**: Ensures mutual exclusion (only one thread at a time)
- **Context Manager**: `with lock:` automatically handles acquire/release
- **Deadlock**: Two threads waiting for each other's locks
- **Critical Section**: Code protected by a lock
- **Best Practice**: Keep critical sections small and use consistent lock ordering
