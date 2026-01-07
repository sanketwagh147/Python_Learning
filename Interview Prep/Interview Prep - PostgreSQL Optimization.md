# PostgreSQL Optimization — 100 Scenario-Based Interview Questions

Each scenario includes a Good Answer and a Senior-Level trade-off explanation. Code examples are provided where relevant.

## Purpose & How To Use
- Calibrate depth: Start with diagnosis (EXPLAIN, stats, IO) then move to design (indexes, partitioning) and finally operations (vacuum, WAL, HA).
- Evaluate answers on: correctness, plan stability, SLO awareness (latency/error budgets), and operational trade-offs (write amplification, freshness, cost).
- Drill-down prompts: “What if writes are 10x?”, “What if we need zero-downtime?”, “How would this impact replicas?”
## What Senior Engineers (4-5 YOE) Should Demonstrate
1. **Diagnostic Ownership**: Independently investigate slow queries, correlate with system metrics, and propose targeted fixes without over-engineering.
2. **Architectural Judgment**: Know when to add indexes vs restructure schema vs introduce caching; understand downstream effects on replication and maintenance.
3. **Production Mindset**: Plan migrations with rollback strategies, estimate impact on existing traffic, and communicate risks to stakeholders.
4. **Cross-Team Collaboration**: Work with DBAs, platform teams, and product to balance feature velocity with database health.
5. **Mentorship**: Guide junior engineers through query profiling and schema design decisions.
## Key Concepts Primer
- Cost-based planner: chooses plans based on estimated row counts and cost constants (`random_page_cost`, `effective_cache_size`).
- Statistics: `ANALYZE`, per-column stats target, extended stats for correlations; estimates drive plan quality.
- Index families: B-Tree (general), GIN (inverted, JSONB/array/search), GiST (ranges/geospatial), BRIN (large, ordered tables).
- MVCC & visibility: Vacuum sets visibility map for index-only scans; HOT updates need same-page space and unchanged index keys.
- Memory & spills: `work_mem` is per-node/per-query; spills create temp files and latency spikes.
- Parallel & partitioning: Parallel workers for large scans; partition by time/hash to speed retention and reduce working sets.
- Plan cache: Generic vs custom plans; parameter sensitivity and `plan_cache_mode`.

## Mini Case Study: Hot Dashboard Regression
Symptoms: P95 jumped from 150ms to 900ms after data grew 4x.
Approach: Validate estimates vs actuals, add partial covering index for hot predicate, and precompute via a materialized view.

```sql
EXPLAIN (ANALYZE, BUFFERS)
SELECT u.id, u.name, SUM(o.total)
FROM users u
JOIN orders o ON o.user_id = u.id
WHERE o.status = 'PAID' AND o.created_at >= now() - interval '30 days'
GROUP BY 1,2;

CREATE INDEX CONCURRENTLY idx_orders_paid_30d
  ON orders (user_id, created_at DESC) INCLUDE (total)
  WHERE status = 'PAID';

CREATE MATERIALIZED VIEW mv_revenue_30d AS
SELECT user_id, SUM(total) AS revenue
FROM orders
WHERE status='PAID' AND created_at>= now() - interval '30 days'
GROUP BY 1;
```

## Real-World Debugging Walkthrough

**Scenario**: Production alert fires at 2 AM—P95 read latency jumped from 50ms to 800ms.

**Step 1: Triage** (5 min)
```sql
-- Check for long-running queries
SELECT pid, now() - query_start AS duration, query
FROM pg_stat_activity
WHERE state = 'active' AND now() - query_start > interval '10 seconds'
ORDER BY duration DESC;

-- Check for lock contention
SELECT blocked_locks.pid AS blocked_pid,
       blocking_locks.pid AS blocking_pid,
       blocked_activity.query AS blocked_query
FROM pg_locks blocked_locks
JOIN pg_locks blocking_locks ON blocked_locks.locktype = blocking_locks.locktype
  AND blocked_locks.relation = blocking_locks.relation
  AND blocked_locks.pid != blocking_locks.pid
JOIN pg_stat_activity blocked_activity ON blocked_activity.pid = blocked_locks.pid
WHERE NOT blocked_locks.granted;
```

**Step 2: Identify culprit** (10 min)
```sql
-- Top queries by total time in last hour
SELECT query, calls, total_exec_time, mean_exec_time,
       rows, shared_blks_hit, shared_blks_read
FROM pg_stat_statements
ORDER BY total_exec_time DESC
LIMIT 10;
```

