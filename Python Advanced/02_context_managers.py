"""
================================================================================
  CONTEXT MANAGERS — From Fundamentals to Production-Ready Mastery
================================================================================
  Author: Senior Software Engineer Practice Guide
  Goal:   Understand __enter__/__exit__ at the protocol level, use context
          managers in production, avoid common pitfalls, and fix broken code.
================================================================================
"""

# ─────────────────────────────────────────────────────────────────────────────
# SECTION 1: UNDER THE HOOD — The Context Manager Protocol
# ─────────────────────────────────────────────────────────────────────────────
"""
When you write:

    with SomeManager() as value:
        do_stuff(value)

Python does this:

    manager = SomeManager()             # Step 1: Create the manager object
    value = manager.__enter__()          # Step 2: Call __enter__, bind result to `value`
    try:
        do_stuff(value)                  # Step 3: Run the body
    except Exception as exc:
        # Step 4a: If exception, pass it to __exit__
        if not manager.__exit__(type(exc), exc, exc.__traceback__):
            raise                        # If __exit__ returns False/None → re-raise
    else:
        # Step 4b: If no exception, call __exit__ with (None, None, None)
        manager.__exit__(None, None, None)

KEY INSIGHTS:
    1. __enter__ returns the value bound to `as variable`
    2. __exit__ ALWAYS runs (like a finally block)
    3. __exit__ receives exception info → can SUPPRESS exceptions by returning True
    4. __exit__ returning False/None → exception propagates normally
"""


# ── Proof: Custom class implementing the protocol ───────────────────────────

