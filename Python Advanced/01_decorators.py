"""
================================================================================
  DECORATORS — From Fundamentals to Production-Ready Mastery
================================================================================
  Author: Senior Software Engineer Practice Guide
  Goal:   Understand decorators at the dunder-method level, use them in
          production, avoid common pitfalls, and build muscle memory.
================================================================================
"""

# ─────────────────────────────────────────────────────────────────────────────
# SECTION 1: UNDER THE HOOD — How Decorators Actually Work
# ─────────────────────────────────────────────────────────────────────────────
"""
A decorator is simply a callable that takes a function and returns a new callable.

When you write:

    @my_decorator
    def greet():
        ...

Python does:

    greet = my_decorator(greet)

That's it.  Everything else—functools.wraps, arguments, classes—builds on
this one-line transformation.

KEY INSIGHT: Any object with a __call__ method is a valid decorator.
    - Functions have __call__ (they ARE callables)
    - Classes can define __call__ to become callable instances

The call chain:
    1. Python sees @decorator → calls decorator(original_fn)
    2. decorator returns a NEW callable (wrapper)
    3. Every future call to original_fn actually calls wrapper
    4. wrapper can run code BEFORE and AFTER calling original_fn
"""


# ── Proof: A class as a decorator via __call__ ──────────────────────────────

class CountCalls:
    """Decorator implemented as a class — demonstrates __call__ dunder."""

    def __init__(self, func):
        self.func = func
        self.call_count = 0

    def __call__(self, *args, **kwargs):
        """This is what gets invoked every time the decorated fn is called."""
        self.call_count += 1
        print(f"[CountCalls] {self.func.__name__} has been called {self.call_count} time(s)")
        return self.func(*args, **kwargs)


@CountCalls
def say_hello(name: str) -> str:
    return f"Hello, {name}!"


# Uncomment to test:
# print(say_hello("Sanket"))   # [CountCalls] say_hello has been called 1 time(s)
# print(say_hello("World"))    # [CountCalls] say_hello has been called 2 time(s)
# print(type(say_hello))       # <class '__main__.CountCalls'>  ← NOT a function anymore!


# ─────────────────────────────────────────────────────────────────────────────
# SECTION 2: PRODUCTION-READY EXAMPLE — @rate_limit decorator
# ─────────────────────────────────────────────────────────────────────────────
"""
Real-world scenario: You have an API client and want to limit how many calls
per second can be made.  This is a decorator WITH arguments, thread-safe.
"""

import functools
import threading
import time
from collections import deque


def rate_limit(max_calls: int, period: float = 1.0):
    """
    Decorator that limits a function to `max_calls` invocations per `period` seconds.
    Thread-safe using a lock.  Uses a sliding-window approach.

    Usage:
        @rate_limit(max_calls=5, period=1.0)
        def call_api(endpoint):
            ...
    """
    def decorator(func):
        timestamps = deque()          # sliding window of call timestamps
        lock = threading.Lock()       # thread safety

        @functools.wraps(func)        # preserves __name__, __doc__, __module__
        def wrapper(*args, **kwargs):
            with lock:
                now = time.monotonic()

                # Evict timestamps outside the current window
                while timestamps and timestamps[0] <= now - period:
                    timestamps.popleft()

                if len(timestamps) >= max_calls:
                    sleep_time = period - (now - timestamps[0])
                    if sleep_time > 0:
                        print(f"[rate_limit] Throttling {func.__name__} for {sleep_time:.3f}s")
                        time.sleep(sleep_time)

                    # Re-check after sleeping
                    now = time.monotonic()
                    while timestamps and timestamps[0] <= now - period:
                        timestamps.popleft()

                timestamps.append(time.monotonic())

            return func(*args, **kwargs)

        # Expose internals for testing/inspection
        wrapper._timestamps = timestamps
        wrapper._lock = lock
        return wrapper
    return decorator


@rate_limit(max_calls=3, period=2.0)
def fetch_data(url: str) -> str:
    """Simulate an API call."""
    return f"Response from {url}"


# Uncomment to test:
# for i in range(6):
#     print(f"Call {i+1}: {fetch_data(f'https://api.example.com/data/{i}')}")


# ── Another production example: @retry with exponential backoff ─────────────