**Step 3: Analyze specific query**
```sql
EXPLAIN (ANALYZE, BUFFERS, FORMAT TEXT)
-- paste the slow query here
```

**Step 4: Quick mitigation vs proper fix**
- Quick: Kill long-running query, add connection limit, or scale read replicas
- Proper: Add missing index, refactor query, or partition table

**Step 5: Post-incident**
- Document root cause and timeline
- Add monitoring for early detection
- Schedule proper fix with migration plan

## Common Pitfalls
- Blindly adding indexes without measuring write cost and memory pressure.
- Relying on `OFFSET` pagination at scale instead of keyset.
- Under-tuning autovacuum on hot tables, causing bloat and plan regressions.
- Using JSONB everywhere without expression indexes or constraints.

## Evaluation Rubric (Interview)

### Junior (1-2 YOE)
- Reads `EXPLAIN` output and identifies sequential vs index scans
- Knows basic index types and when to use them
- Understands transactions and isolation basics

### Mid-Level (3-4 YOE)
- Reads `EXPLAIN (ANALYZE, BUFFERS)` correctly, spots estimate errors and spills
- Chooses proper index type/order, uses partial/covering judiciously
- Understands vacuum/bloat and can tune autovacuum settings

### Senior (4-5 YOE) — Target Level
- **Diagnostic rigor**: Correlates query plans with system metrics (CPU, IO, memory); identifies root cause vs symptoms
- **Design sense**: Makes schema/index decisions considering write amplification, maintenance overhead, and future growth
- **Operability**: Plans zero-downtime migrations; understands WAL, checkpoints, replication lag, and their interdependencies
- **SLO alignment**: Quantifies trade-offs (e.g., "this index adds 15% write overhead but reduces P99 from 200ms to 20ms")
- **Communication**: Explains technical decisions to non-technical stakeholders; documents architectural decisions (ADRs)
- **Mentorship**: Guides team through query optimization; establishes performance review processes

### Staff+ (6+ YOE)
- Designs database architecture for multi-region, high-availability systems
- Establishes organization-wide standards for schema design and query patterns
- Drives cross-team initiatives for database performance and reliability

---

## 1) Slow dashboard query after data growth
- Good Answer: Profile with `EXPLAIN (ANALYZE, BUFFERS)`, add covering indexes (`INCLUDE`), ensure selective filters precede joins, consider partial indexes for common predicates, and cache infrequently changing aggregates via materialized views.
- Senior Trade-offs: Indexes speed reads but slow writes; covering indexes increase size and memory footprint. Materialized views add freshness lag and refresh complexity; choose `CONCURRENTLY` for refresh if uptime matters.

```sql
EXPLAIN (ANALYZE, BUFFERS)
SELECT u.id, u.name, SUM(o.total)
FROM users u
JOIN orders o ON o.user_id = u.id
WHERE o.status = 'PAID' AND o.created_at >= now() - interval '30 days'
GROUP BY 1,2;

-- Example covering index
CREATE INDEX CONCURRENTLY idx_orders_user_paid_recent
  ON orders (user_id, created_at) INCLUDE (status, total)
  WHERE status = 'PAID';
```

## 2) Choosing between GIN and GiST for JSONB search
- Good Answer: For containment queries (`@>`) and existence checks on JSONB keys/values, GIN is typically best. GiST is useful when you need custom operators or range-like semantics; for trigram-ish fuzzy text use `pg_trgm` with GIN.
- Senior Trade-offs: GIN indexes can be large and slower to update; GiST can be smaller but may not support needed operators as efficiently. Consider write amplification and autovacuum impact on hot paths.

## 3) High CPU from hash aggregates
- Good Answer: Increase `work_mem` to enable in-memory hash aggregation; if still spilling, consider pre-aggregation, partial aggregates via materialized views, or partitioning to reduce working set.
- Senior Trade-offs: `work_mem` is per node/per query; too high risks OOM under concurrency. Materialized views trade freshness for predictable CPU usage.

## 4) Frequent sequential scans despite indexes
- Good Answer: Check `ANALYZE` and stats target; bump `ALTER TABLE ... ALTER COLUMN ... SET STATISTICS` for skewed columns; ensure `enable_seqscan` isn’t disabled for testing only; validate predicate selectivity.
- Senior Trade-offs: Higher stats targets increase analyze time and system catalogs size but yield better plans. For very low cardinality, indexes might still be ignored; consider bitmap scans.

