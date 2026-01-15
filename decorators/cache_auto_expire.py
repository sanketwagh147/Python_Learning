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
    Decorator factory that returns a caching decorator with auto-expiration.
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
