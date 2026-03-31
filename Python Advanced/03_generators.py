"""
================================================================================
  GENERATORS — From Fundamentals to Production-Ready Mastery
================================================================================
  Author: Senior Software Engineer Practice Guide
  Goal:   Understand __next__/yield at the protocol level, use generators in
          production for memory-efficient data processing, avoid common pitfalls.
================================================================================
"""

# ─────────────────────────────────────────────────────────────────────────────
# SECTION 1: UNDER THE HOOD — The Iterator Protocol & yield
# ─────────────────────────────────────────────────────────────────────────────
"""
THE ITERATOR PROTOCOL:
    Any object that implements __iter__() and __next__() is an iterator.
    - __iter__() returns the iterator object itself
    - __next__() returns the next value, or raises StopIteration when done

A GENERATOR is a function that uses `yield`.  When called, it returns a
generator object — which automatically implements the iterator protocol.

When you write:

    def count_up(n):
        i = 0
        while i < n:
            yield i        # ← Pauses here, returns i
            i += 1         # ← Resumes here on next() call

Python does this internally:

    gen = count_up(3)           # Creates generator object (NOTHING executes yet!)
    gen.__next__()              # Executes until first yield → returns 0
    gen.__next__()              # Resumes after yield, loops → returns 1
    gen.__next__()              # Resumes after yield, loops → returns 2
    gen.__next__()              # Resumes, while condition fails → raises StopIteration

KEY INSIGHTS:
    1. The function body does NOT execute when you call it — only when you iterate
    2. yield SUSPENDS the function's state (local vars, instruction pointer)
    3. next() RESUMES execution from exactly where it left off
    4. When the function returns (or falls off the end), StopIteration is raised
    5. Generator objects are SINGLE-USE — once exhausted, they're done

MEMORY INSIGHT:
    A list stores ALL values in memory at once: [0, 1, 2, ..., 999999] → ~8MB
    A generator produces ONE value at a time: gen → ~120 bytes regardless of size
"""


# ── Proof: Manual iterator class vs generator function ──────────────────────

class RangeIterator:
    """Manual implementation of range() — shows __iter__ and __next__."""

    def __init__(self, start, stop, step=1):
        self.current = start
        self.stop = stop
        self.step = step

    def __iter__(self):
        """Returns self — the iterator IS the iterable."""
        return self

    def __next__(self):
        """Returns next value or raises StopIteration."""
        if self.current >= self.stop:
            raise StopIteration
        value = self.current
        self.current += self.step
        return value


# Equivalent generator (much simpler!)
def range_generator(start, stop, step=1):
    """Same behavior as RangeIterator but in 4 lines."""
    current = start
    while current < stop:
        yield current
        current += step


# Uncomment to test:
# print("--- Manual Iterator ---")
# for val in RangeIterator(0, 5):
#     print(val, end=" ")  # 0 1 2 3 4
# print()
#
# print("--- Generator ---")
# for val in range_generator(0, 5):
#     print(val, end=" ")  # 0 1 2 3 4
# print()


# ── yield from — delegating to sub-generators ──────────────────────────────

def flatten(nested_list):
    """
    Recursively flatten a nested list using `yield from`.
    
    `yield from iterable` is equivalent to:
        for item in iterable:
            yield item
    
    But yield from also properly propagates .send(), .throw(), and .close().
    """
    for item in nested_list:
        if isinstance(item, (list, tuple)):
            yield from flatten(item)  # delegate to recursive call
        else:
            yield item


# Uncomment:
# print(list(flatten([1, [2, [3, 4], 5], [6, 7]])))  # [1, 2, 3, 4, 5, 6, 7]


# ── Generator .send() — two-way communication ──────────────────────────────

def accumulator():
    """
    Generator that receives values via .send() and yields running totals.
    
    .send(value) resumes the generator AND sets the yield expression's value.
    First call must be .send(None) or next() to prime the generator.
    """
    total = 0
    while True:
        value = yield total  # yield current total, receive new value
        if value is None:
            break
        total += value


# Uncomment to test:
# acc = accumulator()
# next(acc)            # Prime the generator (advances to first yield) → 0
# print(acc.send(10))  # total=10 → yields 10
# print(acc.send(20))  # total=30 → yields 30
# print(acc.send(5))   # total=35 → yields 35


