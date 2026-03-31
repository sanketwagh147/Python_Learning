"""
================================================================================
  ITERTOOLS & FUNCTOOLS — From Fundamentals to Production-Ready Mastery
================================================================================
  Author: Senior Software Engineer Practice Guide
  Goal:   Master Python's functional programming toolkit — lazy iteration,
          higher-order functions, and clean data pipelines.
================================================================================
"""

# ─────────────────────────────────────────────────────────────────────────────
# SECTION 1: UNDER THE HOOD — How Itertools & Functools Work
# ─────────────────────────────────────────────────────────────────────────────
"""
ITERTOOLS — LAZY COMBINATORIC & ITERATION LIBRARY:

    Every itertools function returns an ITERATOR (lazy).  No computation
    happens until you consume elements.  This means:
    - Constant memory regardless of input size
    - Composable (chain iterators together)
    - Single-pass only (can't go back)

    Categories:
    ┌──────────────────┬──────────────────────────────────────────────────┐
    │  Infinite        │  count(), cycle(), repeat()                     │
    │  Terminating     │  chain(), islice(), takewhile(), dropwhile()    │
    │  Combinatoric    │  product(), permutations(), combinations()      │
    │  Grouping        │  groupby()                                      │
    │  Accumulating    │  accumulate()                                   │
    └──────────────────┴──────────────────────────────────────────────────┘

FUNCTOOLS — HIGHER-ORDER FUNCTION TOOLKIT:

    functools provides tools that take functions and return enhanced functions.

    Key tools:
    ┌──────────────────┬──────────────────────────────────────────────────┐
    │  lru_cache       │  Memoization with LRU eviction                  │
    │  cache           │  Unbounded memoization (Python 3.9+)            │
    │  partial         │  Pre-fill some arguments of a function          │
    │  reduce          │  Fold a sequence to a single value              │
    │  singledispatch  │  Generic function with type-based dispatch      │
    │  wraps           │  Preserve metadata of decorated functions       │
    │  total_ordering  │  Generate comparison methods from __eq__ + __lt__│
    │  cached_property │  One-time computed property (descriptor-based)  │
    └──────────────────┴──────────────────────────────────────────────────┘

    Under the hood:
    - lru_cache uses a doubly-linked list + dict for O(1) access/eviction
    - partial creates a new callable that stores args/kwargs
    - singledispatch uses a dict mapping types to implementations
    - wraps copies __name__, __doc__, __module__, __qualname__, __dict__,
      __wrapped__ from the original function to the wrapper
"""

import itertools
import functools
from typing import Iterator, Callable, Any


# ─────────────────────────────────────────────────────────────────────────────
# SECTION 2: PRODUCTION-READY EXAMPLES
# ─────────────────────────────────────────────────────────────────────────────

# ── Example 1: Data Pipeline with itertools (streaming ETL) ─────────────────

def streaming_etl_pipeline(raw_records: Iterator[dict]) -> Iterator[dict]:
    """
    Production-grade streaming data pipeline.
    Processes millions of records in constant memory.

    Pipeline:
        raw_records → filter invalid → normalize → deduplicate → batch
    """

    # Step 1: Filter out invalid records (lazy)
    valid = filter(lambda r: r.get("email") and r.get("name"), raw_records)

    # Step 2: Normalize (lazy transformation)
    normalized = (
        {
            "name": r["name"].strip().title(),
            "email": r["email"].strip().lower(),
            "active": r.get("active", True),
        }
        for r in valid
    )

    # Step 3: Deduplicate by email (keeps first occurrence)
    seen_emails = set()

    def deduplicate(records):
        for r in records:
            if r["email"] not in seen_emails:
                seen_emails.add(r["email"])
                yield r

    unique = deduplicate(normalized)

    # Step 4: Filter active users only
    active = filter(lambda r: r["active"], unique)

    return active


def batch_iterator(iterable: Iterator, batch_size: int) -> Iterator[list]:
    """
    Yield successive batches from an iterable.  Uses itertools.islice
    for memory-efficient chunking.
    """
    it = iter(iterable)
    while True:
        batch = list(itertools.islice(it, batch_size))
        if not batch:
            break
        yield batch


# Usage:
# records = ({"name": f"User {i}", "email": f"user{i}@test.com"} for i in range(1_000_000))
# pipeline = streaming_etl_pipeline(records)
# for batch in batch_iterator(pipeline, batch_size=100):
#     db.bulk_insert(batch)  # Insert 100 at a time, constant memory


# ── Example 2: functools.singledispatch (polymorphism without classes) ──────

@functools.singledispatch
def serialize(obj) -> str:
    """Generic serializer — dispatches based on argument type."""
    raise TypeError(f"Cannot serialize {type(obj).__name__}")