## 5) Parameterized queries choose generic plans
- Good Answer: Monitor generic vs custom plans; set `plan_cache_mode = force_custom_plan` or lower `prepared_statement_threshold` for critical queries with skewed parameters.
- Senior Trade-offs: Custom plans improve per-parameter performance but add planning overhead; under high QPS, planning time can dominate. Consider query-level tuning via server-side functions with stable parameters.

## 6) Balancing read/write with indexes on hot table
- Good Answer: Keep only necessary indexes; combine into composite indexes following most selective and join/filter order; exploit partial indexes for common predicates.
- Senior Trade-offs: Every extra index costs on INSERT/UPDATE/DELETE. Composite index order matters for range vs equality. Partial indexes increase complexity but reduce bloat and write cost.

## 7) Minimizing bloat after frequent updates
- Good Answer: Ensure autovacuum settings per table (scale factor, threshold) reflect write volume; schedule `VACUUM (FULL)` only when absolutely necessary; prefer `REINDEX CONCURRENTLY` on bloated indexes.
- Senior Trade-offs: Aggressive vacuum reduces bloat but increases IO and CPU. `VACUUM FULL` reclaims space but locks; use sparingly in maintenance windows.

## 8) HOT updates not kicking in
- Good Answer: Reduce indexed columns updated, adjust `fillfactor` to leave room on page; HOT updates require no index key changes and free space on the same page.
- Senior Trade-offs: Lower `fillfactor` increases table size and cache footprint but reduces page splits and improves HOT likelihood.

## 9) Time-series table with slow retention deletes
- Good Answer: Range partition by time; drop old partitions instead of row deletes. For large backfills, use `COPY` and `UNLOGGED` staging + `INSERT ... SELECT` into partitions.
- Senior Trade-offs: Partitioning adds planning overhead and schema complexity; dropping partitions is near-instant but requires disciplined partition lifecycle management.

## 10) COPY vs bulk INSERT for ingestion
- Good Answer: Prefer `COPY` for bulk; disable constraints and triggers only if you can validate separately. Use `maintenance_work_mem` higher for index builds, and `synchronous_commit = off` for non-critical batches.
- Senior Trade-offs: Turning off WAL/constraints risks data integrity and recovery gaps; isolate in staging tables.

## 11) Choosing BRIN vs B-Tree for large append-only table
- Good Answer: For naturally ordered columns (timestamp, ID), BRIN is space-efficient and fast to scan; for point lookups or highly selective predicates, B-Tree is better.
- Senior Trade-offs: BRIN requires table order correlation and `VACUUM/ANALYZE` to maintain summaries; queries may still scan ranges.

## 12) Slow LIKE '%term%' searches
- Good Answer: Use `pg_trgm` with GIN or GiST to accelerate substring searches; refactor to prefix searches where possible; consider full-text search for language-aware needs.
- Senior Trade-offs: Trigram indexes can be large; weigh storage and update overhead against query latency SLAs.

## 13) Choosing isolation level for mixed workloads
- Good Answer: Use `READ COMMITTED` by default; escalate to `REPEATABLE READ` or `SERIALIZABLE` only where anomalies matter. Apply explicit locking or optimistic retries for critical sections.
- Senior Trade-offs: Higher isolation reduces anomalies but increases contention and abort rates; measure business cost of anomalies vs throughput.

## 14) Deadlocks after adding new feature
- Good Answer: Standardize lock acquisition order, break big transactions into smaller units, add timeouts, and monitor `pg_locks` to map cycles.
- Senior Trade-offs: Smaller transactions reduce deadlock windows but increase overhead and partial failure handling.

## 15) Choosing partial vs full index
- Good Answer: Use partial index when a predicate covers most hot queries (e.g., `status='ACTIVE'`). Keep predicate immutable and aligned to common filters.
- Senior Trade-offs: Partial indexes complicate planner selectivity and maintenance; if predicate covers too many rows, benefit diminishes.

## 16) Connection spikes overwhelm Postgres
- Good Answer: Use PgBouncer in transaction pooling mode; cap max connections on Postgres; use async/await in app to avoid thread-per-connection.
- Senior Trade-offs: Transaction pooling breaks session-level features (temp tables, prepared statements). Weigh simplicity vs throughput.

