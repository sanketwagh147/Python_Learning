"""
Docstring for multi threading.simple_thread_lock
Atomic means indivisible and uninterruptible.
In multithreading, an atomic operation is one that completes in a single step relative to other threads. This means that once an atomic operation starts, it runs to completion without any possibility of being interrupted or observed in an incomplete state by other threads.
"""

import threading


class UnsafeCounter:
    
    def __init__(self):
        self.count = 0

    def increment(self):
        """
        Not thread safe
        Triggers Read-Modify-Write Race condition
        """
        self.count += 1

class SafeCounter:
    def __init__(self):
        self.count = 0
        self._lock = threading.Lock()

    def increment(self):
        """
        Not thread safe
        Triggers Read-Modify-Write Race condition
        """
        with self._lock:
            self.count += 1

def run_test(counter_class,thread_count = 100, increment=1000):
    
    counter = counter_class()
    name = counter.__class__

    threads = []

    print(f"Worker Working on counter{name}")
    def worker():
        for _ in range(increment):
            counter.increment()

    
    for _ in range(thread_count):
        t = threading.Thread(target=worker)
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    print(f"{name} : Final Count = {counter.count} Expected = 100000")

if __name__ == "__main__":
    
    # 
    run_test(UnsafeCounter,1000,increment=10000)
    run_test(SafeCounter,1000,increment=10000)
    