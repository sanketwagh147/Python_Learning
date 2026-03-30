# Iterator Pattern — Question 3 (Hard)

## Problem: Database Query Result Iterator with Pagination

Build an iterator that lazily fetches paginated results from a simulated database, supporting filtering, mapping, and chaining (like a mini LINQ/Stream API).

### Requirements

#### PaginatedIterator
```python
class PaginatedIterator:
    """Fetches data in pages of `page_size` from a data source."""
    def __init__(self, data_source: DataSource, page_size: int = 10): ...
    def __iter__(self): ...
    def __next__(self): ...
```

The iterator fetches one page at a time from `DataSource.fetch_page(page_num, page_size) -> list[dict]`. When a page returns fewer items than `page_size`, iteration ends.

#### Chainable Operations
```python
class QueryIterator:
    def __init__(self, source: Iterable): ...
    def filter(self, predicate: Callable) -> QueryIterator: ...
    def map(self, transform: Callable) -> QueryIterator: ...
    def take(self, n: int) -> QueryIterator: ...
    def skip(self, n: int) -> QueryIterator: ...
    def collect(self) -> list: ...   # terminal operation
    def first(self) -> Any: ...      # terminal operation
    def count(self) -> int: ...      # terminal operation
```

### Expected Usage

```python
source = MockDataSource(total_records=1000)

# Lazily paginate, filter, and transform
results = (
    QueryIterator(PaginatedIterator(source, page_size=50))
    .filter(lambda r: r["age"] > 25)
    .filter(lambda r: r["active"])
    .map(lambda r: {"name": r["name"], "email": r["email"]})
    .take(10)
    .collect()
)
# Only fetched as many pages as needed to get 10 matching results!

print(source.pages_fetched)  # e.g., 3 (not all 20 pages)

# Get first matching
first = (
    QueryIterator(PaginatedIterator(source, page_size=50))
    .filter(lambda r: r["name"] == "Alice")
    .first()
)
```

### Constraints

- **Lazy evaluation**: `filter()`, `map()`, `take()`, `skip()` do NOT process data until a terminal operation (`collect`, `first`, `count`) is called.
- `PaginatedIterator` tracks how many pages were fetched (for testing laziness).
- `QueryIterator` must work with ANY iterable source, not just `PaginatedIterator`.
- `take(10)` should stop fetching after 10 items are found (short-circuit).
- All operations return a new `QueryIterator` (immutable chaining).

### Think About

- How does this compare to Python generators with `itertools`?
- How does this relate to Java Streams or C# LINQ?
- What's the memory complexity of this approach vs loading all 1000 records?