## 17) Parallel query not used
- Good Answer: Enable `max_parallel_workers_per_gather`, ensure operations are parallel-safe, and increase table size thresholds; avoid functions marked `parallel unsafe`.
- Senior Trade-offs: Parallelism adds overhead and can hurt for small datasets; tune per query class.

## 18) Frequent temp file spills
- Good Answer: Increase `work_mem` judiciously; add targeted hints by setting at role or query level; consider indexes to avoid big sorts/hashes.
- Senior Trade-offs: Over-allocating `work_mem` under concurrency risks memory pressure; profile typical concurrency levels.

## 19) Choosing between CTEs and subqueries
- Good Answer: In modern PostgreSQL, CTEs may inline; avoid relying on materialization for performance unless needed; prefer subqueries if you want planner flexibility.
- Senior Trade-offs: Forced materialization can stabilize runtime but increases IO; readability vs performance trade-off.

## 20) Tuning `shared_buffers` and `effective_cache_size`
- Good Answer: Set `shared_buffers` ~25% of RAM (rule of thumb), `effective_cache_size` to approximate OS cache + shared buffers to guide planner cost model.
- Senior Trade-offs: Too large `shared_buffers` can degrade OS cache behavior; validate with workload.

## 21) Choosing `synchronous_commit`
- Good Answer: For latency-sensitive but loss-tolerant events, set `synchronous_commit=off` (or at transaction level). For critical transactions, keep it on, optionally with quorum synchronous replication.
- Senior Trade-offs: Turning off sync commit risks a small window of data loss on crash.

## 22) Auto-explain for production query capture
- Good Answer: Enable `auto_explain` with sampling and `ANALYZE, BUFFERS` for slow queries only; avoid verbose logs under load; complement with `pg_stat_statements`.
- Senior Trade-offs: Logging with analyze can add overhead; sample conservatively.

## 23) JSONB vs normalized schema
- Good Answer: Use JSONB for flexible, sparse attributes; normalize frequently queried fields and join keys; create functional indexes for JSON paths.
- Senior Trade-offs: JSONB simplifies schema evolution but complicates constraints, referential integrity, and indexing cost.

## 24) Upsert contention with ON CONFLICT
- Good Answer: Batch operations, ensure conflict target matches index, reduce lock scopes, and consider partitioning hot keys.
- Senior Trade-offs: ON CONFLICT is convenient but can serialize on hot rows; batching trades latency for throughput.

## 25) Heavy write workload causing checkpoint storms
- Good Answer: Increase `max_wal_size`, tune `checkpoint_timeout` and `checkpoint_completion_target` to smooth IO. Monitor `bgwriter` stats.
- Senior Trade-offs: Larger WAL increases recovery time and disk usage; find balance.

## 26) Choosing materialized views vs caching layer
- Good Answer: Materialized views with `CONCURRENTLY` refresh offer SQL-native caching; external caches (Redis) can reduce DB load but add consistency complexity.
- Senior Trade-offs: DB-contained cache eases data locality; external caches scale independently but need invalidation strategies.

## 27) Index-only scans not occurring
- Good Answer: Ensure index covers all referenced columns (via `INCLUDE`) and visibility map is set; vacuum to set VM bits.
- Senior Trade-offs: INCLUDE increases index size; frequent updates degrade IOS benefits.

## 28) Range queries on composite index
- Good Answer: Equality columns should precede range columns in index order; consider `DESC` ordering for latest-first scans.
- Senior Trade-offs: Composite order biases planner; different query shapes may need multiple indexes.

## 29) Avoiding OR predicates
- Good Answer: Replace `OR` with `UNION ALL` where each branch uses its own index; ensure dedup if needed.
- Senior Trade-offs: More complex queries but often better plans; measure result correctness under duplicates.

## 30) Long-running transactions blocking vacuum
- Good Answer: Keep transactions short, use timeouts, monitor `xmin` and `age(datfrozenxid)`, investigate idle-in-transaction sessions.
- Senior Trade-offs: Strict timeouts can cause user-facing errors; balance reliability vs maintenance.

## 31) Aggregations over large tables
- Good Answer: Precompute rollups by partition/day; use incremental refresh patterns; leverage `GROUPING SETS` where helpful.
- Senior Trade-offs: Denormalization reduces compute but adds complexity and storage.

## 32) Foreign keys and bulk loads
- Good Answer: Load parent first, then child; disable and re-enable constraints cautiously only in isolated staging phases.
- Senior Trade-offs: Disabling constraints risks invalid data; ensure rigorous validation.

