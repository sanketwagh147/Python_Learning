"""
================================================================================
  CLOSURES & SCOPING — From Fundamentals to Production-Ready Mastery
================================================================================
  Author: Senior Software Engineer Practice Guide
  Goal:   Master LEGB scope resolution, closures, nonlocal, late binding,
          and factory patterns that are the foundation of decorators.
================================================================================
"""

# ─────────────────────────────────────────────────────────────────────────────
# SECTION 1: UNDER THE HOOD — LEGB Rule and Cell Variables
# ─────────────────────────────────────────────────────────────────────────────
"""
LEGB SCOPE RESOLUTION ORDER:

    When Python encounters a name, it searches in this exact order:

    L — Local:      Inside the current function
    E — Enclosing:  Inside any enclosing function (closure scope)
    G — Global:     Module-level names
    B — Built-in:   Python's built-in names (len, print, etc.)

    First match wins.  If not found in any scope → NameError.


HOW CLOSURES WORK:

    When an inner function references a variable from an outer function,
    Python creates a "closure".  The inner function carries a reference
    to the enclosing variable — NOT a copy of its value.

    def outer():
        x = 10              # x lives in outer's local scope
        def inner():
            return x        # inner "closes over" x
        return inner        # inner survives even after outer() returns
    
    fn = outer()
    fn()  # → 10  (x is still accessible via the closure!)

    Under the hood:
    - Python stores closed-over variables in "cell objects"
    - fn.__closure__    → tuple of cell objects
    - fn.__closure__[0].cell_contents  → the actual value (10)
    - fn.__code__.co_freevars → ('x',)  — names of closed-over variables

    CRITICAL: The closure holds a REFERENCE to the variable, not a snapshot.
    If the variable changes, the closure sees the new value!


THE `nonlocal` KEYWORD:

    By default, assigning to a variable in an inner function creates a
    NEW local variable (doesn't modify the enclosing one).

    def counter():
        count = 0
        def increment():
            count += 1      # UnboundLocalError! Python sees assignment → local
        return increment
    
    FIX: Use `nonlocal` to tell Python "this name is from enclosing scope":
    
    def counter():
        count = 0
        def increment():
            nonlocal count  # ← references the enclosing count
            count += 1
            return count
        return increment

THE `global` KEYWORD:

    Same idea but for module-level variables:
    
    total = 0
    def add(n):
        global total    # without this, `total += n` raises UnboundLocalError
        total += n
"""


# ── Proof: Inspecting closure internals ─────────────────────────────────────

def make_multiplier(factor):
    """Factory function that returns a closure."""
    def multiply(x):
        return x * factor
    return multiply


double = make_multiplier(2)
triple = make_multiplier(3)

# Uncomment to inspect:
# print(double(5))        # 10
# print(triple(5))        # 15
# print(double.__closure__)                    # (<cell ...>,)
# print(double.__closure__[0].cell_contents)   # 2
# print(double.__code__.co_freevars)           # ('factor',)


# ── Proof: Reference semantics (NOT a copy) ────────────────────────────────

def demonstrate_reference_semantics():
    """Shows that closures hold references, not copies."""
    data = []
    
    def append_and_return(item):
        data.append(item)   # modifies the SAME list object
        return data
    
    append_and_return("a")
    append_and_return("b")
    return data  # ['a', 'b'] — both calls modified the same list


# ─────────────────────────────────────────────────────────────────────────────
# SECTION 2: PRODUCTION-READY EXAMPLES
# ─────────────────────────────────────────────────────────────────────────────

# ── Example 1: Configuration Factory (real-world closure pattern) ───────────

def create_logger(service_name: str, min_level: int = 0):
    """
    Factory that creates a pre-configured logger closure.
    
    In production, this pattern is used for:
    - Pre-configure clients with API keys
    - Create specialized validators
    - Build partial-application functions without functools.partial
    """
    import sys
    from datetime import datetime

    levels = {0: "DEBUG", 1: "INFO", 2: "WARN", 3: "ERROR"}

    def log(level: int, message: str):
        if level >= min_level:
            timestamp = datetime.now().strftime("%H:%M:%S")
            level_name = levels.get(level, "UNKNOWN")
            output = f"[{timestamp}] [{service_name}] [{level_name}] {message}"
            print(output, file=sys.stderr if level >= 3 else sys.stdout)
            return output
        return None

    # Attach convenience methods via closure
    log.debug = lambda msg: log(0, msg)
    log.info = lambda msg: log(1, msg)
    log.warn = lambda msg: log(2, msg)
    log.error = lambda msg: log(3, msg)

    return log