# ─────────────────────────────────────────────────────────────────────────────
# SECTION 2: PRODUCTION-READY EXAMPLES
# ─────────────────────────────────────────────────────────────────────────────
"""
Real-world scenario #1: Memory-efficient log file processing.
Process multi-GB log files without loading them into memory.
"""

import os
import time
import csv
import json
import threading
from io import StringIO
from typing import Generator, Iterator, Any
from dataclasses import dataclass


# ── Production Example 1: Streaming Log Processor ───────────────────────────

def read_log_lines(filepath: str) -> Generator[str, None, None]:
    """
    Memory-efficient line reader for large files.
    Yields one line at a time — never loads the whole file.
    """
    with open(filepath, "r") as f:
        for line in f:
            yield line.rstrip("\n")


def parse_log_entries(lines: Iterator[str]) -> Generator[dict, None, None]:
    """
    Parse raw log lines into structured dicts.
    Pipeline stage: filters out invalid lines.
    """
    for line_num, line in enumerate(lines, 1):
        # Example format: "2026-03-31 10:15:00 ERROR [auth] Login failed for user=sanket"
        parts = line.split(" ", 3)
        if len(parts) < 4:
            continue  # skip malformed lines

        yield {
            "line_num": line_num,
            "timestamp": f"{parts[0]} {parts[1]}",
            "level": parts[2],
            "message": parts[3],
        }


def filter_errors(entries: Iterator[dict]) -> Generator[dict, None, None]:
    """Pipeline stage: only yield ERROR and CRITICAL entries."""
    for entry in entries:
        if entry["level"] in ("ERROR", "CRITICAL"):
            yield entry


def batch(iterable: Iterator, size: int = 100) -> Generator[list, None, None]:
    """
    Collect items from an iterator into fixed-size batches.
    Last batch may be smaller.  Very useful for bulk DB inserts.
    """
    current_batch = []
    for item in iterable:
        current_batch.append(item)
        if len(current_batch) >= size:
            yield current_batch
            current_batch = []
    if current_batch:
        yield current_batch


# USAGE: Composable pipeline — each stage is lazy (processed one item at a time)
#
# lines   = read_log_lines("/var/log/app.log")     # lazy
# entries = parse_log_entries(lines)                 # lazy
# errors  = filter_errors(entries)                   # lazy
# batches = batch(errors, size=50)                   # lazy
#
# for error_batch in batches:
#     db.insert_many("error_logs", error_batch)      # only here does work happen
#
# Memory used: O(batch_size), NOT O(file_size)


# ── Production Example 2: Paginated API Data Fetcher ───────────────────────

def fetch_all_pages(base_url: str, page_size: int = 100) -> Generator[dict, None, None]:
    """
    Lazily fetch all pages from a paginated REST API.
    Yields individual items, handles pagination transparently.
    
    Consumer doesn't need to know about pagination at all:
    
        for user in fetch_all_pages("https://api.example.com/users"):
            process(user)
    """
    import urllib.request

    page = 1
    while True:
        url = f"{base_url}?page={page}&per_page={page_size}"
        # In production, use requests/httpx with proper error handling
        # response = requests.get(url)
        # data = response.json()

        # Simulated response for practice:
        data = {"items": [{"id": i} for i in range((page-1)*page_size, page*page_size)],
                "has_next": page < 5}

        if not data["items"]:
            break

        yield from data["items"]  # yield each item individually

        if not data.get("has_next", True):
            break
        page += 1


# ── Production Example 3: CSV Streaming Transformer ────────────────────────

def transform_csv(input_path: str, output_path: str, transform_fn) -> int:
    """
    Stream-process a CSV file row by row.  Memory usage: O(1 row).
    Returns number of rows processed.
    """
    def read_csv_rows(path: str) -> Generator[dict, None, None]:
        with open(path, "r", newline="") as f:
            reader = csv.DictReader(f)
            for row in reader:
                yield row

    def transform_rows(rows: Iterator[dict]) -> Generator[dict, None, None]:
        for row in rows:
            transformed = transform_fn(row)
            if transformed is not None:  # None = skip row
                yield transformed

    count = 0
    rows = read_csv_rows(input_path)
    transformed = transform_rows(rows)

    first_row = next(transformed, None)
    if first_row is None:
        return 0

    with open(output_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=first_row.keys())
        writer.writeheader()
        writer.writerow(first_row)
        count = 1
        for row in transformed:
            writer.writerow(row)
            count += 1

    return count


