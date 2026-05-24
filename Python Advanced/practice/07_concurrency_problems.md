# Concurrency Practice Problems

These problems progress from simple I/O parallelism to hybrid concurrency design.

## Problem 1 - Parallel Receipt Downloads

Scenario: A finance tool needs to download hundreds of receipt PDFs from a vendor API.

Choose and implement a concurrent design that:

- improves throughput for I/O-bound work
- limits the number of concurrent requests
- collects successes and failures separately
- avoids shared-state bugs in the result collector

## Problem 2 - Producer-Consumer Invoice Pipeline

Scenario: An invoicing system receives invoice ids from a queue, enriches them, and writes results to storage.

Build a concurrent pipeline that:

- uses a thread-safe queue between producers and workers
- supports graceful shutdown
- tracks failed items without killing the whole pipeline
- allows the main thread to wait for completion

## Problem 3 - Async API Sync with Semaphores

Scenario: A customer sync job makes tens of thousands of outbound HTTP calls to a CRM with strict rate limits.

Build an asyncio-based solution that:

- caps concurrency with a semaphore
- retries transient failures
- returns structured results instead of printing from tasks
- uses `async with` where resource cleanup matters

## Problem 4 - Process Pool for CPU Work

Scenario: A media service needs to compute thumbnails and image hashes for a large catalog.

Build a multiprocessing solution that:

- spreads CPU-bound work across cores
- handles per-item failures cleanly
- avoids sending giant mutable objects to worker processes
- makes it obvious why threads are not the right choice here

## Problem 5 - Hybrid Event Processing System

Scenario: An analytics backend ingests events from the network, performs CPU-heavy scoring, and writes results to a database.

Design a hybrid solution that:

- uses async or threads for network-bound ingestion
- uses processes for CPU-heavy scoring
- coordinates backpressure between stages
- shuts down cleanly without dropping accepted work