class ManagedResource:
    """Demonstrates the full __enter__/__exit__ lifecycle."""

    def __init__(self, name: str):
        self.name = name
        print(f"  [__init__] Resource '{name}' created")

    def __enter__(self):
        """Called when entering 'with' block. Returns self (or any value)."""
        print(f"  [__enter__] Resource '{self.name}' acquired")
        self.acquired = True
        return self  # ← this is what gets bound to `as variable`

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Called when exiting 'with' block — ALWAYS, even on exception.

        Args:
            exc_type: Exception class (or None if no exception)
            exc_val:  Exception instance (or None)
            exc_tb:   Traceback object (or None)

        Returns:
            True  → suppress the exception (dangerous, use sparingly!)
            False → let the exception propagate (default, safe)
        """
        print(f"  [__exit__] Resource '{self.name}' released")
        if exc_type:
            print(f"  [__exit__] Exception caught: {exc_type.__name__}: {exc_val}")
        self.acquired = False
        return False  # Don't suppress exceptions

    def do_work(self):
        print(f"  [do_work] Using resource '{self.name}'")


# Uncomment to test:
# print("--- Normal flow ---")
# with ManagedResource("DB Connection") as res:
#     res.do_work()
# print()
#
# print("--- Exception flow ---")
# try:
#     with ManagedResource("File Handle") as res:
#         res.do_work()
#         raise ValueError("Something went wrong!")
# except ValueError:
#     print("  Exception propagated correctly")


# ── The @contextmanager shortcut (generator-based) ──────────────────────────

from contextlib import contextmanager

@contextmanager
def managed_resource_simple(name: str):
    """
    Same as ManagedResource class but using a generator.
    
    Everything BEFORE yield  → __enter__ logic
    The yielded value        → bound to `as variable`
    Everything AFTER yield   → __exit__ logic (in the finally block)
    """
    print(f"  [enter] Acquiring '{name}'")
    resource = {"name": name, "acquired": True}
    try:
        yield resource  # ← control passes to the `with` body here
    finally:
        print(f"  [exit] Releasing '{name}'")
        resource["acquired"] = False


# ─────────────────────────────────────────────────────────────────────────────
# SECTION 2: PRODUCTION-READY EXAMPLE — DatabaseTransaction
# ─────────────────────────────────────────────────────────────────────────────
"""
Real-world scenario: Manage database transactions with automatic
commit on success and rollback on failure.  Thread-safe, with
savepoint support for nested transactions.
"""

import threading
import time
import logging

logger = logging.getLogger(__name__)


class DatabaseTransaction:
    """
    Production-grade transaction context manager.
    
    Features:
        - Auto-commit on success, auto-rollback on failure
        - Nested transaction support via savepoints
        - Thread-safe (each thread gets its own transaction state)
        - Configurable isolation level
        - Timing and logging
    
    Usage:
        db = DatabaseConnection(...)
        
        with DatabaseTransaction(db) as txn:
            txn.execute("INSERT INTO users (name) VALUES ('Sanket')")
            txn.execute("UPDATE accounts SET balance = balance - 100")
            # Auto-commits if no exception
            # Auto-rollbacks if exception occurs
    """

    _nesting_level = threading.local()  # per-thread nesting counter

    def __init__(self, connection, isolation_level="READ COMMITTED"):
        self.connection = connection
        self.isolation_level = isolation_level
        self._savepoint_name = None
        self._start_time = None

    def __enter__(self):
        # Track nesting per-thread
        if not hasattr(self._nesting_level, 'depth'):
            self._nesting_level.depth = 0

        self._nesting_level.depth += 1
        self._start_time = time.monotonic()

        if self._nesting_level.depth == 1:
            # Outermost transaction — BEGIN
            logger.info(f"BEGIN TRANSACTION (isolation={self.isolation_level})")
            self.connection.execute(f"SET TRANSACTION ISOLATION LEVEL {self.isolation_level}")
            self.connection.execute("BEGIN")
        else:
            # Nested — use SAVEPOINT
            self._savepoint_name = f"sp_{self._nesting_level.depth}_{id(self)}"
            logger.info(f"SAVEPOINT {self._savepoint_name}")
            self.connection.execute(f"SAVEPOINT {self._savepoint_name}")

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        elapsed = time.monotonic() - self._start_time

        try:
            if exc_type is not None:
                # Error path
                if self._savepoint_name:
                    logger.warning(f"ROLLBACK TO {self._savepoint_name} ({elapsed:.3f}s)")
                    self.connection.execute(f"ROLLBACK TO SAVEPOINT {self._savepoint_name}")
                else:
                    logger.error(f"ROLLBACK ({elapsed:.3f}s) due to {exc_type.__name__}: {exc_val}")
                    self.connection.execute("ROLLBACK")
            else:
                # Success path
                if self._savepoint_name:
                    logger.info(f"RELEASE SAVEPOINT {self._savepoint_name} ({elapsed:.3f}s)")
                    self.connection.execute(f"RELEASE SAVEPOINT {self._savepoint_name}")
                else:
                    logger.info(f"COMMIT ({elapsed:.3f}s)")
                    self.connection.execute("COMMIT")
        finally:
            self._nesting_level.depth -= 1

        return False  # Never suppress exceptions

    def execute(self, query: str, params=None):
        """Execute a query within this transaction."""
        logger.debug(f"  EXEC: {query}")
        return self.connection.execute(query, params)


# ── Another production example: TimedBlock for profiling ────────────────────

class TimedBlock:
    """
    Context manager that times a code block and logs results.
    
    Usage:
        with TimedBlock("data_processing"):
            process_data()
        # Prints: [TimedBlock] data_processing took 1.234s
    """

    def __init__(self, label: str, warn_threshold: float = 5.0):
        self.label = label
        self.warn_threshold = warn_threshold
        self.elapsed = None

    def __enter__(self):
        self.start = time.monotonic()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.elapsed = time.monotonic() - self.start
        level = "WARNING" if self.elapsed > self.warn_threshold else "INFO"
        status = "FAILED" if exc_type else "OK"
        print(f"[TimedBlock][{level}] {self.label} {status} in {self.elapsed:.4f}s")
        return False


# ── Production: FileTransaction — atomic file writes ────────────────────────

import os
import tempfile

class FileTransaction:
    """
    Atomic file write — either the full content is written or nothing changes.
    
    Uses write-to-temp + rename strategy (rename is atomic on most filesystems).
    
    Usage:
        with FileTransaction("/path/to/config.json") as f:
            json.dump(config, f)
        # File is atomically replaced only on success
    """

    def __init__(self, filepath: str, mode: str = "w"):
        self.filepath = filepath
        self.mode = mode
        self._tmpfile = None
        self._tmppath = None

    def __enter__(self):
        dir_name = os.path.dirname(self.filepath) or "."
        fd, self._tmppath = tempfile.mkstemp(dir=dir_name, suffix=".tmp")
        self._tmpfile = os.fdopen(fd, self.mode)
        return self._tmpfile

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._tmpfile.close()

        if exc_type is None:
            # Success → atomic rename
            os.replace(self._tmppath, self.filepath)
        else:
            # Failure → clean up temp file
            try:
                os.unlink(self._tmppath)
            except OSError:
                pass

        return False  # Don't suppress exceptions


# ─────────────────────────────────────────────────────────────────────────────
# SECTION 3: COMMON PITFALLS — Top 3 bugs juniors introduce
# ─────────────────────────────────────────────────────────────────────────────

# ┌─────────────────────────────────────────────────────────────────────────┐
# │ PITFALL #1: __exit__ returning True accidentally (suppressing errors)  │
# │                                                                         │
# │ If __exit__ returns True, the exception is SILENTLY SWALLOWED.         │
# │ This is almost never what you want.  It makes bugs invisible.          │
# └─────────────────────────────────────────────────────────────────────────┘

# BAD — suppresses ALL exceptions!
class BadConnection:
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        print("Cleaning up...")
        return True  # ← DANGER: ALL exceptions are silently eaten!

# with BadConnection():
#     raise RuntimeError("Critical error!")
# print("This runs — the error was swallowed!")  # ← BAD

# GOOD — always return False (or omit the return, which returns None → falsy)
class GoodConnection:
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        print("Cleaning up...")
        return False  # ← Exceptions propagate normally


# ┌─────────────────────────────────────────────────────────────────────────┐
# │ PITFALL #2: @contextmanager — forgetting the try/finally               │
# │                                                                         │
# │ Without try/finally, cleanup code NEVER runs if the body raises.       │
# └─────────────────────────────────────────────────────────────────────────┘

# BAD — cleanup skipped on exception
@contextmanager
def open_resource_bad(name):
    print(f"Acquiring {name}")
    resource = {"name": name}
    yield resource
    # ← This line NEVER executes if the with-body raises!
    print(f"Releasing {name}")

# GOOD — cleanup always runs
@contextmanager
def open_resource_good(name):
    print(f"Acquiring {name}")
    resource = {"name": name}
    try:
        yield resource
    finally:
        # ← This ALWAYS runs, even if the with-body raises
        print(f"Releasing {name}")


# ┌─────────────────────────────────────────────────────────────────────────┐
# │ PITFALL #3: Returning self vs returning something useful from __enter__│
# │                                                                         │
# │ __enter__ can return ANY value — not just self.                        │
# │ Juniors forget that `as variable` binds to __enter__'s return value,   │
# │ NOT to the context manager object itself.                              │
# └─────────────────────────────────────────────────────────────────────────┘

# CONFUSING — __enter__ returns None implicitly
class BadFileManager:
    def __init__(self, path):
        self.path = path

    def __enter__(self):
        self.file = open(self.path, "r")
        # ← Forgot to return! Returns None.

    def __exit__(self, *args):
        self.file.close()

# with BadFileManager("test.txt") as f:
#     f.read()  # ← AttributeError: 'NoneType' has no attribute 'read'

# CORRECT — return the useful object
class GoodFileManager:
    def __init__(self, path):
        self.path = path

    def __enter__(self):
        self.file = open(self.path, "r")
        return self.file  # ← User gets the file object

    def __exit__(self, *args):
        self.file.close()


# ─────────────────────────────────────────────────────────────────────────────
# SECTION 4: BROKEN CODE — Fix These! (Thread-Safety & Efficiency)
# ─────────────────────────────────────────────────────────────────────────────

"""
╔══════════════════════════════════════════════════════════════════════════════╗
║  PROBLEM 1: Fix the ConnectionPool context manager                         ║
║                                                                             ║
║  This connection pool has 4 bugs:                                          ║
║    1. NOT thread-safe — multiple threads can grab the same connection      ║
║    2. Connections are never returned to the pool on exception              ║
║    3. No timeout — blocks forever if pool is exhausted                     ║
║    4. __enter__ returns self instead of the connection                     ║
║                                                                             ║
║  Hints:                                                                    ║
║    - Use threading.Semaphore for pool size limiting                        ║
║    - Use a Queue (thread-safe) instead of a plain list                    ║
║    - __exit__ must ALWAYS return the connection (use finally pattern)      ║
║    - __enter__ should return the connection object                        ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

