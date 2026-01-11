"""
Cache Decorator with Auto-Expiration using Background Threads

This module provides a caching decorator that automatically clears expired
entries using a background thread. It demonstrates several important
threading concepts in Python.
"""

from functools import wraps
import time
import threading
from loguru import logger


def cache_me_auto_expire(ttl=120, cleanup_interval=30):
    """
    Cache decorator that automatically clears expired entries in the background.
    
    Args:
        ttl: Time to live in seconds (default 120 = 2 minutes)
        cleanup_interval: How often to run cleanup in seconds (default 30)
    
    
    ==================================================================================
    CONCEPT 1: THREADS
    ==================================================================================
    
    What is a Thread?
    -----------------
    A thread is the smallest unit of execution within a process. Think of a process
    as a running program (like your Python script), and threads as workers inside
    that program that can do tasks simultaneously.
    
    By default, Python runs in a single thread (the "main thread"). When you use
    the `threading` module, you can create additional threads to run code concurrently.
    
    Why use threads?
    ----------------
    - To perform background tasks (like our cache cleanup) without blocking main code
    - To handle I/O-bound operations (file reading, network requests) efficiently
    - To keep UI responsive while doing work in the background
    
    ----------------------
    
    
    ==================================================================================
    CONCEPT 2: DAEMON THREADS
    ==================================================================================
    
    What is a Daemon Thread?
    ------------------------
    A daemon thread is a "background" thread that automatically terminates when all
    non-daemon (main) threads have finished. Think of it as a helper that should
    NOT keep the program alive if the main work is done.
    
    Daemon vs Non-Daemon:
    ---------------------
    - Non-daemon thread: Program waits for it to complete before exiting
    - Daemon thread: Program can exit even if daemon is still running (daemon dies)
    
    Why daemon=True for our cleanup thread?
    ---------------------------------------
    We don't want the cache cleanup thread to keep the program running forever.
    When the main program finishes, the cleanup thread should also stop.
    
    Daemon Thread Example:
    ----------------------
    ```python
    import threading
    import time
    
    def background_task():
        while True:
            print("Background task running...")
            time.sleep(1)
    
    # NON-DAEMON (daemon=False, the default)
    # This would keep the program running forever!
    # thread = threading.Thread(target=background_task, daemon=False)
    
    # DAEMON (daemon=True)
    # Program will exit after main code finishes, killing this thread
    thread = threading.Thread(target=background_task, daemon=True)
    thread.start()
    
    print("Main thread doing work...")
    time.sleep(3)
    print("Main thread done. Program will exit, daemon thread will be killed.")
    # Output:
    # Main thread doing work...
    # Background task running...
    # Background task running...
    # Background task running...
    # Main thread done. Program will exit, daemon thread will be killed.
    # (program exits, no more "Background task running...")
    ```
    
    When to use Daemon Threads:
    ---------------------------
    ✓ Background cleanup/maintenance tasks (like our cache cleanup)
    ✓ Logging or monitoring threads
    ✓ Heartbeat/health check threads
    ✗ Don't use for critical operations that must complete (data saving, etc.)
    
    
    ==================================================================================
    CONCEPT 3: RACE CONDITIONS
    ==================================================================================
    
    What is a Race Condition?
    -------------------------
    A race condition occurs when two or more threads access shared data simultaneously,
    and the final result depends on the unpredictable timing/order of execution.
    It's called a "race" because threads are "racing" to access/modify the data.
    
    Race conditions lead to bugs that are:
    - Hard to reproduce (timing-dependent)
    - Hard to debug (may not occur during testing)
    - Potentially catastrophic (data corruption, crashes)
    
    Classic Race Condition Example (BROKEN CODE):
    ----------------------------------------------
    ```python
    import threading
    
    counter = 0  # Shared variable
    
    def increment():
        global counter
        for _ in range(100000):
            counter += 1  # NOT atomic! This is actually:
                          # 1. Read counter value
                          # 2. Add 1 to value
                          # 3. Write new value back
                          # Another thread can interfere between steps!
    
    thread1 = threading.Thread(target=increment)
    thread2 = threading.Thread(target=increment)
    
    thread1.start()
    thread2.start()
    thread1.join()
    thread2.join()
    
    print(f"Counter: {counter}")  # Expected: 200000
                                   # Actual: Something less! (e.g., 154832)
                                   # Because increments were "lost" due to race
    ```
    
    How Race Conditions Happen (Step by Step):
    ------------------------------------------
    Time    Thread1              Thread2              counter (actual)
    ----    -------              -------              ----------------
    T1      Read counter (0)                          0
    T2                           Read counter (0)     0
    T3      Add 1 (result=1)                          0
    T4                           Add 1 (result=1)     0
    T5      Write 1                                   1
    T6                           Write 1              1  ← Should be 2!
    
    Both threads read 0, both write 1. One increment was LOST!
    
    Race Condition in OUR Cache (without lock):
    -------------------------------------------
    ```python
    # BROKEN: Without lock, this could happen:
    # Thread1 (main): Checking if key exists...
    # Thread2 (cleanup): Deleting the key...
    # Thread1 (main): Key exists! Trying to read it...
    # CRASH! KeyError because Thread2 deleted it between check and read
    ```
    
    
    ==================================================================================
    CONCEPT 4: THREAD LOCKS (threading.Lock)
    ==================================================================================
    
    What is a Lock?
    ---------------
    A lock (also called mutex - "mutual exclusion") is a synchronization primitive
    that ensures only ONE thread can access a shared resource at a time.
    
    Think of it like a bathroom key:
    - Only one person can have the key at a time
    - Others must wait until the key is returned
    - This prevents "collisions" (two people using bathroom simultaneously)
    
    How Lock Works:
    ---------------
    ```python
    lock = threading.Lock()
    
    # Method 1: Explicit acquire/release
    lock.acquire()      # Get the lock (blocks if another thread has it)
    # ... critical section (only one thread can be here) ...
    lock.release()      # Release the lock (let others in)
    
    # Method 2: Context manager (RECOMMENDED - auto-releases on exception)
    with lock:
        # ... critical section ...
        pass  # Lock automatically released when exiting 'with' block
    ```
    
    Fixed Counter Example (with Lock):
    ----------------------------------
    ```python
    import threading
    
    counter = 0
    lock = threading.Lock()
    
    def increment():
        global counter
        for _ in range(100000):
            with lock:  # Only one thread can execute this block at a time
                counter += 1
    
    thread1 = threading.Thread(target=increment)
    thread2 = threading.Thread(target=increment)
    
    thread1.start()
    thread2.start()
    thread1.join()
    thread2.join()
    
    print(f"Counter: {counter}")  # Now correctly prints: 200000
    ```
    
    Why we use Lock in our cache:
    -----------------------------
    - Main thread reads/writes to _cache dict
    - Cleanup thread deletes from _cache dict
    - Without lock: cleanup might delete while main is reading → crash
    - With lock: operations are serialized, no conflicts
    
    Lock Types in Python:
    ---------------------
    1. threading.Lock()      - Basic lock, can't be acquired twice by same thread
    2. threading.RLock()     - Reentrant lock, same thread can acquire multiple times
    3. threading.Semaphore() - Allows N threads to access resource simultaneously
    4. threading.Event()     - Signal between threads (used for _stop_cleanup)
    
    
    ==================================================================================
    CONCEPT 5: threading.Event (used for _stop_cleanup)
    ==================================================================================
    
    What is an Event?
    -----------------
    An Event is a simple thread-safe flag for communication between threads.
    One thread can "set" the event, and another thread can "wait" for it or check it.
    
    Event Methods:
    --------------
    - event.set()      : Set the flag to True
    - event.clear()    : Reset the flag to False
    - event.is_set()   : Check if flag is True
    - event.wait()     : Block until flag becomes True
    
    Event Example:
    --------------
    ```python
    import threading
    import time
    
    stop_event = threading.Event()
    
    def worker():
        print("Worker started")
        while not stop_event.is_set():  # Keep running until told to stop
            print("Working...")
            time.sleep(1)
        print("Worker stopped gracefully")
    
    thread = threading.Thread(target=worker)
    thread.start()
    
    time.sleep(3)           # Let worker run for 3 seconds
    stop_event.set()        # Signal worker to stop
    thread.join()           # Wait for worker to finish
    print("Main done")
    
    # Output:
    # Worker started
    # Working...
    # Working...
    # Working...
    # Worker stopped gracefully
    # Main done
    ```
    
    Why we use Event for _stop_cleanup:
    -----------------------------------
    It provides a graceful way to stop the cleanup thread. Instead of abruptly
    killing it, we signal it to stop, and it exits on its next iteration.
    
    ==================================================================================
    """
    def decorator_factory(fn):
        _cache = {}  # stores {args: (result, timestamp)}
        
        # Lock ensures thread-safe access to _cache
        # Without this, race conditions could occur when main thread and 
        # cleanup thread both access _cache simultaneously
        _lock = threading.Lock()
        
        _cleanup_thread = None
        
        # Event to signal the cleanup thread to stop gracefully
        _stop_cleanup = threading.Event()

        def cleanup_expired():
            """
            Background thread function that removes expired cache entries.
            
            This runs in a loop, checking every `cleanup_interval` seconds
            for entries that have exceeded their TTL.
            """
            while not _stop_cleanup.is_set():  # Check if we should stop
                time.sleep(cleanup_interval)
                current_time = time.time()
                
                # CRITICAL SECTION: Must use lock when accessing shared _cache
                with _lock:
                    # Find all expired keys first (can't modify dict while iterating)
                    expired_keys = [
                        key for key, (_, cached_time) in _cache.items()
                        if current_time - cached_time >= ttl
                    ]
                    # Now delete the expired keys
                    for key in expired_keys:
                        del _cache[key]
                        logger.info(f"Auto-cleared expired cache for args: {key}")

        def start_cleanup_thread():
            """
            Lazily start the cleanup thread (only when first cache entry is made).
            Uses `nonlocal` to modify the outer function's _cleanup_thread variable.
            """
            nonlocal _cleanup_thread
            if _cleanup_thread is None or not _cleanup_thread.is_alive():
                _stop_cleanup.clear()  # Reset stop signal
                
                # Create daemon thread - will be killed when main program exits
                # daemon=True is crucial here, otherwise program would hang forever
                _cleanup_thread = threading.Thread(target=cleanup_expired, daemon=True)
                _cleanup_thread.start()

        @wraps(fn)
        def wrapper(*args):
            start_cleanup_thread()  # Ensure cleanup thread is running
            current_time = time.time()
            
            # CRITICAL SECTION: Reading from shared _cache
            with _lock:
                if args in _cache:
                    result, cached_time = _cache[args]
                    if current_time - cached_time < ttl:
                        logger.info(f"Fetching from cache for args: {args}")
                        return result
                    else:
                        logger.info(f"Cache expired for args: {args}, recalculating...")

            # Computation happens OUTSIDE the lock (don't hold lock during slow ops)
            logger.info(f"Calculating result for args: {args}")
            result = fn(*args)
            
            # CRITICAL SECTION: Writing to shared _cache
            with _lock:
                _cache[args] = (result, current_time)

            return result

        # Expose cache for inspection/testing
        wrapper.cache = _cache
        wrapper.stop_cleanup = lambda: _stop_cleanup.set()
        
        return wrapper
    
    return decorator_factory


# ===================================================================================
# USAGE EXAMPLE
# ===================================================================================

if __name__ == "__main__":
    
    @cache_me_auto_expire(ttl=10, cleanup_interval=5)  # Short TTL for testing
    def expensive_calculation(x, y):
        """Simulates an expensive calculation."""
        logger.info(f"Performing expensive calculation for ({x}, {y})...")
        time.sleep(2)  # Simulate slow computation
        return x + y

    # First call - will compute
    print(f"Result 1: {expensive_calculation(1, 2)}")
    
    # Second call with same args - will use cache
    print(f"Result 2: {expensive_calculation(1, 2)}")
    
    # Different args - will compute
    print(f"Result 3: {expensive_calculation(3, 4)}")
    
    # Wait for cache to expire (TTL is 10 seconds)
    print("\nWaiting 12 seconds for cache to auto-expire...")
    time.sleep(12)
    
    # This will recompute because cache was auto-cleared
    print(f"Result 4: {expensive_calculation(1, 2)}")