# Usage:
# api_log = create_logger("API", min_level=1)
# db_log = create_logger("Database", min_level=2)
# api_log.info("Request received")    # prints
# api_log.debug("Parsing headers")    # skipped (below min_level)
# db_log.error("Connection timeout")  # prints to stderr


# ── Example 2: Memoization via closures (before you reach for lru_cache) ───

def memoize(func):
    """
    Closure-based memoization.  Demonstrates:
    - Closure captures `cache` dict
    - The returned function carries the cache for its entire lifetime
    - This IS how functools.lru_cache works conceptually
    """
    cache = {}

    def wrapper(*args):
        if args not in cache:
            cache[args] = func(*args)
        return cache[args]

    wrapper.cache = cache  # expose for debugging
    wrapper.cache_clear = lambda: cache.clear()
    wrapper.__name__ = func.__name__
    wrapper.__doc__ = func.__doc__
    return wrapper


@memoize
def fibonacci(n):
    """Recursive fibonacci — O(n) with memoization, O(2^n) without."""
    if n < 2:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)


# ── Example 3: State machine via closure ────────────────────────────────────

def create_state_machine(transitions: dict, initial_state: str):
    """
    Closure-based state machine.  The current state is captured
    in the closure — no class needed.

    transitions = {
        ('idle', 'start'):   'running',
        ('running', 'pause'): 'paused',
        ('paused', 'resume'): 'running',
        ('running', 'stop'):  'idle',
    }
    """
    current = [initial_state]  # list so we can mutate without nonlocal
    history = [initial_state]

    def transition(event: str) -> str:
        key = (current[0], event)
        if key not in transitions:
            raise ValueError(
                f"Invalid transition: {current[0]} + '{event}'. "
                f"Valid events: {[e for (s, e) in transitions if s == current[0]]}"
            )
        old = current[0]
        current[0] = transitions[key]
        history.append(current[0])
        return f"{old} → [{event}] → {current[0]}"

    transition.state = lambda: current[0]
    transition.history = lambda: list(history)
    return transition


# Usage:
# machine = create_state_machine({
#     ('idle', 'start'): 'running',
#     ('running', 'pause'): 'paused',
#     ('paused', 'resume'): 'running',
#     ('running', 'stop'): 'idle',
# }, initial_state='idle')
#
# print(machine('start'))   # idle → [start] → running
# print(machine('pause'))   # running → [pause] → paused
# print(machine.state())    # paused
# print(machine.history())  # ['idle', 'running', 'paused']


# ─────────────────────────────────────────────────────────────────────────────
# SECTION 3: COMMON PITFALLS — Top 3 Bugs Juniors Introduce
# ─────────────────────────────────────────────────────────────────────────────
"""
PITFALL 1: Late Binding in Loops (THE classic closure bug)
───────────────────────────────────────────────────────────────────────────
    functions = []
    for i in range(5):
        functions.append(lambda: i)     # all lambdas share the SAME i!
    
    [f() for f in functions]   # [4, 4, 4, 4, 4]  ← NOT [0, 1, 2, 3, 4]
    
    WHY: lambda captures a REFERENCE to i, not its value.
         By the time you call the lambdas, the loop is done and i == 4.
    
    FIX 1 — Default argument (captures VALUE at creation time):
        functions.append(lambda i=i: i)
    
    FIX 2 — Use a factory function:
        def make_fn(val):
            return lambda: val
        functions.append(make_fn(i))


PITFALL 2: Forgetting `nonlocal` for mutable rebinding
───────────────────────────────────────────────────────────────────────────
    def counter():
        count = 0
        def increment():
            count += 1       # UnboundLocalError!
            return count
        return increment
    
    WHY: Python sees `count = ...` (assignment) → treats count as LOCAL.
         But count is referenced before assignment in count += 1.
    
    FIX: Add `nonlocal count` at the top of increment().
    
    ALTERNATIVE: Use a mutable container: count = [0] → count[0] += 1
                 (this works because you're MUTATING, not REBINDING)


PITFALL 3: Closures keeping large objects alive (memory leaks)
───────────────────────────────────────────────────────────────────────────
    def process_data():
        huge_dataset = load_gb_of_data()   # 2 GB in memory
        
        def summarize():
            return len(huge_dataset)       # closure keeps huge_dataset alive!
        
        return summarize
    
    fn = process_data()  # huge_dataset is NEVER garbage collected
    
    FIX: Extract only what you need BEFORE the closure:
        def process_data():
            huge_dataset = load_gb_of_data()
            size = len(huge_dataset)
            del huge_dataset  # free memory
            
            def summarize():
                return size  # only captures the int
            return summarize
"""