# ── BROKEN CODE — DO NOT PEEK AT SOLUTION ──

class ConnectionPool:
    def __init__(self, max_connections=5):
        self.pool = []
        self.max_connections = max_connections
        for i in range(max_connections):
            self.pool.append(f"Connection-{i}")

    def __enter__(self):
        if not self.pool:
            raise RuntimeError("No connections available")
        self.current = self.pool.pop()  # ← Not thread-safe!
        return self  # ← Bug: should return self.current

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:  # ← Bug: connection only returned on success!
            self.pool.append(self.current)
        return True  # ← Bug: suppresses ALL exceptions!

# pool = ConnectionPool(max_connections=2)
# with pool as conn:
#     print(f"Using {conn}")        # prints "Using <ConnectionPool object>" ← WRONG
#     raise ValueError("oops")      # connection leaked, exception suppressed!


"""
╔══════════════════════════════════════════════════════════════════════════════╗
║  PROBLEM 2: Fix the TempDirectory context manager                          ║
║                                                                             ║
║  Creates a temporary directory, cleans it up on exit.  Has bugs:           ║
║    1. Cleanup can fail silently if directory has read-only files           ║
║    2. __exit__ swallows exceptions from the with-body                     ║
║    3. Race condition: another process could create same dir name           ║
║    4. No handling of cleanup failure (just crashes)                        ║
║                                                                             ║
║  Hints:                                                                    ║
║    - Use tempfile.mkdtemp() for unique directory names                    ║
║    - Use shutil.rmtree with onerror handler for robust cleanup            ║
║    - Separate cleanup errors from business logic errors                    ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

# ── BROKEN CODE — DO NOT PEEK AT SOLUTION ──

import shutil

class TempDirectory:
    def __init__(self, prefix="tmp_"):
        self.path = f"/tmp/{prefix}{os.getpid()}"  # ← Bug: predictable, race condition

    def __enter__(self):
        os.makedirs(self.path)
        return self.path

    def __exit__(self, exc_type, exc_val, exc_tb):
        try:
            shutil.rmtree(self.path)  # ← Crashes on read-only files
        except Exception:
            pass  # ← Silently ignores cleanup failure
        return True  # ← Bug: suppresses exceptions from with-body!


"""
╔══════════════════════════════════════════════════════════════════════════════╗
║  PROBLEM 3: Fix the RedisLock distributed lock                             ║
║                                                                             ║
║  Implements a distributed lock using Redis.  Has bugs:                     ║
║    1. Lock can be released by a different thread/process (no ownership)    ║
║    2. No TTL — if process crashes, lock is held forever (deadlock)        ║
║    3. acquire + set is not atomic (race between check and set)            ║
║    4. __exit__ doesn't handle the case where lock was already expired     ║
║                                                                             ║
║  Hints:                                                                    ║
║    - Use a unique token (UUID) to prove lock ownership                    ║
║    - Use Redis SET with NX + EX for atomic acquire-with-TTL              ║
║    - Use a Lua script for atomic check-and-delete on release              ║
║    - Handle the case where the lock expired before we release it          ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