## 33) Choosing identity vs UUID keys
- Good Answer: Use int identity for write-heavy clustered tables to minimize page splits; for distributed systems requiring uniqueness, UUID v4 or v7; consider `uuid-ossp` or `gen_random_uuid`.
- Senior Trade-offs: UUIDs are larger and randomize inserts; v7 improves locality but still larger than int.

## 34) Statistics for skewed distributions
- Good Answer: Increase stats target for skewed columns; create extended stats on column groups (`CREATE STATISTICS`) for correlated predicates.
- Senior Trade-offs: Larger stats increase analyze time and memory; benefit is plan stability.

## 35) Tuning `work_mem` per role or query
- Good Answer: Set conservative global; bump for reporting role; use `SET LOCAL work_mem='256MB'` within controlled functions.
- Senior Trade-offs: Over-allocating can crash the server under concurrency.

## 36) Hot standby read consistency
- Good Answer: Understand replica lag; use `hot_standby_feedback` cautiously to reduce conflicts; for read-your-writes, use same primary or logical replication.
- Senior Trade-offs: Feedback prevents vacuum cleanup and can cause bloat on primary.

## 37) WAL size explosion during bulk ops
- Good Answer: Use `UNLOGGED` tables for transient data, switch to logged before making durable; batch in chunks; consider `COPY FREEZE` for fresh tables.
- Senior Trade-offs: Unlogged tables lose data on crash; not suitable for durable data.

## 38) Effective use of `EXPLAIN` costs
- Good Answer: Compare estimated vs actual rows; big discrepancies imply stats issues; use `BUFFERS` and `TIMING` to see IO and CPU hotspots.
- Senior Trade-offs: Over-fitting to one plan can regress others; tune at workload level.

## 39) Join order surprises
- Good Answer: Check `join_collapse_limit` and `from_collapse_limit`; ensure proper indexes on join keys; avoid cross joins.
- Senior Trade-offs: For complex queries, planner heuristics may not be optimal; sometimes decomposing into steps helps.

## 40) Vacuum tuning per table
- Good Answer: Override `autovacuum_vacuum_scale_factor`, `analyze_scale_factor`, and thresholds on hot tables; monitor `pg_stat_user_tables`.
- Senior Trade-offs: Aggressive settings increase maintenance cost.

## 41) Partition pruning not happening
- Good Answer: Ensure partition key is directly constrained in the query; avoid expressions that block pruning; keep partition bounds aligned.
- Senior Trade-offs: Query rewrites may sacrifice readability.

## 42) Indexing expressions
- Good Answer: Use functional indexes for computed predicates (e.g., `lower(email)`); ensure function is immutable or stable.
- Senior Trade-offs: Function volatility can prevent index usage; adds complexity.

## 43) Large IN lists
- Good Answer: Use temp tables + join or `VALUES` lists; beware plan bloat; consider bitmap scans.
- Senior Trade-offs: Temp tables add lifecycle overhead but give better stats.

## 44) DISTINCT ON vs window functions
- Good Answer: For “latest per group”, use indexed `DISTINCT ON (key) ORDER BY key, created_at DESC`; alternatively `ROW_NUMBER() OVER (PARTITION BY ...)`.
- Senior Trade-offs: Window functions can be clearer but may sort more data.

## 45) UPDATE vs INSERT for slowly changing data
- Good Answer: Use `INSERT ... ON CONFLICT DO UPDATE` for upserts; separate history table if auditing required; minimize updated indexed columns.
- Senior Trade-offs: Upserts can serialize on hot keys; history tables grow and need archiving.

## 46) Choosing `INCLUDE` columns
- Good Answer: Include non-selective, frequently selected columns to enable index-only scans without affecting index order.
- Senior Trade-offs: Larger indexes increase cache pressure.

## 47) Read-mostly table tuning
- Good Answer: Higher `fillfactor` (default 100) is fine; focus on read-optimized indexes and IOS; schedule vacuum for visibility map upkeep.
- Senior Trade-offs: Over-indexing slows occasional writes.

## 48) Write-mostly table tuning
- Good Answer: Minimize indexes, reduce `fillfactor` to avoid page splits, batch writes, and use unlogged staging if safe.
- Senior Trade-offs: Read queries may suffer; add targeted read indexes only as needed.