# ── Production Example 4: Windowed/Sliding Window Generator ────────────────

from collections import deque

def sliding_window(iterable, window_size: int):
    """
    Yield sliding windows of `window_size` over the iterable.
    
    Useful for: time-series analysis, running averages, anomaly detection.
    
    list(sliding_window([1,2,3,4,5], 3))
    → [(1,2,3), (2,3,4), (3,4,5)]
    """
    it = iter(iterable)
    window = deque(maxlen=window_size)

    # Fill the first window
    for _ in range(window_size):
        window.append(next(it))
    yield tuple(window)

    # Slide
    for item in it:
        window.append(item)  # deque auto-evicts oldest
        yield tuple(window)


def running_average(values, window_size: int = 5):
    """Compute running average using sliding_window generator."""
    for window in sliding_window(values, window_size):
        yield sum(window) / len(window)


# ─────────────────────────────────────────────────────────────────────────────
# SECTION 3: COMMON PITFALLS — Top 3 bugs juniors introduce
# ─────────────────────────────────────────────────────────────────────────────

# ┌─────────────────────────────────────────────────────────────────────────┐
# │ PITFALL #1: Exhausted generator reuse                                   │
# │                                                                         │
# │ Generators are SINGLE-USE.  Once exhausted, iterating again yields     │
# │ NOTHING — no error, just an empty loop.  This is a silent bug.         │
# └─────────────────────────────────────────────────────────────────────────┘

# BAD
def get_numbers():
    yield 1; yield 2; yield 3

# gen = get_numbers()
# first_pass  = list(gen)   # [1, 2, 3]
# second_pass = list(gen)   # [] ← EMPTY! Generator is exhausted!

# GOOD — create a new generator each time, or use itertools.tee
# Option 1: Call the function again
# first_pass  = list(get_numbers())
# second_pass = list(get_numbers())

# Option 2: Use a reusable iterable class
class ReusableRange:
    def __init__(self, n):
        self.n = n

    def __iter__(self):
        """Returns a NEW iterator every time — so it's reusable."""
        for i in range(self.n):
            yield i

# nums = ReusableRange(5)
# list(nums)  # [0, 1, 2, 3, 4]
# list(nums)  # [0, 1, 2, 3, 4] ← Works again!


# ┌─────────────────────────────────────────────────────────────────────────┐
# │ PITFALL #2: Generator with side effects + early termination            │
# │                                                                         │
# │ If you break out of a generator loop early, cleanup code AFTER yield   │
# │ may never run.  Use try/finally inside the generator.                  │
# └─────────────────────────────────────────────────────────────────────────┘

# BAD — cleanup never runs if consumer breaks early
def read_sensor_bad():
    print("  [SETUP] Connecting to sensor...")
    sensor = {"connected": True}
    for i in range(100):
        yield f"reading-{i}"
    # ← This only runs if ALL 100 items are consumed!
    print("  [CLEANUP] Disconnecting from sensor...")
    sensor["connected"] = False

# for reading in read_sensor_bad():
#     print(f"  Got: {reading}")
#     if reading == "reading-2":
#         break
# # "Disconnecting" is NEVER printed!

# GOOD — use try/finally for guaranteed cleanup
def read_sensor_good():
    print("  [SETUP] Connecting to sensor...")
    sensor = {"connected": True}
    try:
        for i in range(100):
            yield f"reading-{i}"
    finally:
        # This runs even if the consumer breaks, or calls .close()
        print("  [CLEANUP] Disconnecting from sensor...")
        sensor["connected"] = False


# ┌─────────────────────────────────────────────────────────────────────────┐
# │ PITFALL #3: Accidentally materializing a generator                     │
# │                                                                         │
# │ Wrapping a generator in list() defeats the entire purpose.             │
# │ Juniors do this because they want to "see" the data or get len().      │
# └─────────────────────────────────────────────────────────────────────────┘