# ── BROKEN CODE (pseudo-code, no actual Redis needed) ──

import uuid

class RedisLock:
    """Simulated Redis distributed lock — fix the logic bugs."""

    def __init__(self, redis_client, lock_name, timeout=10):
        self.redis = redis_client
        self.lock_name = lock_name
        self.timeout = timeout

    def __enter__(self):
        # Bug: check-then-set is NOT atomic (race condition)
        if not self.redis.get(self.lock_name):
            self.redis.set(self.lock_name, "locked")  # ← No TTL! No ownership token!
        else:
            raise TimeoutError("Lock is held by another process")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        # Bug: any process can delete any lock (no ownership check)
        self.redis.delete(self.lock_name)
        return False


# ─────────────────────────────────────────────────────────────────────────────
# SECTION 5: REFACTORING CHALLENGE
# ─────────────────────────────────────────────────────────────────────────────

"""
╔══════════════════════════════════════════════════════════════════════════════╗
║  REFACTORING CHALLENGE: Clean up this messy function using context managers║
║                                                                             ║
║  The function below manually manages multiple resources with nested        ║
║  try/finally blocks.  It's fragile and hard to read.                      ║
║                                                                             ║
║  YOUR TASK:                                                                ║
║    1. Create context managers for each resource (file, db, lock)           ║
║    2. Refactor the function to use `with` statements                      ║
║    3. The function body should be clean and flat (~5 lines)               ║
║    4. Handle partial failures gracefully                                   ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

# ── MESSY CODE TO REFACTOR ──

def export_user_data(user_id: int, output_path: str):
    """Export user data to a file with locking and database access."""
    lock_acquired = False
    db_conn = None
    output_file = None

    try:
        # Acquire lock
        import fcntl
        lock_file = open(f"/tmp/export_{user_id}.lock", "w")
        try:
            fcntl.flock(lock_file, fcntl.LOCK_EX | fcntl.LOCK_NB)
            lock_acquired = True
        except IOError:
            raise RuntimeError(f"Export already in progress for user {user_id}")

        # Open database
        import sqlite3
        db_conn = sqlite3.connect("users.db")
        cursor = db_conn.cursor()

        # Open output file
        output_file = open(output_path, "w")

        # Do the actual work
        cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
        rows = cursor.fetchall()
        for row in rows:
            output_file.write(str(row) + "\n")

        db_conn.commit()

    except Exception:
        if db_conn:
            try:
                db_conn.rollback()
            except Exception:
                pass
        raise

    finally:
        if output_file:
            try:
                output_file.close()
            except Exception:
                pass
        if db_conn:
            try:
                db_conn.close()
            except Exception:
                pass
        if lock_acquired:
            try:
                import fcntl
                fcntl.flock(lock_file, fcntl.LOCK_UN)
                lock_file.close()
                os.unlink(lock_file.name)
            except Exception:
                pass


# ═════════════════════════════════════════════════════════════════════════════
# YOUR REFACTORED VERSION GOES HERE:
# ═════════════════════════════════════════════════════════════════════════════
#
# Hint: Create these context managers, then the function becomes:
#
#   @contextmanager
#   def file_lock(user_id): ...
#
#   @contextmanager
#   def db_transaction(db_path): ...
#
#   def export_user_data_clean(user_id: int, output_path: str):
#       with file_lock(user_id), \
#            db_transaction("users.db") as cursor, \
#            open(output_path, "w") as output_file:
#           rows = cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchall()
#           for row in rows:
#               output_file.write(str(row) + "\n")


# ─────────────────────────────────────────────────────────────────────────────
# SECTION 6: ADVANCED — contextlib utilities you should know
# ─────────────────────────────────────────────────────────────────────────────
"""
The contextlib module has powerful utilities beyond @contextmanager:

1. contextlib.suppress(*exceptions)
   - Suppresses specified exceptions (use sparingly!)
   
   with suppress(FileNotFoundError):
       os.remove("maybe_exists.tmp")

2. contextlib.redirect_stdout / redirect_stderr
   - Redirects output to a file or StringIO
   
   from io import StringIO
   f = StringIO()
   with redirect_stdout(f):
       print("captured!")
   output = f.getvalue()

3. contextlib.ExitStack
   - Manages a dynamic number of context managers
   
   with ExitStack() as stack:
       files = [stack.enter_context(open(f)) for f in file_list]
       # ALL files are closed when the block exits, even on error

4. contextlib.closing(thing)
   - Calls thing.close() on exit (for objects without __exit__)
   
   with closing(urlopen("https://example.com")) as page:
       content = page.read()

5. contextlib.asynccontextmanager (Python 3.10+)
   - Async version of @contextmanager for async with
"""

from contextlib import suppress, ExitStack

# Example: ExitStack for dynamic resource management
def process_multiple_files(file_paths: list[str]):
    """Process N files, ensuring ALL are properly closed."""
    with ExitStack() as stack:
        files = [stack.enter_context(open(path)) for path in file_paths]
        for f in files:
            print(f"Processing: {f.name}")
            # If ANY processing fails, ALL files are still closed


if __name__ == "__main__":
    print("=" * 60)
    print("  Context Manager Practice Module")
    print("=" * 60)
    print()

    # Demo: ManagedResource lifecycle
    print("--- Normal flow ---")
    with ManagedResource("DB Connection") as res:
        res.do_work()
    print()

    print("--- Exception flow ---")
    try:
        with ManagedResource("File Handle") as res:
            res.do_work()
            raise ValueError("Something went wrong!")
    except ValueError:
        print("  Exception propagated correctly ✓")
    print()

    # Demo: TimedBlock
    print("--- TimedBlock demo ---")
    with TimedBlock("sleep_test") as timer:
        time.sleep(0.1)
    print(f"  Elapsed: {timer.elapsed:.4f}s")
