# Generators Practice Solutions

## Solution 1 - Stream Error Logs Lazily
Yield matching lines directly from the file iterator.

```python
def iter_error_lines(path, predicate=lambda line: "ERROR" in line):
    with open(path, "r", encoding="utf-8") as handle:
        for line in handle:
            if predicate(line):
                yield line.rstrip("\n")
```

## Solution 2 - Paginated CRM Export
Keep fetching until the cursor disappears.

```python
def iter_customers(fetch_page, start_cursor=None):
    cursor = start_cursor
    while True:
        payload = fetch_page(cursor)
        for customer in payload.get("items", []):
            yield customer
        cursor = payload.get("next_cursor")
        if not cursor:
            break
```

## Solution 3 - Normalize Large CSV Rows
Chain generators so each stage does one thing well.

```python
import csv


def cleaned_csv_rows(path):
    with open(path, newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            cleaned = {
                key.strip(): (value.strip().lower() or None) if isinstance(value, str) else value
                for key, value in row.items()
            }
            if cleaned.get("email"):
                yield cleaned
```

## Solution 4 - Merge Sorted Sensor Feeds
Use a heap so only one item from each source is in memory.

```python
import heapq


def merge_streams(*streams):
    heap = []
    iterators = [iter(stream) for stream in streams]
    for index, iterator in enumerate(iterators):
        try:
            item = next(iterator)
            heapq.heappush(heap, (item["timestamp"], index, item, iterator))
        except StopIteration:
            pass

    while heap:
        _, index, item, iterator = heapq.heappop(heap)
        yield item
        try:
            next_item = next(iterator)
            heapq.heappush(heap, (next_item["timestamp"], index, next_item, iterator))
        except StopIteration:
            pass
```

## Solution 5 - Backpressure-Aware Batch Builder
Track both size and elapsed time before deciding to flush.

```python
import time


def iter_batches(records, batch_size, max_wait_seconds):
    batch = []
    started = time.monotonic()
    for record in records:
        batch.append(record)
        elapsed = time.monotonic() - started
        if len(batch) >= batch_size or elapsed >= max_wait_seconds:
            yield batch
            batch = []
            started = time.monotonic()
    if batch:
        yield batch
```