def retry(max_attempts: int = 3, backoff_factor: float = 0.5, exceptions: tuple = (Exception,)):
    """
    Retries the decorated function on failure with exponential backoff.
    
    Usage:
        @retry(max_attempts=3, backoff_factor=0.5, exceptions=(ConnectionError, TimeoutError))
        def unreliable_api_call():
            ...
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None
            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    last_exception = e
                    if attempt < max_attempts:
                        wait = backoff_factor * (2 ** (attempt - 1))
                        print(f"[retry] {func.__name__} attempt {attempt} failed: {e}. "
                              f"Retrying in {wait:.1f}s...")
                        time.sleep(wait)
                    else:
                        print(f"[retry] {func.__name__} failed after {max_attempts} attempts.")
            raise last_exception
        return wrapper
    return decorator


# ── Production example: @cache_with_ttl — time-based caching ───────────────

def cache_with_ttl(ttl_seconds: float = 60.0):
    """
    Caches function results with a time-to-live.  Thread-safe.
    Unlike functools.lru_cache, entries expire after ttl_seconds.
    """
    def decorator(func):
        cache = {}
        lock = threading.Lock()

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            key = (args, tuple(sorted(kwargs.items())))
            now = time.monotonic()

            with lock:
                if key in cache:
                    result, timestamp = cache[key]
                    if now - timestamp < ttl_seconds:
                        print(f"[cache_hit] {func.__name__}{args}")
                        return result
                    else:
                        del cache[key]  # expired

            # Call outside lock to avoid holding lock during slow calls
            result = func(*args, **kwargs)

            with lock:
                cache[key] = (result, time.monotonic())

            return result

        def clear_cache():
            with lock:
                cache.clear()

        wrapper.clear_cache = clear_cache
        wrapper._cache = cache
        return wrapper
    return decorator


# ─────────────────────────────────────────────────────────────────────────────
# SECTION 3: COMMON PITFALLS — Top 3 bugs juniors introduce
# ─────────────────────────────────────────────────────────────────────────────

# ┌─────────────────────────────────────────────────────────────────────────┐
# │ PITFALL #1: Forgetting @functools.wraps(func)                          │
# │                                                                         │
# │ Without it, the decorated function loses its __name__, __doc__,        │
# │ __module__, and __qualname__.  This breaks:                            │
# │   - Logging (you see "wrapper" instead of the real function name)      │
# │   - Debugging / stack traces                                           │
# │   - API documentation generators (Sphinx, FastAPI)                     │
# │   - Serialization / pickling                                           │
# │   - pytest fixtures that match by name                                 │
# └─────────────────────────────────────────────────────────────────────────┘

# BAD
def bad_decorator(func):
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper

@bad_decorator
def important_function():
    """This docstring will be LOST."""
    pass

# print(important_function.__name__)  # "wrapper" ← WRONG
# print(important_function.__doc__)   # None       ← LOST

# GOOD
def good_decorator(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper

@good_decorator
def important_function_v2():
    """This docstring is preserved."""
    pass

# print(important_function_v2.__name__)  # "important_function_v2" ← CORRECT
# print(important_function_v2.__doc__)   # "This docstring is preserved."


# ┌─────────────────────────────────────────────────────────────────────────┐
# │ PITFALL #2: Mutable default state shared across ALL decorated functions │
# │                                                                         │
# │ If you store state in the decorator's OUTER scope (rather than per-fn),│
# │ all decorated functions share the same state.                          │
# └─────────────────────────────────────────────────────────────────────────┘

# BAD — one shared counter for ALL decorated functions
call_log = []  # ← shared mutable state!

def log_calls_bad(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        call_log.append(func.__name__)  # ALL functions write to same list
        return func(*args, **kwargs)
    return wrapper

# GOOD — each decorated function gets its own state
def log_calls_good(func):
    func._call_log = []  # ← per-function state

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        func._call_log.append(time.time())
        return func(*args, **kwargs)
    return wrapper


# ┌─────────────────────────────────────────────────────────────────────────┐
# │ PITFALL #3: Decorator with arguments — missing the extra nesting layer │
# │                                                                         │
# │ @decorator        → decorator(func)                                    │
# │ @decorator(args)  → decorator(args)(func)   ← needs 3 levels!         │
# └─────────────────────────────────────────────────────────────────────────┘

# BAD — only 2 levels, will crash with TypeError
# def repeat_bad(times):
#     @functools.wraps(func)   # ← WHERE is `func`? Not in scope!
#     def wrapper(*args, **kwargs):
#         for _ in range(times):
#             func(*args, **kwargs)
#     return wrapper

# GOOD — 3 levels: outer(args) → decorator(func) → wrapper(*args)
def repeat(times: int):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            result = None
            for _ in range(times):
                result = func(*args, **kwargs)
            return result
        return wrapper
    return decorator

@repeat(times=3)
def greet(name):
    print(f"Hello, {name}!")

# Uncomment: greet("Sanket")  # prints 3 times


# ─────────────────────────────────────────────────────────────────────────────
# SECTION 4: BROKEN CODE — Fix These! (Thread-Safety & Efficiency)
# ─────────────────────────────────────────────────────────────────────────────

"""
╔══════════════════════════════════════════════════════════════════════════════╗
║  PROBLEM 1: Fix the @memoize decorator                                     ║
║                                                                             ║
║  This decorator has 3 bugs:                                                ║
║    1. It's NOT thread-safe (race condition on shared dict)                 ║
║    2. It loses the original function's metadata                            ║
║    3. The cache grows unbounded — add a max_size limit                     ║
║                                                                             ║
║  Hints:                                                                    ║
║    - threading.Lock for thread safety                                      ║
║    - functools.wraps to preserve metadata                                  ║
║    - collections.OrderedDict for LRU eviction                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