## 49) Locking plan for migrations
- Good Answer: Use `CREATE INDEX CONCURRENTLY`, `ALTER TABLE ... ADD COLUMN` is fast; avoid `ALTER TYPE` in-place on huge tables; use shadow tables for heavy rewrites.
- Senior Trade-offs: Concurrent ops are slower and complex to rollback.

## 50) Statistics on JSONB keys
- Good Answer: Create expression indexes and increase stats for popular paths using `ALTER TABLE ... SET STATISTICS` via `pg_statistic_ext` where available.
- Senior Trade-offs: Expression stats add overhead; ensure paths are stable.

## 51) Avoiding N+1 with joins
- Good Answer: Consolidate into fewer queries, use `JOIN` with proper indexes, or server-side batching.
- Senior Trade-offs: Larger joins may need more memory; watch `work_mem`.

## 52) Retry strategy for serialization failures
- Good Answer: Implement retry with backoff for `SERIALIZABLE`/`REPEATABLE READ` aborts; limit retry count.
- Senior Trade-offs: Retries increase tail latency; apply only where isolation is required.

## 53) Aggregation on distinct counts
- Good Answer: Use `approx_count_distinct` via extensions like `hyperloglog` or `count(distinct)` with pre-aggregation tables.
- Senior Trade-offs: Approximation trades accuracy for speed and memory.

## 54) Data compression strategies
- Good Answer: Leverage TOAST for large values; for columnar needs consider Citus/Timescale/FDW to columnar engines; use `wal_compression` for heavy WAL traffic.
- Senior Trade-offs: Compression reduces IO but increases CPU; end-to-end latency impact varies.

## 55) Query plan instability after analyze
- Good Answer: Pin plans via SQL rewrite or stable parameters; ensure representative stats; consider `ALTER TABLE ... SET (autovacuum_analyze_scale_factor=...)` to control frequency.
- Senior Trade-offs: Forcing plans can protect critical paths but hide regressions.

## 56) Fast pagination at scale
- Good Answer: Use keyset pagination with `WHERE (created_at, id) < (...) ORDER BY created_at DESC, id DESC LIMIT 50` over `OFFSET`.
- Senior Trade-offs: Keyset requires deterministic sort keys and more complex client logic.

## 57) Minimizing replication lag
- Good Answer: Optimize write transactions, tune `wal_compression`, network, and `max_wal_size`; on replica, avoid slow queries that block replay.
- Senior Trade-offs: Compressing WAL uses CPU; too-small `max_wal_size` increases checkpoints.

## 58) Heavy contention on sequence
- Good Answer: Increase `CACHE` on sequence; consider hi/lo or per-shard sequences; for UUID, avoid central contention.
- Senior Trade-offs: Larger cache risks gaps on crash; usually acceptable.

## 59) Handling large deletes
- Good Answer: Delete in small batches with indexes, or detach/drop partitions; avoid long transactions; vacuum afterward.
- Senior Trade-offs: Batching extends maintenance window but keeps DB healthy.

## 60) Choosing UNLOGGED tables
- Good Answer: Use for ephemeral data where crash loss is acceptable (caches, scratch); not replicated.
- Senior Trade-offs: Faster writes but no durability; replication gaps.

## 61) Managing bloat in indexes
- Good Answer: `REINDEX CONCURRENTLY`; consider `fillfactor` and fewer updates on key columns.
- Senior Trade-offs: Concurrent rebuilds take longer and use extra disk.

## 62) Operator class selection
- Good Answer: Choose appropriate opclass (e.g., `text_pattern_ops` for prefix LIKE) to enable index usage.
- Senior Trade-offs: Specialized opclasses limit versatility; maintain separate indexes if needed.

## 63) Join algorithm selection insights
- Good Answer: Understand nested loop (good for selective joins with index), hash join (large datasets, enough memory), merge join (sorted inputs).
- Senior Trade-offs: Forcing a method via GUCs is for diagnostics; prefer stats-driven plans.

## 64) Optimizing EXISTS vs IN
- Good Answer: Use `EXISTS` for semi-join semantics; planner often rewrites; pick the more expressive one and check plan.
- Senior Trade-offs: Clarity usually wins; performance similar with good stats.

## 65) Large reports with window functions
- Good Answer: Add indexes supporting partition/order keys; pre-filter aggressively; bump `work_mem` for sorts.
- Senior Trade-offs: Memory vs concurrency balance required.