@serialize.register(str)
def _serialize_str(obj: str) -> str:
    return f'"{obj}"'


@serialize.register(int)
@serialize.register(float)
def _serialize_number(obj) -> str:
    return str(obj)


@serialize.register(list)
def _serialize_list(obj: list) -> str:
    items = ", ".join(serialize(item) for item in obj)
    return f"[{items}]"


@serialize.register(dict)
def _serialize_dict(obj: dict) -> str:
    pairs = ", ".join(f"{serialize(k)}: {serialize(v)}" for k, v in obj.items())
    return f"{{{pairs}}}"


@serialize.register(bool)
def _serialize_bool(obj: bool) -> str:
    return "true" if obj else "false"


@serialize.register(type(None))
def _serialize_none(obj) -> str:
    return "null"


# ── Example 3: functools.partial for configuration ──────────────────────────

import json


def api_request(method: str, url: str, headers: dict = None,
                timeout: int = 30, data: dict = None) -> dict:
    """Simulated API request function."""
    return {
        "method": method,
        "url": url,
        "headers": headers or {},
        "timeout": timeout,
        "data": data,
    }


# Create specialized versions using partial
get = functools.partial(api_request, "GET")
post = functools.partial(api_request, "POST")
auth_get = functools.partial(
    api_request, "GET",
    headers={"Authorization": "Bearer TOKEN123"}
)

# Usage:
# get("/api/users")                    # GET request with defaults
# post("/api/users", data={"name": "Sanket"})  # POST with data
# auth_get("/api/protected")           # Pre-authenticated GET


# ── Example 4: itertools.groupby for data aggregation ──────────────────────

def aggregate_sales_by_region(sales: list[dict]) -> dict:
    """
    Group sales data by region and compute totals.
    
    CRITICAL: itertools.groupby requires data to be SORTED by the key
    (it only groups consecutive elements with the same key).
    """
    # Must sort first!
    sorted_sales = sorted(sales, key=lambda s: s["region"])

    result = {}
    for region, group_iter in itertools.groupby(sorted_sales, key=lambda s: s["region"]):
        group = list(group_iter)  # consume the group iterator
        result[region] = {
            "total_sales": sum(s["amount"] for s in group),
            "count": len(group),
            "avg_sale": sum(s["amount"] for s in group) / len(group),
        }
    return result


# ── Example 5: itertools.accumulate for running totals ─────────────────────

def running_balance(transactions: list[float]) -> list[float]:
    """Compute running balance from list of deposits (+) and withdrawals (-)."""
    return list(itertools.accumulate(transactions))


def running_max(values: list) -> list:
    """Track running maximum — useful for stock price analysis."""
    return list(itertools.accumulate(values, max))


# ── Example 6: functools.lru_cache with proper usage ───────────────────────

@functools.lru_cache(maxsize=256)
def expensive_computation(n: int, multiplier: int = 1) -> int:
    """Simulates an expensive computation with caching."""
    # In production: DB query, API call, complex calculation
    import time
    time.sleep(0.001)  # simulate work
    return sum(i ** 2 for i in range(n)) * multiplier


# Cache inspection:
# expensive_computation(100)
# expensive_computation(100)  # cache hit!
# print(expensive_computation.cache_info())
#   CacheInfo(hits=1, misses=1, maxsize=256, currsize=1)
# expensive_computation.cache_clear()  # reset cache


# ── Example 7: Composable pipeline with itertools ──────────────────────────

def compose_pipeline(*functions):
    """
    Create a data pipeline by composing multiple transformation functions.
    Each function takes an iterable and returns an iterable (lazy).
    """
    def pipeline(data):
        result = data
        for fn in functions:
            result = fn(result)
        return result
    return pipeline


# Pipeline building blocks
def strip_whitespace(records):
    for r in records:
        yield {k: v.strip() if isinstance(v, str) else v for k, v in r.items()}

def filter_active(records):
    return filter(lambda r: r.get("active", True), records)

def add_timestamp(records):
    from datetime import datetime
    ts = datetime.now().isoformat()
    for r in records:
        yield {**r, "processed_at": ts}

# Compose:
# process = compose_pipeline(strip_whitespace, filter_active, add_timestamp)
# for record in process(raw_data_iterator):
#     save(record)