# ── BROKEN CODE — DO NOT PEEK AT SOLUTION ──

def memoize(func):
    cache = {}

    def wrapper(*args):
        if args not in cache:
            cache[args] = func(*args)
        return cache[args]

    return wrapper

@memoize
def expensive_computation(n):
    """Simulates an expensive computation."""
    time.sleep(0.1)
    return n ** 2

# TEST: Call from multiple threads — will it break?
# from concurrent.futures import ThreadPoolExecutor
# with ThreadPoolExecutor(max_workers=10) as pool:
#     results = list(pool.map(expensive_computation, range(20)))


"""
╔══════════════════════════════════════════════════════════════════════════════╗
║  PROBLEM 2: Fix the @audit_log decorator                                   ║
║                                                                             ║
║  This decorator logs function calls to a list.  It has 4 bugs:             ║
║    1. Swallows ALL exceptions silently (masks real errors)                 ║
║    2. Logs the same entry twice on retry                                   ║
║    3. Log list is module-level (shared across ALL decorated funcs)         ║
║    4. Not safe for concurrent access                                       ║
║                                                                             ║
║  Hints:                                                                    ║
║    - Re-raise exceptions after logging                                     ║
║    - Each decorated function should own its log                            ║
║    - Use a lock for the log list                                           ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

# ── BROKEN CODE — DO NOT PEEK AT SOLUTION ──

_global_log = []   # ← Bug: shared across all decorated functions

def audit_log(func):
    def wrapper(*args, **kwargs):
        entry = {"function": func.__name__, "args": args, "kwargs": kwargs}
        _global_log.append(entry)
        try:
            result = func(*args, **kwargs)
            entry["status"] = "success"
            entry["result"] = result
            _global_log.append(entry)   # ← Bug: double append
            return result
        except Exception as e:
            entry["status"] = "error"
            entry["error"] = str(e)
            # ← Bug: exception is swallowed, never re-raised
    return wrapper

@audit_log
def divide(a, b):
    """Divide a by b."""
    return a / b

# divide(10, 0)  ← This should raise ZeroDivisionError, but it returns None!


"""
╔══════════════════════════════════════════════════════════════════════════════╗
║  PROBLEM 3: Fix the @validate_types decorator                              ║
║                                                                             ║
║  Should validate argument types based on annotations. Has bugs:            ║
║    1. Doesn't handle **kwargs at all                                       ║
║    2. Crashes if function has no annotations                               ║
║    3. Doesn't work with methods (self param breaks it)                     ║
║    4. Missing functools.wraps                                              ║
║                                                                             ║
║  Hints:                                                                    ║
║    - Use inspect.signature for robust argument binding                     ║
║    - Skip 'self' and 'cls' parameters                                     ║
║    - Guard against missing annotations with .get()                        ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

# ── BROKEN CODE — DO NOT PEEK AT SOLUTION ──

import inspect

def validate_types(func):
    def wrapper(*args, **kwargs):
        annotations = func.__annotations__
        for i, (arg_name, arg_val) in enumerate(zip(annotations, args)):
            expected_type = annotations[arg_name]
            if not isinstance(arg_val, expected_type):
                raise TypeError(
                    f"Argument '{arg_name}' expected {expected_type.__name__}, "
                    f"got {type(arg_val).__name__}"
                )
        return func(*args, **kwargs)
    return wrapper

@validate_types
def add_numbers(a: int, b: int) -> int:
    """Add two numbers."""
    return a + b

# add_numbers(1, 2)      # Works
# add_numbers(1, "two")  # Should raise TypeError
# add_numbers(a=1, b=2)  # ← BUG: kwargs not validated!


# ─────────────────────────────────────────────────────────────────────────────
# SECTION 5: REFACTORING CHALLENGE
# ─────────────────────────────────────────────────────────────────────────────