# BAD — defeats the purpose of the generator
def process_large_file_bad(path: str):
    lines = list(read_log_lines(path))  # ← Loads ENTIRE file into memory!
    errors = list(filter(lambda l: "ERROR" in l, lines))  # ← Another full copy!
    return len(errors)

# GOOD — stay lazy, only count
def process_large_file_good(path: str):
    lines = read_log_lines(path)       # lazy
    errors = (l for l in lines if "ERROR" in l)  # lazy (generator expression)
    return sum(1 for _ in errors)      # counts without storing


# ─────────────────────────────────────────────────────────────────────────────
# SECTION 4: BROKEN CODE — Fix These! (Thread-Safety & Efficiency)
# ─────────────────────────────────────────────────────────────────────────────

"""
╔══════════════════════════════════════════════════════════════════════════════╗
║  PROBLEM 1: Fix the ThreadSafeBuffer generator                             ║
║                                                                             ║
║  A producer-consumer pattern using generators. Has 4 bugs:                 ║
║    1. NOT thread-safe — producer and consumer share a list unsafely       ║
║    2. Busy-waits (burns CPU) when buffer is empty                         ║
║    3. No way to signal "done" — consumer loops forever                    ║
║    4. Buffer grows unbounded — can OOM if producer is faster              ║
║                                                                             ║
║  Hints:                                                                    ║
║    - Use queue.Queue (thread-safe, with blocking get/put)                 ║
║    - Use a sentinel value (None) to signal "done"                         ║
║    - Queue(maxsize=N) blocks the producer when buffer is full             ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

# ── BROKEN CODE — DO NOT PEEK AT SOLUTION ──

import queue

class DataBuffer:
    def __init__(self):
        self.buffer = []  # ← Not thread-safe!
        self.done = False

    def produce(self, items):
        """Producer: adds items to the buffer."""
        for item in items:
            self.buffer.append(item)  # ← Race condition!
        self.done = True

    def consume(self):
        """Consumer generator: yields items from the buffer."""
        while True:
            if self.buffer:
                yield self.buffer.pop(0)  # ← Race condition! Also O(n)!
            elif self.done:
                break
            # ← Busy wait! Burns CPU when buffer is empty!

# buf = DataBuffer()
# # In thread 1: buf.produce(range(1000000))
# # In thread 2: for item in buf.consume(): process(item)


"""
╔══════════════════════════════════════════════════════════════════════════════╗
║  PROBLEM 2: Fix the chunked file reader                                    ║
║                                                                             ║
║  Reads a large file in chunks.  Has bugs:                                  ║
║    1. File handle is never closed if consumer breaks early                 ║
║    2. Empty chunks are yielded (when file size is exact multiple of chunk) ║
║    3. Binary mode not handled properly with encoding                      ║
║    4. No progress tracking                                                ║
║                                                                             ║
║  Hints:                                                                    ║
║    - Use try/finally to ensure file is closed                             ║
║    - Check `if chunk:` before yielding                                    ║
║    - Track bytes_read for progress                                        ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

# ── BROKEN CODE — DO NOT PEEK AT SOLUTION ──

def read_in_chunks(filepath: str, chunk_size: int = 8192):
    """Read a file in chunks of chunk_size bytes."""
    f = open(filepath, "rb")  # ← Never closed if consumer breaks early!
    while True:
        chunk = f.read(chunk_size)
        yield chunk  # ← Bug: yields empty bytes b"" at end of file!
        if not chunk:
            break     # ← Bug: break AFTER yielding empty chunk!
    f.close()  # ← Never reached if consumer breaks!

# for chunk in read_in_chunks("large_file.bin"):
#     if some_condition:
#         break  # ← File handle leaked!