# ─────────────────────────────────────────────────────────────────────────────
# SECTION 3: COMMON PITFALLS — Top 3 Bugs Juniors Introduce
# ─────────────────────────────────────────────────────────────────────────────
"""
PITFALL 1: Consuming an iterator twice
───────────────────────────────────────────────────────────────────────────
    data = map(int, ["1", "2", "3"])
    total = sum(data)     # 6 ← works
    count = len(list(data))  # 0 ← empty! Iterator was exhausted!
    
    FIX: Convert to list first if you need multiple passes:
        data = list(map(int, ["1", "2", "3"]))
    
    OR: Use itertools.tee() to create independent copies:
        it1, it2 = itertools.tee(data)


PITFALL 2: Using groupby without sorting first
───────────────────────────────────────────────────────────────────────────
    data = [("a", 1), ("b", 2), ("a", 3)]
    for key, group in itertools.groupby(data, key=lambda x: x[0]):
        print(key, list(group))
    # Output: a [(a,1)], b [(b,2)], a [(a,3)]  ← TWO "a" groups!
    
    FIX: Sort first: data.sort(key=lambda x: x[0])
    
    ALTERNATIVE: Use collections.defaultdict(list) instead of groupby
    when data doesn't need to be sorted.


PITFALL 3: lru_cache with mutable arguments
───────────────────────────────────────────────────────────────────────────
    @lru_cache
    def process(data: list):  # TypeError: unhashable type: 'list'
        ...
    
    FIX: Convert to tuple: process(tuple(data))
    
    OR: Use a custom cache key:
        def process(data: list):
            return _process_cached(tuple(data))
        
        @lru_cache
        def _process_cached(data: tuple):
            return ...
"""


# ─────────────────────────────────────────────────────────────────────────────
# SECTION 4: BROKEN CODE CHALLENGES — Fix These!
# ─────────────────────────────────────────────────────────────────────────────

# ── Challenge 1: Iterator consumed prematurely ──────────────────────────────
"""
PROBLEM: The statistics function gives wrong results because
         the data iterator is consumed on the first operation.

HINT:    - sum() exhausts the iterator
         - After sum(), there's nothing left for min(), max(), len()
         - Three possible fixes: list, tee, or single-pass accumulation
"""


def broken_statistics(data_iter):
    """BUG: Iterator consumed on first pass!"""
    total = sum(data_iter)          # exhausts iterator
    minimum = min(data_iter)        # ERROR: empty iterator
    maximum = max(data_iter)        # ERROR: empty iterator
    count = sum(1 for _ in data_iter)  # ERROR: empty iterator
    return {
        "total": total,
        "min": minimum,
        "max": maximum,
        "count": count,
        "mean": total / count if count else 0,
    }


# ── Challenge 2: lru_cache memory leak ──────────────────────────────────────
"""
PROBLEM: This cached function keeps references to large objects forever,
         causing memory to grow unbounded.

HINT:    - lru_cache stores strong references to all arguments and return values
         - If you pass unique objects each time, cache grows without limit
         - Use maxsize parameter, or use weakref, or cache only the key
"""


@functools.lru_cache(maxsize=None)  # BUG: unbounded cache!
def broken_process_user(user_id: int, user_data: str) -> dict:
    """
    BUG: user_data changes frequently for the same user_id,
    causing the cache to store every version forever.
    """
    import hashlib
    return {
        "id": user_id,
        "hash": hashlib.sha256(user_data.encode()).hexdigest(),
        "processed": True,
    }


# Cache grows forever because (user_id, user_data) is always unique:
# broken_process_user(1, "version_1")  # cached
# broken_process_user(1, "version_2")  # NEW cache entry (different user_data)
# broken_process_user(1, "version_3")  # NEW cache entry...


# ── Challenge 3: groupby silently gives wrong results ──────────────────────
"""
PROBLEM: The sales report shows incorrect groupings — some regions
         appear multiple times with partial data.

HINT:    - itertools.groupby only groups CONSECUTIVE equal elements
         - The data isn't sorted by region
         - Also: the group iterator is consumed when you move to next key
"""


def broken_sales_report(sales):
    """BUG: Incorrect grouping due to unsorted data."""
    report = {}
    for region, group in itertools.groupby(sales, key=lambda s: s["region"]):
        # BUG 1: Data not sorted → multiple groups per region
        # BUG 2: If region already in report, it's overwritten, not merged
        items = list(group)
        report[region] = {
            "total": sum(s["amount"] for s in items),
            "count": len(items),
        }
    return report


# Test data (NOT sorted by region):
# broken_sales = [
#     {"region": "East", "amount": 100},
#     {"region": "West", "amount": 200},
#     {"region": "East", "amount": 150},  # ← Second "East" group overwrites first!
# ]
# broken_sales_report(broken_sales)
# Result: {'East': {'total': 150, 'count': 1}, 'West': ...}  ← East total wrong!