# ── Proof of Pitfall 1 — Late binding demo ─────────────────────────────────

def late_binding_demo():
    """Demonstrates the classic loop closure bug and fix."""
    # BUG version
    buggy = [lambda: i for i in range(5)]
    buggy_results = [f() for f in buggy]  # [4, 4, 4, 4, 4]

    # FIXED version (default argument captures value)
    fixed = [lambda i=i: i for i in range(5)]
    fixed_results = [f() for f in fixed]  # [0, 1, 2, 3, 4]

    return buggy_results, fixed_results


# ─────────────────────────────────────────────────────────────────────────────
# SECTION 4: BROKEN CODE CHALLENGES — Fix These!
# ─────────────────────────────────────────────────────────────────────────────

# ── Challenge 1: Broken event handler registration ──────────────────────────
"""
PROBLEM: All buttons call the handler for the LAST button, not their own.
         This is the late-binding bug in a real UI scenario.

HINT:    - The loop variable `btn_name` is captured by reference
         - Two fixes: default argument or factory function
         - In frameworks (Tkinter, Flask), this is a VERY common bug
"""


class BrokenUI:
    def __init__(self):
        self.handlers = {}

    def register_buttons(self):
        button_names = ["save", "delete", "export", "print"]
        for btn_name in button_names:
            # BUG: All handlers will use the LAST value of btn_name
            self.handlers[btn_name] = lambda: f"Clicked: {btn_name}"

    def test(self):
        self.register_buttons()
        results = {name: handler() for name, handler in self.handlers.items()}
        return results
        # Returns: {'save': 'Clicked: print', 'delete': 'Clicked: print', ...}
        # Should: {'save': 'Clicked: save', 'delete': 'Clicked: delete', ...}


# ── Challenge 2: Broken counter with thread safety ─────────────────────────
"""
PROBLEM: This closure-based counter is not thread-safe.
         Multiple threads incrementing simultaneously lose counts.

HINT:    - `nonlocal count; count += 1` is read-modify-write (not atomic)
         - Add a threading.Lock inside the closure
         - Make sure the lock itself is in the enclosing scope
"""

import threading


def broken_make_counter():
    count = 0

    def increment():
        nonlocal count
        # BUG: Not thread-safe! Multiple threads can read same count
        current = count
        # Simulate slow operation
        # time.sleep(0.0001)
        count = current + 1
        return count

    def get_count():
        return count

    increment.get_count = get_count
    return increment


# ── Challenge 3: Closure memory leak ────────────────────────────────────────
"""
PROBLEM: Each call to create_processor() loads a huge dataset into memory
         and the returned closure keeps it alive forever.

HINT:    - Process the data and extract results BEFORE creating the closure
         - Only close over the small summary, not the raw data
         - Use del or reassignment to free the large object
"""


def broken_create_processor(data_source: str):
    """Creates a data processor — but leaks memory!"""

    # Simulate loading a large dataset (in reality this could be GBs)
    large_dataset = list(range(10_000_000))  # ~80MB for a list of 10M ints

    def get_statistics():
        # BUG: Closure keeps `large_dataset` alive even though we only
        # need aggregate stats
        return {
            "count": len(large_dataset),
            "sum": sum(large_dataset),
            "min": min(large_dataset),
            "max": max(large_dataset),
        }

    def get_sample(n=5):
        # BUG: Also keeps large_dataset alive
        import random
        return random.sample(large_dataset, min(n, len(large_dataset)))

    get_statistics.get_sample = get_sample
    return get_statistics