"""
╔══════════════════════════════════════════════════════════════════════════════╗
║  PROBLEM 3: Fix the database cursor generator                              ║
║                                                                             ║
║  Streams rows from a database query using server-side cursors.  Has bugs:  ║
║    1. Cursor not closed on early exit → holds DB resources                 ║
║    2. Connection not returned to pool on exception                         ║
║    3. fetchmany() called with wrong size after partial read               ║
║    4. Generator doesn't support .close() for cleanup                      ║
║                                                                             ║
║  Hints:                                                                    ║
║    - Use try/finally inside the generator                                 ║
║    - Handle GeneratorExit explicitly                                      ║
║    - Return connection to pool in finally block                           ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

# ── BROKEN CODE (pseudo-code) ──

def stream_query(pool, query: str, batch_size: int = 1000):
    """Stream rows from a database query."""
    conn = pool.get_connection()  # ← Never returned if consumer breaks!
    cursor = conn.cursor()
    cursor.execute(query)

    while True:
        rows = cursor.fetchmany(batch_size)
        if not rows:
            break
        for row in rows:
            yield row

    cursor.close()  # ← Never reached if consumer breaks!
    pool.return_connection(conn)  # ← Never reached if consumer breaks!


# ─────────────────────────────────────────────────────────────────────────────
# SECTION 5: REFACTORING CHALLENGE
# ─────────────────────────────────────────────────────────────────────────────

"""
╔══════════════════════════════════════════════════════════════════════════════╗
║  REFACTORING CHALLENGE: Clean up this messy ETL function using generators  ║
║                                                                             ║
║  The function below loads ALL data into memory, processes it, then writes. ║
║  It crashes on large datasets (>1GB) with MemoryError.                    ║
║                                                                             ║
║  YOUR TASK:                                                                ║
║    1. Refactor into a pipeline of generators                               ║
║    2. Memory usage should be O(batch_size), not O(data_size)              ║
║    3. Each pipeline stage should be a separate generator function          ║
║    4. Handle errors in individual records without stopping the pipeline    ║
║    5. Add progress reporting without breaking the pipeline pattern         ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

# ── MESSY CODE TO REFACTOR ──