"""
╔══════════════════════════════════════════════════════════════════════════════╗
║  REFACTORING CHALLENGE: Clean up this messy function using decorators.     ║
║                                                                             ║
║  The function below does TOO MANY THINGS:                                  ║
║    - Input validation                                                      ║
║    - Timing                                                                ║
║    - Retry logic                                                           ║
║    - Logging                                                               ║
║    - The actual business logic                                             ║
║                                                                             ║
║  YOUR TASK: Refactor into a clean function with decorators handling the    ║
║  cross-cutting concerns.  The function body should be ~3 lines.            ║
║                                                                             ║
║  Create these decorators:                                                  ║
║    @log_execution     — logs entry/exit with args                          ║
║    @time_it           — prints execution time                              ║
║    @retry_on_failure  — retries up to 3 times on ConnectionError           ║
║    @validate_input    — validates the input types                          ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

# ── MESSY CODE TO REFACTOR ──

import random
import logging

logger = logging.getLogger(__name__)

def process_payment(user_id, amount, currency="INR"):
    # === Input validation ===
    if not isinstance(user_id, int):
        raise TypeError(f"user_id must be int, got {type(user_id).__name__}")
    if not isinstance(amount, (int, float)):
        raise TypeError(f"amount must be numeric, got {type(amount).__name__}")
    if amount <= 0:
        raise ValueError("amount must be positive")
    if currency not in ("INR", "USD", "EUR", "GBP"):
        raise ValueError(f"Unsupported currency: {currency}")

    # === Logging ===
    logger.info(f"Processing payment: user={user_id}, amount={amount}, currency={currency}")

    # === Timing ===
    start = time.time()

    # === Retry logic ===
    last_error = None
    for attempt in range(1, 4):
        try:
            # === ACTUAL BUSINESS LOGIC ===
            if random.random() < 0.3:
                raise ConnectionError("Payment gateway timeout")

            transaction_id = f"TXN-{user_id}-{int(time.time())}"
            result = {
                "transaction_id": transaction_id,
                "user_id": user_id,
                "amount": amount,
                "currency": currency,
                "status": "success"
            }

            elapsed = time.time() - start
            logger.info(f"Payment processed in {elapsed:.3f}s: {transaction_id}")
            return result

        except ConnectionError as e:
            last_error = e
            logger.warning(f"Attempt {attempt}/3 failed: {e}")
            time.sleep(0.5 * attempt)

    elapsed = time.time() - start
    logger.error(f"Payment FAILED after 3 attempts in {elapsed:.3f}s")
    raise last_error


# ═════════════════════════════════════════════════════════════════════════════
# YOUR REFACTORED VERSION GOES HERE:
# ═════════════════════════════════════════════════════════════════════════════

# @log_execution
# @time_it
# @retry_on_failure(max_attempts=3, exceptions=(ConnectionError,))
# @validate_input
# def process_payment_clean(user_id: int, amount: float, currency: str = "INR"):
#     """Process a payment — just the business logic."""
#     if random.random() < 0.3:
#         raise ConnectionError("Payment gateway timeout")
#     transaction_id = f"TXN-{user_id}-{int(time.time())}"
#     return {"transaction_id": transaction_id, "status": "success",
#             "user_id": user_id, "amount": amount, "currency": currency}


# ─────────────────────────────────────────────────────────────────────────────
# SECTION 6: STACKING DECORATORS — Execution Order
# ─────────────────────────────────────────────────────────────────────────────
"""
When you stack decorators:

    @A
    @B
    @C
    def func(): ...

Python does:  func = A(B(C(func)))

Execution order:
    - A's wrapper runs FIRST (outermost)
    - Then B's wrapper
    - Then C's wrapper
    - Then the actual func
    - Returns bubble back: C → B → A

Think of it as layers of an onion.

    @log          ← logs entry/exit (sees everything)
    @authenticate ← checks auth (runs before business logic)
    @cache        ← checks cache (innermost, closest to func)
    def get_data():
        ...
"""

if __name__ == "__main__":
    print("=" * 60)
    print("  Decorator Practice Module")
    print("=" * 60)
    print()

    # Demo: CountCalls class decorator
    print("--- CountCalls demo ---")
    print(say_hello("Sanket"))
    print(say_hello("World"))
    print(f"Total calls: {say_hello.call_count}")
    print()

    # Demo: rate_limit
    print("--- rate_limit demo ---")
    for i in range(5):
        print(f"  Call {i+1}: {fetch_data(f'https://api.example.com/{i}')}")
    print()

    # Demo: Metadata preservation
    print("--- Metadata pitfall demo ---")
    print(f"  bad_decorator result:  __name__={important_function.__name__!r}")
    print(f"  good_decorator result: __name__={important_function_v2.__name__!r}")