# ─────────────────────────────────────────────────────────────────────────────
# SECTION 5: REFACTORING CHALLENGE
# ─────────────────────────────────────────────────────────────────────────────
"""
REFACTORING CHALLENGE: Messy Callback System
─────────────────────────────────────────────

The class below uses repetitive callback registration with duplicated
state management.  Refactor using closures and factory functions so:

    1. Each event type has its own closure-based handler factory
    2. No repeated if/elif chains
    3. State (retry count, last error) is captured cleanly in closures
    4. Adding a new event type requires zero changes to core logic
"""


class MessyEventSystem:
    """Refactor me to use closures and factory functions!"""

    def __init__(self):
        self.retry_counts = {}
        self.last_errors = {}
        self.handlers = {}

    def handle_event(self, event_type: str, data: dict) -> str:
        if event_type == "payment":
            try:
                result = f"Processing payment of ${data.get('amount', 0)}"
                self.retry_counts["payment"] = 0
                return result
            except Exception as e:
                self.retry_counts.setdefault("payment", 0)
                self.retry_counts["payment"] += 1
                self.last_errors["payment"] = str(e)
                if self.retry_counts["payment"] < 3:
                    return self.handle_event("payment", data)
                return f"Payment failed after 3 retries: {e}"

        elif event_type == "notification":
            try:
                result = f"Sending notification: {data.get('message', '')}"
                self.retry_counts["notification"] = 0
                return result
            except Exception as e:
                self.retry_counts.setdefault("notification", 0)
                self.retry_counts["notification"] += 1
                self.last_errors["notification"] = str(e)
                if self.retry_counts["notification"] < 3:
                    return self.handle_event("notification", data)
                return f"Notification failed after 3 retries: {e}"

        elif event_type == "logging":
            try:
                result = f"Logged: [{data.get('level', 'INFO')}] {data.get('message', '')}"
                self.retry_counts["logging"] = 0
                return result
            except Exception as e:
                self.retry_counts.setdefault("logging", 0)
                self.retry_counts["logging"] += 1
                self.last_errors["logging"] = str(e)
                if self.retry_counts["logging"] < 3:
                    return self.handle_event("logging", data)
                return f"Logging failed after 3 retries: {e}"
        else:
            return f"Unknown event: {event_type}"


# ─────────────────────────────────────────────────────────────────────────────
# QUICK SELF-TEST
# ─────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("=" * 60)
    print("  08_closures_scoping.py — Self Test")
    print("=" * 60)

    # Test closure basics
    print("\n[Test] Closure internals:")
    assert double(5) == 10
    assert triple(5) == 15
    assert double.__closure__[0].cell_contents == 2
    assert double.__code__.co_freevars == ('factor',)
    print(f"  double(5) = {double(5)}, triple(5) = {triple(5)}")
    print(f"  Closed-over vars: {double.__code__.co_freevars}")

    # Test late binding demo
    print("\n[Test] Late binding bug:")
    buggy, fixed = late_binding_demo()
    assert buggy == [4, 4, 4, 4, 4]
    assert fixed == [0, 1, 2, 3, 4]
    print(f"  Buggy: {buggy}")
    print(f"  Fixed: {fixed}")

    # Test memoized fibonacci
    print("\n[Test] Memoized fibonacci:")
    assert fibonacci(10) == 55
    assert fibonacci(20) == 6765
    print(f"  fib(10) = {fibonacci(10)}, fib(20) = {fibonacci(20)}")
    print(f"  Cache size: {len(fibonacci.cache)}")

    # Test state machine
    print("\n[Test] Closure state machine:")
    machine = create_state_machine({
        ('idle', 'start'): 'running',
        ('running', 'pause'): 'paused',
        ('paused', 'resume'): 'running',
        ('running', 'stop'): 'idle',
    }, initial_state='idle')
    print(f"  {machine('start')}")
    print(f"  {machine('pause')}")
    print(f"  {machine('resume')}")
    assert machine.state() == 'running'
    print(f"  History: {machine.history()}")

    # Test logger factory
    print("\n[Test] Logger factory:")
    log = create_logger("TestService", min_level=1)
    result = log.info("Server started")
    assert "TestService" in result
    assert log.debug("hidden") is None  # below min_level

    print("\n✓ All closures & scoping tests passed!")
    print("=" * 60)
