# Generators Practice Problems

These problems move from lazy file handling to large-scale streaming pipelines.

## Problem 1 - Stream Error Logs Lazily

Scenario: A support script needs to scan a 15 GB application log and extract only error lines.

Build a generator that:

- reads the file lazily line by line
- yields only lines matching an error predicate
- strips trailing newlines
- does not load the whole file into memory

## Problem 2 - Paginated CRM Export

Scenario: Your CRM API returns customers page by page, but the analytics team wants a simple iterable over all records.

Build a generator that:

- keeps requesting pages until the API returns no next cursor
- yields customer records one at a time
- tolerates transient empty pages
- makes it easy to resume from a known cursor

## Problem 3 - Normalize Large CSV Rows

Scenario: A data-import pipeline receives huge CSV files and must normalize each row before validation.

Build a generator pipeline that:

- reads rows lazily from the CSV
- trims whitespace, standardizes casing, and converts empty strings to `None`
- skips rows that fail a light validation rule
- yields clean dictionaries downstream

## Problem 4 - Merge Sorted Sensor Feeds

Scenario: A monitoring platform receives individually sorted event streams from several factories.

Build a generator that:

- merges multiple sorted iterables by timestamp
- yields a single time-ordered stream
- handles exhausted inputs cleanly
- keeps memory usage near constant regardless of stream length

## Problem 5 - Backpressure-Aware Batch Builder

Scenario: An event-ingestion worker receives a stream of records but should flush batches either when they reach a size limit or when a time window expires.

Build a generator that:

- groups incoming records into batches lazily
- flushes on size or elapsed time
- yields final partial batches at shutdown
- can be reused in downstream ETL code