## 66) Preventing table scans on nullable columns
- Good Answer: Consider partial indexes `WHERE col IS NOT NULL`; rework predicates to be sargable.
- Senior Trade-offs: Partial indexes increase complexity.

## 67) Optimizing UPSERT storms
- Good Answer: Queue and coalesce updates per key; use `ON CONFLICT` with minimal updates; consider `INSERT ... ON CONFLICT DO NOTHING` then follow-up updates.
- Senior Trade-offs: Complexity increases but reduces lock contention.

## 68) Read replicas for analytics
- Good Answer: Offload heavy reads to replicas; ensure acceptable replica lag; use logical replication for selective subsets.
- Senior Trade-offs: Replicas cost; lag can cause stale reads and anomalies.

## 69) Statistics for partitions
- Good Answer: Gather stats per partition; use `default_statistics_target` appropriately; global stats help cross-partition estimates in newer PG.
- Senior Trade-offs: More partitions = more analyze overhead.

## 70) Minimizing impact of large transactions
- Good Answer: Chunk data migrations; commit frequently; monitor `pg_xact` wraparound risk.
- Senior Trade-offs: More commits increase overhead but keep vacuum healthy.

## 71) Handling skewed keys in joins
- Good Answer: Skew-aware batching; split hot keys to separate processing; use `DISTINCT` on driver side to reduce duplicates.
- Senior Trade-offs: Additional logic vs significant speedups under skew.

## 72) Avoiding function volatility pitfalls
- Good Answer: Use immutable/stable functions in indexes; avoid `now()` in indexed expressions (use generated columns or triggers).
- Senior Trade-offs: Triggers add write cost; generated columns are simpler in newer PG.

## 73) Tuning `random_page_cost` and `seq_page_cost`
- Good Answer: Reflect storage type (SSD vs HDD); lowering `random_page_cost` encourages index scans.
- Senior Trade-offs: Wrong values cause bad plans; change cautiously.

## 74) Memory accounting under load
- Good Answer: Sum `work_mem` across concurrent queries and nodes; cap connections, use pooling.
- Senior Trade-offs: Underestimating leads to OOM; over-restricting reduces concurrency.

## 75) Optimizing DISTINCT heavy queries
- Good Answer: Use `DISTINCT ON` with suitable index; deduplicate earlier with groupings or temp tables.
- Senior Trade-offs: Indexes needed for speed; otherwise sorts spill.

## 76) Avoiding write amplification with many small updates
- Good Answer: Batch updates, use `COPY` to temp and `UPDATE ... FROM` joins; consider `UPSERT` with minimal changed columns.
- Senior Trade-offs: Batching trades latency for throughput.

## 77) Choosing partition key for time-series
- Good Answer: Partition by time for retention; sub-partition by tenant or hash for load distribution.
- Senior Trade-offs: Too many partitions harm planning; balance count and size.

## 78) Fast count(*)
- Good Answer: Use approximate counts or maintain counters per partition; exact counts on large tables are expensive.
- Senior Trade-offs: Freshness and accuracy vs speed.

## 79) Tuning autovacuum on append-only tables
- Good Answer: Lower analyze frequency; vacuum less often; focus on visibility map.
- Senior Trade-offs: Over-tuning risks stale stats; keep some analyze cadence.

## 80) Cross-region replication
- Good Answer: Use async replication for latency; for strict durability consider quorum sync to local plus async remote.
- Senior Trade-offs: Sync across WAN hurts latency and throughput.

## 81) Detecting slow IO vs bad plans
- Good Answer: Compare `BUFFERS` and timing; high shared/hit with slow time suggests CPU; high read IO suggests storage; use `pg_stat_io` and system metrics.
- Senior Trade-offs: Hardware upgrades vs schema/query fixes.

## 82) Avoiding duplicate work with CTE reuse
- Good Answer: Materialize a subresult if reused multiple times; otherwise let inlining happen.
- Senior Trade-offs: Materialization trades CPU for IO predictability.

## 83) Optimizing large IN subqueries
- Good Answer: Rewrite as `JOIN` with distinct keys; ensure index on subquery output.
- Senior Trade-offs: Subquery may be fine if planner rewrites; verify.

## 84) Constraint checks and performance
- Good Answer: Use `DEFERRABLE INITIALLY DEFERRED` to batch checks; but only when correctness allows.
- Senior Trade-offs: Deferred errors appear late; debugging harder.