def etl_user_events(input_csv: str, output_json: str):
    """
    Extract user events from CSV, transform, load into JSON.
    Currently loads EVERYTHING into memory — crashes on large files.
    """
    # EXTRACT: Load ALL rows into memory
    all_rows = []
    with open(input_csv, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            all_rows.append(row)  # ← Stores entire file in memory!

    print(f"Loaded {len(all_rows)} rows")

    # TRANSFORM: Process ALL rows, store ALL results
    transformed = []
    error_count = 0
    for row in all_rows:
        try:
            # Parse and clean
            event = {
                "user_id": int(row["user_id"]),
                "event": row["event_type"].strip().lower(),
                "timestamp": row["created_at"],
                "amount": float(row.get("amount", 0)),
            }
            # Business rule: skip events with zero amount
            if event["amount"] <= 0 and event["event"] == "purchase":
                continue
            # Enrich
            event["amount_inr"] = event["amount"] * 83.5
            transformed.append(event)  # ← Another full copy in memory!
        except (ValueError, KeyError) as e:
            error_count += 1
            print(f"Error on row: {e}")

    print(f"Transformed {len(transformed)} rows, {error_count} errors")

    # LOAD: Write ALL at once
    with open(output_json, "w") as f:
        json.dump(transformed, f, indent=2)  # ← Builds entire JSON string in memory!

    print(f"Written to {output_json}")
    return len(transformed)


# ═════════════════════════════════════════════════════════════════════════════
# YOUR REFACTORED VERSION GOES HERE:
# ═════════════════════════════════════════════════════════════════════════════
#
# Hint: Create these generator pipeline stages:
#
#   def extract_rows(csv_path: str) -> Generator[dict, None, None]:
#       """Yield one row at a time from CSV."""
#       ...
#
#   def transform_events(rows: Iterator[dict]) -> Generator[dict, None, None]:
#       """Transform and filter rows. Skip bad rows with try/except."""
#       ...
#
#   def with_progress(items: Iterator, every_n: int = 1000) -> Generator:
#       """Yield items unchanged but print progress every N items."""
#       ...
#
#   def write_jsonl(events: Iterator[dict], output_path: str) -> int:
#       """Write as JSON Lines (one JSON object per line) — streamable format."""
#       ...
#
#   def etl_user_events_clean(input_csv: str, output_jsonl: str) -> int:
#       rows = extract_rows(input_csv)
#       events = transform_events(rows)
#       events = with_progress(events, every_n=10000)
#       return write_jsonl(events, output_jsonl)


# ─────────────────────────────────────────────────────────────────────────────
# SECTION 6: GENERATOR EXPRESSIONS & itertools — Power Tools
# ─────────────────────────────────────────────────────────────────────────────
"""
Generator expressions: like list comprehensions but lazy.

    # List comprehension — creates full list in memory
    squares_list = [x**2 for x in range(1_000_000)]   # ~8MB

    # Generator expression — lazy, ~120 bytes
    squares_gen  = (x**2 for x in range(1_000_000))

Key itertools for production:
    itertools.chain(*iterables)     — lazy concatenation
    itertools.islice(gen, n)        — take first n from generator
    itertools.groupby(sorted_iter)  — group consecutive equal elements
    itertools.tee(gen, n)           — split a generator into n independent copies
    itertools.starmap(fn, pairs)    — like map but unpacks arguments
    itertools.count(start, step)    — infinite counter
    itertools.cycle(iterable)       — infinite loop over iterable
    itertools.product(a, b)         — cartesian product (lazy)
"""

import itertools

# ── Practical examples ──────────────────────────────────────────────────────

def unique_elements(iterable):
    """Yield unique elements preserving order.  O(1) memory per unique element."""
    seen = set()
    for item in iterable:
        if item not in seen:
            seen.add(item)
            yield item


def take(n: int, iterable):
    """Take first n elements from any iterable (lazy)."""
    return itertools.islice(iterable, n)


def chunk_iterable(iterable, size: int):
    """Split an iterable into chunks of `size`.  Lazy.  Better than slicing a list."""
    it = iter(iterable)
    while True:
        first = next(it, None)
        if first is None:
            break
        rest = itertools.islice(it, size - 1)
        yield itertools.chain([first], rest)


# ── Infinite generators ────────────────────────────────────────────────────

def fibonacci():
    """Infinite Fibonacci sequence generator."""
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a + b


# Uncomment:
# print(list(take(10, fibonacci())))  # [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]


def prime_sieve():
    """
    Infinite prime number generator using an incremental sieve.
    Memory-efficient: only stores factors for numbers we've seen.
    """
    composites = {}
    n = 2
    while True:
        if n not in composites:
            yield n
            composites[n * n] = [n]  # First composite is n²
        else:
            for prime in composites[n]:
                composites.setdefault(n + prime, []).append(prime)
            del composites[n]  # No longer needed
        n += 1


# Uncomment:
# print(list(take(20, prime_sieve())))
# [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71]


if __name__ == "__main__":
    print("=" * 60)
    print("  Generators Practice Module")
    print("=" * 60)
    print()

    # Demo: Iterator protocol
    print("--- Manual Iterator vs Generator ---")
    print("Iterator:", list(RangeIterator(0, 5)))
    print("Generator:", list(range_generator(0, 5)))
    print()

    # Demo: Flatten
    print("--- Flatten nested list ---")
    nested = [1, [2, [3, 4], 5], [6, 7], 8]
    print(f"  Input:  {nested}")
    print(f"  Output: {list(flatten(nested))}")
    print()

    # Demo: Sliding window
    print("--- Sliding Window ---")
    data = [10, 20, 30, 40, 50, 60, 70]
    print(f"  Data: {data}")
    print(f"  Windows(3): {list(sliding_window(data, 3))}")
    print(f"  Running avg(3): {list(running_average(data, 3))}")
    print()

    # Demo: Exhausted generator pitfall
    print("--- Exhausted Generator Pitfall ---")
    gen = get_numbers()
    print(f"  First pass:  {list(gen)}")
    print(f"  Second pass: {list(gen)} ← EMPTY!")
    print()

    # Demo: Fibonacci
    print("--- First 15 Fibonacci numbers ---")
    print(f"  {list(take(15, fibonacci()))}")
    print()

    # Demo: First 20 primes
    print("--- First 20 Primes ---")
    print(f"  {list(take(20, prime_sieve()))}")
    print()

    # Demo: Memory comparison
    import sys
    list_version = [x**2 for x in range(100_000)]
    gen_version = (x**2 for x in range(100_000))
    print("--- Memory Comparison ---")
    print(f"  List of 100K squares: {sys.getsizeof(list_version):,} bytes")
    print(f"  Generator of 100K:    {sys.getsizeof(gen_version):,} bytes")