# ─────────────────────────────────────────────────────────────────────────────
# SECTION 5: REFACTORING CHALLENGE
# ─────────────────────────────────────────────────────────────────────────────
"""
REFACTORING CHALLENGE: Messy Report Generator
──────────────────────────────────────────────

Refactor using itertools and functools to:
    1. Use itertools.groupby for grouping (after sorting)
    2. Use functools.reduce or itertools.accumulate for totals
    3. Use itertools.chain to merge data sources
    4. Make it lazy/streaming so it works on huge datasets
    5. Use functools.partial to create specialized report generators
"""


def messy_report(orders: list, returns: list) -> dict:
    """Refactor me using itertools/functools!"""
    # Merge orders and returns (eagerly loads everything)
    all_transactions = []
    for o in orders:
        all_transactions.append({**o, "type": "order"})
    for r in returns:
        all_transactions.append({**r, "type": "return"})

    # Group by category (manual grouping with defaultdict behavior)
    by_category = {}
    for t in all_transactions:
        cat = t.get("category", "unknown")
        if cat not in by_category:
            by_category[cat] = []
        by_category[cat].append(t)

    # Compute stats per category
    report = {}
    for cat, transactions in by_category.items():
        total_orders = 0
        total_returns = 0
        order_count = 0
        return_count = 0
        for t in transactions:
            if t["type"] == "order":
                total_orders += t["amount"]
                order_count += 1
            else:
                total_returns += t["amount"]
                return_count += 1
        report[cat] = {
            "order_total": total_orders,
            "return_total": total_returns,
            "order_count": order_count,
            "return_count": return_count,
            "net": total_orders - total_returns,
        }

    # Sort by net revenue
    sorted_report = dict(sorted(report.items(), key=lambda x: x[1]["net"], reverse=True))
    return sorted_report


# ─────────────────────────────────────────────────────────────────────────────
# QUICK SELF-TEST
# ─────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("=" * 60)
    print("  09_itertools_functools.py — Self Test")
    print("=" * 60)

    # Test streaming ETL pipeline
    print("\n[Test] Streaming ETL pipeline:")
    raw = [
        {"name": "  alice ", "email": "Alice@Test.com", "active": True},
        {"name": "bob", "email": "bob@test.com", "active": True},
        {"name": "", "email": "invalid@test.com", "active": True},  # filtered: no name
        {"name": "alice again", "email": "ALICE@test.com", "active": True},  # deduplicated
        {"name": "charlie", "email": "charlie@test.com", "active": False},  # filtered: inactive
    ]
    results = list(streaming_etl_pipeline(iter(raw)))
    assert len(results) == 2  # alice + bob
    assert results[0]["name"] == "Alice"
    assert results[0]["email"] == "alice@test.com"
    print(f"  Processed {len(results)} valid records from {len(raw)} raw")

    # Test batch_iterator
    print("\n[Test] Batch iterator:")
    batches = list(batch_iterator(range(7), batch_size=3))
    assert batches == [[0, 1, 2], [3, 4, 5], [6]]
    print(f"  7 items in batches of 3: {batches}")

    # Test singledispatch serializer
    print("\n[Test] singledispatch serializer:")
    assert serialize("hello") == '"hello"'
    assert serialize(42) == "42"
    assert serialize([1, "a"]) == '[1, "a"]'
    assert serialize({"key": "val"}) == '{"key": "val"}'
    assert serialize(None) == "null"
    assert serialize(True) == "true"
    print(f"  serialize([1, 'a', None]) = {serialize([1, 'a', None])}")

    # Test partial API functions
    print("\n[Test] functools.partial:")
    result = get("/api/users")
    assert result["method"] == "GET"
    result = post("/api/data", data={"x": 1})
    assert result["method"] == "POST"
    print(f"  get('/api/users') → method={result['method']}")

    # Test groupby aggregation
    print("\n[Test] groupby aggregation:")
    sales = [
        {"region": "East", "amount": 100},
        {"region": "West", "amount": 200},
        {"region": "East", "amount": 150},
        {"region": "West", "amount": 50},
    ]
    agg = aggregate_sales_by_region(sales)
    assert agg["East"]["total_sales"] == 250
    assert agg["West"]["total_sales"] == 250
    print(f"  East total: {agg['East']['total_sales']}, West total: {agg['West']['total_sales']}")

    # Test running balance
    print("\n[Test] Running balance:")
    txns = [1000, -200, -50, 500, -100]
    balance = running_balance(txns)
    assert balance == [1000, 800, 750, 1250, 1150]
    print(f"  Transactions: {txns}")
    print(f"  Balance:      {balance}")

    # Test lru_cache
    print("\n[Test] lru_cache:")
    expensive_computation(50)
    expensive_computation(50)  # cache hit
    info = expensive_computation.cache_info()
    assert info.hits >= 1
    print(f"  Cache info: {info}")

    print("\n✓ All itertools/functools tests passed!")
    print("=" * 60)