## 85) Hot path read latency spikes
- Good Answer: Pin hot data via memory sizing; reduce random IO with covering indexes; warmup after deploys.
- Senior Trade-offs: Memory is finite; larger indexes compete with tables.

## 86) Avoiding table rewrites for column changes
- Good Answer: Add new column nullable; backfill in chunks; then set `NOT NULL` with `VALIDATE CONSTRAINT` style checks.
- Senior Trade-offs: Longer migration window but minimal lock time.

## 87) De-duplication strategies
- Good Answer: Use unique indexes; for soft dedupe, use `DISTINCT ON` with retaining policy and background cleanup.
- Senior Trade-offs: Strict uniqueness simplifies logic but may block writes.

## 88) Handling out-of-date statistics during load spikes
- Good Answer: Run manual `ANALYZE` after large loads; increase autovacuum analyze aggressiveness on target tables.
- Senior Trade-offs: Analyze consumes CPU/IO.

## 89) Choosing `temp_buffers` and temp tables
- Good Answer: Use temp tables for complex pipelines to persist intermediate results; size `temp_buffers` accordingly.
- Senior Trade-offs: Temp tables break in transaction pooling; consider app-level cache.

## 90) Ensuring plan stability with bind parameters
- Good Answer: For highly skewed predicates, avoid prepared statements or force custom plans; wrap in stable functions if needed.
- Senior Trade-offs: Planning time vs execution time trade-off at scale.

## 91) Optimizing JOIN on JSONB keys
- Good Answer: Extract keys into generated columns and index them; avoid runtime JSON extraction in join conditions.
- Senior Trade-offs: Denormalization increases write cost but pays off for joins.

## 92) Large UPDATE with minimal locking
- Good Answer: Update in small batches with `ORDER BY` primary key; `NOWAIT/SKIP LOCKED` where applicable.
- Senior Trade-offs: Longer maintenance window but better concurrency.

## 93) Index maintenance windows
- Good Answer: Build indexes `CONCURRENTLY`; throttle via `maintenance_work_mem` and vacuum cost settings.
- Senior Trade-offs: Longer build times vs availability.

## 94) Enforcing data quality at scale
- Good Answer: Use constraints and check constraints with partial applicability; validate via `VALIDATE CONSTRAINT`.
- Senior Trade-offs: Constraints can block writes on violation; careful rollout.

## 95) Choosing `effective_io_concurrency`
- Good Answer: On systems with RAID/NVMe, increase `effective_io_concurrency` to leverage async IO for bitmap heap scans.
- Senior Trade-offs: Too high may not help; test per hardware.

## 96) Planning for failover
- Good Answer: Use Patroni or cloud equivalents; test failovers; ensure clients handle `read_only` and retry.
- Senior Trade-offs: Strong HA increases operational complexity.

## 97) Detecting and fixing bloated TOAST tables
- Good Answer: Monitor `pg_toast` relations; toast-bloat can be addressed with `VACUUM FULL` on base table in maintenance or rewrite.
- Senior Trade-offs: Locking and rewrite cost; consider compression strategies.

## 98) Optimizing foreign table (FDW) queries
- Good Answer: Push down filters and aggregates; create local stats on foreign tables where supported; materialize frequently used subsets.
- Senior Trade-offs: Network latency dominates; consider ETL.

## 99) Handling collation and sort performance
- Good Answer: Use ICU collations judiciously; for performance-critical case-insensitive, consider `citext` or normalized columns with `lower()` and index.
- Senior Trade-offs: Collations affect index order; changing collation requires rebuilds.

## 100) Observability stack for performance
- Good Answer: Enable `pg_stat_statements`, sampling with `auto_explain`, track `pg_stat_io`, build dashboards for top queries, plans, IO, and bloat trends.
- Senior Trade-offs: Observability costs overhead but prevents blind tuning; sample and aggregate to control cost.

---

## Quick Reference Commands

```sql
-- Enable pg_stat_statements (in postgresql.conf or ALTER SYSTEM)
shared_preload_libraries = 'pg_stat_statements'
pg_stat_statements.max = 10000
pg_stat_statements.save = on

-- Find top queries by total time
SELECT query, calls, total_exec_time, mean_exec_time
FROM pg_stat_statements
ORDER BY total_exec_time DESC
LIMIT 20;

-- Example: increasing stats target for a skewed column
ALTER TABLE orders ALTER COLUMN status SET STATISTICS 500;
ANALYZE orders;
```
