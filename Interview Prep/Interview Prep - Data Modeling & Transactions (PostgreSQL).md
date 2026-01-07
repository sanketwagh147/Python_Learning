# Data Modeling & Transactions (PostgreSQL) — 100 Scenario-Based Interview Questions

Each scenario includes a Good Answer and a Senior-Level trade-off explanation. SQL examples are included where relevant.

## Purpose & How To Use
- Structured flow: Model entities and relationships → enforce invariants with constraints → plan migrations → define transaction semantics.
- Evaluate responses on: integrity guarantees, migration safety, performance implications, and cross-service boundaries (sagas/outbox).
- Drill prompts: “How to avoid double-spend?”, “How to do zero-downtime enum change?”, “How to enforce ‘exactly one active per group’?”
## What Senior Engineers (4-5 YOE) Should Demonstrate
1. **Schema Design Excellence**: Model complex domains correctly; balance normalization vs performance; plan for evolution.
2. **Constraint Mastery**: Use the right constraint types (FK, CHECK, UNIQUE, EXCLUSION); understand when DB vs app enforcement.
3. **Migration Safety**: Execute zero-downtime schema changes; handle backfills at scale; plan rollback strategies.
4. **Transaction Design**: Choose appropriate isolation levels; implement optimistic/pessimistic locking correctly; design sagas.
5. **Cross-Service Thinking**: Design data contracts; implement outbox pattern; handle eventual consistency.

## Schema Design Decision Tree
```
New Feature Requires Data → Ask These Questions:

1. WHO owns this data?
   ├─ Single service → Local table with proper constraints
   └─ Multiple services → Define contracts, consider replication

2. HOW will it be queried?
   ├─ Point lookups → B-tree index on lookup key
   ├─ Range scans → Consider partitioning, BRIN
   ├─ Full-text search → tsvector or external search
   └─ Aggregations → Pre-compute, materialized views

3. HOW will it change over time?
   ├─ Append-only → Partition by time, easy retention
   ├─ Frequent updates → Optimize for HOT, consider narrow tables
   └─ Schema evolution → Plan migration path, JSONB for flexibility

4. WHAT invariants must hold?
   ├─ Simple → CHECK constraints
   ├─ Referential → Foreign keys
   ├─ Uniqueness → UNIQUE (partial if needed)
   └─ Complex → Triggers or app logic with proper locking
```
## Key Concepts Primer
- Normalization vs denormalization: Keep writes correct/lean; denormalize for read-heavy views with rebuilds/materializations.
- Keys & constraints: Surrogate vs natural keys, composite uniques, partial uniques, exclusion constraints for time/space.
- Isolation & locking: `READ COMMITTED` vs `REPEATABLE READ` vs `SERIALIZABLE`; optimistic vs pessimistic locking.
- Temporal patterns: Type 2 SCD, version tables, generated columns for deterministic derivations.
- Outbox & sagas: Atomic event publishing and compensation across service boundaries for at-least-once guarantees.

## Mini Case Study: Payments Double-Spend Guard
Goal: Prevent duplicate charge on retries and preserve audit.
Design: Ledger with idempotency key unique index, outbox to publish payment events, and optimistic updates on balances.

```sql
CREATE TABLE payments (
  id bigserial PRIMARY KEY,
  idempotency_key text NOT NULL,
  account_id bigint NOT NULL REFERENCES accounts(id),
  amount numeric(19,4) NOT NULL CHECK (amount > 0),
  status text NOT NULL CHECK (status in ('PENDING','SETTLED','FAILED')),
  created_at timestamptz DEFAULT now()
);
CREATE UNIQUE INDEX payments_idem_uniq ON payments (idempotency_key);

-- Outbox pattern
CREATE TABLE outbox (
  id bigserial PRIMARY KEY,
  aggregate_id bigint NOT NULL,
  type text NOT NULL,
  payload jsonb NOT NULL,
  created_at timestamptz DEFAULT now(),
  published_at timestamptz
);
```

## Zero-Downtime Migration Playbook

### Adding a NOT NULL Column
```sql
-- Step 1: Add column as nullable (fast, no lock)
ALTER TABLE users ADD COLUMN phone_verified boolean;

-- Step 2: Backfill in batches (app continues working)
UPDATE users SET phone_verified = false
WHERE id BETWEEN 1 AND 10000 AND phone_verified IS NULL;
-- Repeat for all batches...

-- Step 3: Add constraint without validation (fast)
ALTER TABLE users ADD CONSTRAINT users_phone_verified_not_null
  CHECK (phone_verified IS NOT NULL) NOT VALID;

-- Step 4: Validate constraint (slow but doesn't block writes)
ALTER TABLE users VALIDATE CONSTRAINT users_phone_verified_not_null;

-- Step 5: Convert to proper NOT NULL (fast after validation)
ALTER TABLE users ALTER COLUMN phone_verified SET NOT NULL;
ALTER TABLE users DROP CONSTRAINT users_phone_verified_not_null;
```

### Renaming a Column
```sql
-- Step 1: Add new column
ALTER TABLE users ADD COLUMN full_name text;

-- Step 2: Deploy app that writes to BOTH columns, reads from old
-- (code change: write to both 'name' and 'full_name')

-- Step 3: Backfill
UPDATE users SET full_name = name WHERE full_name IS NULL;

-- Step 4: Deploy app that writes to BOTH, reads from NEW

-- Step 5: Drop old column (after monitoring period)
ALTER TABLE users DROP COLUMN name;
```

### Changing Column Type
```sql
-- For incompatible types, use the dual-column approach:
-- 1. Add new column with new type
-- 2. Dual-write from app
-- 3. Backfill and convert
-- 4. Switch reads to new column
-- 5. Drop old column

-- For compatible types (e.g., varchar(50) -> varchar(100)):
ALTER TABLE users ALTER COLUMN email TYPE varchar(100);
-- This is fast and safe for increasing limits
```

### Adding an Index Safely
```sql
-- Always use CONCURRENTLY in production
CREATE INDEX CONCURRENTLY idx_users_email ON users (lower(email));

-- Check for invalid indexes after creation
SELECT indexrelid::regclass, indisvalid
FROM pg_index
WHERE NOT indisvalid;

-- If invalid, drop and retry
DROP INDEX CONCURRENTLY idx_users_email;
```

## Common Modeling Patterns

### Audit Trail
```sql
CREATE TABLE audit_log (
  id bigserial PRIMARY KEY,
  table_name text NOT NULL,
  record_id bigint NOT NULL,
  action text NOT NULL CHECK (action IN ('INSERT', 'UPDATE', 'DELETE')),
  old_data jsonb,
  new_data jsonb,
  changed_by text NOT NULL,
  changed_at timestamptz DEFAULT now()
);

CREATE INDEX idx_audit_log_table_record ON audit_log (table_name, record_id);
CREATE INDEX idx_audit_log_changed_at ON audit_log (changed_at);
```

### Multi-Tenant with RLS
```sql
CREATE TABLE tenant_data (
  id bigserial PRIMARY KEY,
  tenant_id bigint NOT NULL REFERENCES tenants(id),
  data jsonb NOT NULL
);

ALTER TABLE tenant_data ENABLE ROW LEVEL SECURITY;

CREATE POLICY tenant_isolation ON tenant_data
  USING (tenant_id = current_setting('app.current_tenant')::bigint);

-- App sets tenant context per request:
-- SET LOCAL app.current_tenant = '123';
```

### Exactly-One Active Record
```sql
-- Only one active subscription per user
CREATE UNIQUE INDEX idx_subscriptions_one_active
  ON subscriptions (user_id)
  WHERE status = 'ACTIVE';
```

## Common Pitfalls
- Relying on application-only checks for invariants that belong in constraints.
- ENUM proliferation and painful migrations instead of lookup tables with FKs.
- Cross-partition/global uniqueness without including the partition key.
- Large deletes via single transaction instead of partition drops or batched deletes.

## Evaluation Rubric (Interview)

### Junior (1-2 YOE)
- Creates basic tables with appropriate types
- Understands primary keys and foreign keys
- Knows basic SQL operations

### Mid-Level (3-4 YOE)
- Designs normalized schemas; uses constraints appropriately
- Understands transactions and isolation basics
- Can plan simple migrations

### Senior (4-5 YOE) — Target Level
- **Integrity-first**: Uses the right constraints (FKs, checks, uniques, exclusions) to encode business rules; knows when to use triggers vs app logic
- **Migration safety**: Plans zero-downtime changes with `CONCURRENTLY`, `NOT VALID` + `VALIDATE`, staged backfills; has rollback strategies
- **Transaction design**: Picks isolation and locking appropriately; implements optimistic concurrency correctly; avoids common pitfalls
- **Cross-service thinking**: Applies outbox/saga patterns; designs idempotency; understands data contracts and eventual consistency
- **Performance awareness**: Considers query patterns when modeling; plans for data growth; balances normalization vs performance

### Staff+ (6+ YOE)
- Designs schemas for multi-region, multi-tenant systems
- Establishes organization-wide data modeling standards
- Architects data platforms and migration frameworks

---

## 1) Choosing surrogate vs natural primary keys
- Good Answer: Prefer surrogate keys (BIGSERIAL/IDENTITY/UUID) for stability; keep natural keys as unique constraints for validation.
- Senior Trade-offs: Surrogates simplify joins and changes but add an extra column; natural keys reduce columns but can change over time and break referential integrity.

## 2) Many-to-many modeling options
- Good Answer: Use a junction table with two FKs and a composite unique constraint to prevent duplicates.
- Senior Trade-offs: Simpler than array/JSON; adds a join hop but maintains integrity and query flexibility.

```sql
CREATE TABLE author_book (
  author_id bigint REFERENCES authors(id),
  book_id   bigint REFERENCES books(id),
  PRIMARY KEY (author_id, book_id)
);
```

## 3) Polymorphic associations
- Good Answer: Use separate tables per type with a common interface, or a single table with type + nullable FK columns, or a join table with `(target_type, target_id)` plus constraints.
- Senior Trade-offs: Simpler polymorphic schemas reduce constraints; clean referential integrity is harder; prefer explicit tables when possible.

## 4) Modeling hierarchical data
- Good Answer: Adjacency list (`parent_id`) for simplicity; for heavy reads like subtree queries, consider materialized path or nested sets.
- Senior Trade-offs: Adjacency list is easy to mutate but expensive for deep traversals; nested sets optimize reads but complicate writes.

## 5) Soft delete vs hard delete
- Good Answer: Use `deleted_at` column with partial unique indexes to preserve history while preventing duplicates among active rows.
- Senior Trade-offs: Soft deletes complicate queries and indexes; hard deletes lose history; consider an audit table.

```sql
-- Prevent duplicate active usernames
CREATE UNIQUE INDEX users_username_active_uniq
ON users (username)
WHERE deleted_at IS NULL;
```

## 6) Enforcing case-insensitive uniqueness
- Good Answer: Use functional unique index on `lower(column)` or use `citext`.
- Senior Trade-offs: Functional index is explicit and portable; `citext` simplifies usage but changes type semantics.

## 7) JSONB vs normalized columns
- Good Answer: Use JSONB for sparse/less queried attributes; normalize frequently filtered/joined fields; add expression indexes for hot JSON paths.
- Senior Trade-offs: JSONB eases evolution but complicates constraints; normalized schemas improve integrity and indexing.

## 8) Multi-tenant design: single vs schema-per-tenant
- Good Answer: Single schema with `tenant_id` FK and RLS for simplicity; schema-per-tenant for strong isolation at cost of management overhead.
- Senior Trade-offs: Single schema scales operationally; schema-per-tenant isolates noisy neighbors but complicates migrations.

## 9) Enforcing cross-table invariants
- Good Answer: Use FK + check constraints; for complex invariants, use triggers or application-level checks with transactions.
- Senior Trade-offs: Triggers give strong guarantees but add hidden logic; app checks risk races without proper locking.

## 10) Unique across partitions
- Good Answer: Use a global unique index by including partition key or enforce uniqueness via central table or application-level registry.
- Senior Trade-offs: Global uniqueness breaks partition independence; consider composite keys.

## 11) Choosing partitioning strategy
- Good Answer: Range by time for time-series/retention; hash by key for load distribution; list for categorical sharding.
- Senior Trade-offs: More partitions increase planning overhead; align partition size with maintenance needs.

## 12) Constraints with partitioning
- Good Answer: Use partition-level constraints and indexes; global unique constraints require including partition key or logical enforcement.
- Senior Trade-offs: Cross-partition constraints are limited; design keys accordingly.

## 13) Modeling versioned entities
- Good Answer: Separate `entity` table and `entity_version` table with `valid_from/valid_to`; use views for current state.
- Senior Trade-offs: Doubles storage and query complexity; enables full history and temporal queries.

## 14) Slowly Changing Dimension (SCD)
- Good Answer: Use SCD Type 2 with `effective_from/to` and `is_current` or Type 1 for overwrite when history not needed.
- Senior Trade-offs: Type 2 supports audit/history at storage and complexity cost.

## 15) Denormalization for read performance
- Good Answer: Denormalize computed fields or aggregates into target tables; maintain via triggers or ETL.
- Senior Trade-offs: Faster reads but risk staleness; ensure deterministic rebuilds and validation.

## 16) Enforcing business rules with CHECK constraints
- Good Answer: Use `CHECK` for simple invariants (e.g., `amount >= 0`, date ranges); prefer DB checks over app-only.
- Senior Trade-offs: DB checks provide strong guarantees but can block writes on invalid data; coordinate changes carefully.

## 17) Transaction isolation choice
- Good Answer: Default `READ COMMITTED`; use `REPEATABLE READ` for consistency within a request; `SERIALIZABLE` for strict correctness with retry logic.
- Senior Trade-offs: Higher isolation reduces anomalies but increases aborts and contention; apply narrowly.

## 18) Optimistic vs pessimistic locking
- Good Answer: Optimistic with `version`/`updated_at` for most web workloads; pessimistic (`FOR UPDATE`) on short, critical sections with high conflict cost.
- Senior Trade-offs: Optimistic is scalable but requires retries; pessimistic reduces retries but can deadlock.

## 19) Avoiding lost updates
- Good Answer: Add `WHERE version = :v` or `WHERE updated_at = :ts` in `UPDATE`; on failure, refetch and retry.
- Senior Trade-offs: Requires client cooperation and UX for conflict resolution.

## 20) Preventing double-spend
- Good Answer: Enforce invariants in a single transaction with constraints/locks (`SELECT ... FOR UPDATE` on balance row or ledger pattern with unique idempotency keys).
- Senior Trade-offs: Strong guarantees may reduce throughput; idempotency keys add storage overhead.

```sql
-- Idempotency via unique key
CREATE UNIQUE INDEX payments_idempotency_uniq ON payments (idempotency_key);
```

## 21) Savepoints for partial success
- Good Answer: Use savepoints to isolate risky steps and rollback without aborting the entire transaction.
- Senior Trade-offs: Adds overhead and complexity; useful for batch operations.

## 22) Deadlock diagnosis
- Good Answer: Log deadlocks, inspect `pg_locks` and aborted statements; standardize lock order and reduce transaction scope.
- Senior Trade-offs: Smaller transactions reduce windows but increase overhead and partial failure handling.

## 23) Handling phantom reads
- Good Answer: Use `REPEATABLE READ` with predicate locks (via `SELECT ... FOR SHARE` on indexable predicates) or re-check post-commit.
- Senior Trade-offs: Predicate locking reduces concurrency; re-checking adds complexity.

## 24) Cross-service transaction boundaries
- Good Answer: Avoid 2PC; use sagas with idempotent steps and compensations; define clear boundaries.
- Senior Trade-offs: Eventual consistency windows exist; compensation complexity grows.

## 25) Two-phase commit (2PC)
- Good Answer: Only for tightly coupled systems with low latency and high reliability; use cautiously.
- Senior Trade-offs: Coordinator SPOF, locks held longer; often worse than saga for microservices.

## 26) Enforcing at-most-once side effects
- Good Answer: Outbox pattern: write both domain change and outbox event in the same transaction; a relay publishes reliably.
- Senior Trade-offs: Extra table and process; guarantees publication without duplication.

## 27) CDC for downstream sync
- Good Answer: Use logical replication or Debezium to capture changes; consumers apply idempotently.
- Senior Trade-offs: Adds infra and lag; schema changes must be compatible.

## 28) Referential integrity across services
- Good Answer: Avoid cross-service FKs; enforce via contracts and validation; replicate reference data if needed.
- Senior Trade-offs: Lose DB-level guarantees; regain with robust tests and monitoring.

## 29) Enforcing uniqueness across multiple columns
- Good Answer: Composite unique constraints (e.g., `(tenant_id, email)`), possibly partial.
- Senior Trade-offs: Composite keys grow indexes; document business keys clearly.

## 30) Using partial indexes for active records
- Good Answer: Index only `WHERE status='ACTIVE'` or `deleted_at IS NULL` to save space and speed queries.
- Senior Trade-offs: Risk of predicate drift; ensure queries align with predicate.

## 31) Handling large ENUM evolution
- Good Answer: Prefer lookup table + FK or `text` with check constraint; `ENUM` needs migrations and can be painful across services.
- Senior Trade-offs: Lookup tables are flexible; ENUM is compact and fast but rigid.

## 32) Modeling audit trails
- Good Answer: Append-only audit table with `who, when, action, before/after`; use triggers or app logic.
- Senior Trade-offs: Triggers ensure completeness; app logic is explicit but error-prone.

## 33) Row-Level Security (RLS)
- Good Answer: Use RLS for multi-tenant access control; policies per role; always combine with app checks.
- Senior Trade-offs: Powerful but can be misconfigured; harder to reason about; test thoroughly.

## 34) Data retention and TTL
- Good Answer: Partition by time and drop old partitions; or scheduled deletes with batch limits.
- Senior Trade-offs: Partition drop is fast; schema complexity and planning overhead.

## 35) Modeling optional relationships
- Good Answer: Nullable FK with constraint rules; avoid polymorphic columns when possible.
- Senior Trade-offs: Nullable FKs add complexity to joins; acceptable for optionality.

## 36) Unique constraint with soft delete
- Good Answer: Partial unique index on `deleted_at IS NULL`.
- Senior Trade-offs: Must ensure all queries filter out deleted rows appropriately.

## 37) Handling address normalization
- Good Answer: Normalize country/state to reference tables; store freeform address lines for flexibility.
- Senior Trade-offs: Reference integrity vs flexibility for international addresses.

## 38) EAV anti-pattern
- Good Answer: Avoid EAV unless necessary; consider JSONB with expression indexes; for hot attributes, split columns.
- Senior Trade-offs: EAV flexible but terrible for queries; JSONB middle ground.

## 39) Large text search requirements
- Good Answer: Use full text search (`tsvector`) or external search (Elasticsearch); keep canonical data in Postgres.
- Senior Trade-offs: External search scales and features but adds eventual consistency and ops.

## 40) Enforcing one-to-one
- Good Answer: Unique FK on the child referencing parent id; or share primary key.
- Senior Trade-offs: PK-FK sharing enforces strict 1:1 but complicates inserts.

## 41) Optimizing reads with materialized views
- Good Answer: Precompute heavy joins/aggregations; refresh on schedule or on data change triggers.
- Senior Trade-offs: Freshness lag and maintenance cost; `CONCURRENTLY` to avoid blocking.

## 42) Choosing generated columns
- Good Answer: Use generated columns for deterministic derived values; index them.
- Senior Trade-offs: Simpler than triggers; limited to immutable expressions.

## 43) Dealing with high-cardinality parent-child
- Good Answer: Index child FK; denormalize parent attributes used in filters if needed.
- Senior Trade-offs: Denormalization risks staleness; keep authoritative source.

## 44) Composite vs surrogate keys in junctions
- Good Answer: Composite PK `(a_id, b_id)` is fine; add surrogate key only if needed for referencing elsewhere.
- Senior Trade-offs: Surrogate adds simplicity for further FKs but duplicates uniqueness.

## 45) Handling money types
- Good Answer: Store in `numeric(19,4)` or smallest currency unit `bigint`; avoid float.
- Senior Trade-offs: Integer is fast and safe; numeric avoids manual scaling but slower.

## 46) Precision timestamps
- Good Answer: Use `timestamptz` with UTC; avoid timezone-naive `timestamp`.
- Senior Trade-offs: `timestamptz` avoids ambiguity; storage overhead negligible.

## 47) Default values and immutability
- Good Answer: Use `DEFAULT now()` for created timestamps; consider immutability with triggers to prevent updates.
- Senior Trade-offs: Triggers add write cost; can be necessary for compliance.

## 48) Partitioning and foreign keys
- Good Answer: Native partitioned tables support FKs referencing partitioned parents; cross-partition child FKs are limited; design accordingly.
- Senior Trade-offs: Schema complexity increases; test constraints.

## 49) Large bulk imports with constraints
- Good Answer: Stage in unlogged table, validate with constraints and checks, then `INSERT ... SELECT` into target.
- Senior Trade-offs: Staging adds steps but isolates bad data.

## 50) Data seeding strategies
- Good Answer: Use migration scripts for deterministic seeds; avoid app-boot seeding in prod.
- Senior Trade-offs: Migrations are auditable; boot-time seeds can race.

## 51) Temporal validity checks
- Good Answer: CHECK `valid_from <= valid_to`; unique constraint on overlapping intervals via exclusion constraints.
- Senior Trade-offs: Exclusion constraints are powerful but heavier than simple uniques.

```sql
CREATE EXTENSION IF NOT EXISTS btree_gist;
CREATE TABLE reservations (
  room_id bigint,
  during tstzrange,
  EXCLUDE USING gist (room_id WITH =, during WITH &&)
);
```

## 52) Enforcing inventory not below zero
- Good Answer: Use single transaction with `CHECK` and `FOR UPDATE` on inventory rows; or use an aggregate ledger with constraint.
- Senior Trade-offs: Locks serialize hot items; ledger scales with idempotency and unique events.

## 53) Idempotent write APIs
- Good Answer: Require client-provided idempotency keys; store and enforce unique.
- Senior Trade-offs: Storage and key management overhead; enables safe retries.

## 54) Handling hot rows
- Good Answer: Shard counters (e.g., with hash suffix) and aggregate; or use advisory locks to serialize updates.
- Senior Trade-offs: Sharding counters complicates reads; locks reduce concurrency.

## 55) Advisory locks for coordination
- Good Answer: Use `pg_advisory_xact_lock(key)` for short-lived critical sections.
- Senior Trade-offs: No automatic deadlock detection across unrelated keys; keep granularity consistent.

## 56) Large DELETEs without downtime
- Good Answer: Batch deletes with LIMIT and indexed predicates; detach/drop partitions for time-based data.
- Senior Trade-offs: Longer maintenance window vs less blocking.

## 57) Enforcing exactly-one active record per group
- Good Answer: Partial unique index on `(group_id)` where `is_active=true`.
- Senior Trade-offs: Requires consistent updates to toggle flags.

## 58) Auditability of changes
- Good Answer: Triggers that write to audit tables with user context; use `session_user` and `current_setting` for app-set metadata.
- Senior Trade-offs: Triggers increase write latency; provide strong guarantees.

## 59) Large reference data lookups
- Good Answer: Cache in app/Redis with versioning; keep authoritative table with strict constraints.
- Senior Trade-offs: Cache staleness risk; version keys and TTLs mitigate.

## 60) Schema evolution with zero downtime
- Good Answer: Backward-compatible changes first; dual-write/read; migrate; then clean up.
- Senior Trade-offs: Temporary complexity; safer deploys.

## 61) Backfilling new columns
- Good Answer: Add column nullable; backfill in chunks; add `NOT NULL` with `VALIDATE` style.
- Senior Trade-offs: Longer window; minimal lock time.

## 62) Renaming columns safely
- Good Answer: Add new column, write to both, read from both; update code; then drop old.
- Senior Trade-offs: More code paths temporarily.

## 63) Avoiding long-running transactions
- Good Answer: Keep migrations and batch jobs chunked; commit frequently; monitor `xid` age.
- Senior Trade-offs: More commits overhead; healthier vacuum.

## 64) Preventing dead tuples growth
- Good Answer: Tune autovacuum per table; avoid idle-in-transaction sessions; monitor bloat.
- Senior Trade-offs: Maintenance IO vs space/time efficiency.

## 65) Consistent reads across multiple queries
- Good Answer: Use `REPEATABLE READ` to keep snapshot; or store snapshot IDs and re-check at boundaries.
- Senior Trade-offs: Higher isolation increases aborts.

## 66) Event sourcing vs state storage
- Good Answer: Event sourcing for auditability and rebuilds; snapshot for fast reads; or hybrid: events + materialized projection.
- Senior Trade-offs: Complex to implement; powerful audit and time-travel.

## 67) Ensuring foreign key performance
- Good Answer: Index child FK columns; index parent PK by default; avoid unindexed FKs.
- Senior Trade-offs: Extra indexes cost writes; necessary for deletions and joins.

## 68) Handling orphan records
- Good Answer: Enforce FK `ON DELETE CASCADE/SET NULL` appropriately; audit cascades.
- Senior Trade-offs: Cascade can delete large graphs; monitor impact.

## 69) Multi-region data modeling
- Good Answer: Keep data local per region (shard by region) with global directory where needed; async replicate for read-only views.
- Senior Trade-offs: Global consistency hard; favor locality and eventual convergence.

## 70) GDPR delete vs audit
- Good Answer: Pseudonymize PII; keep structural audit sans PII; hard delete where legally required.
- Senior Trade-offs: Trade compliance with operational audit needs; design schemas to isolate PII.

## 71) Numeric precision choices
- Good Answer: Use `numeric(p,s)` for money; `bigint` for counters; avoid float for financial values.
- Senior Trade-offs: Numeric slower but precise; bigint fast but requires scaling logic.

## 72) Default timestamps and clock skew
- Good Answer: Use `now()` in DB; avoid application-provided timestamps for created_at; keep everything UTC.
- Senior Trade-offs: DB clock is single source but must be NTP synced.

## 73) Preventing duplicate business operations
- Good Answer: Unique constraints on business keys + idempotency keys.
- Senior Trade-offs: Requires careful key lifecycle and retries.

## 74) Unique within time window
- Good Answer: Use exclusion constraints with ranges (e.g., unique booking per user per hour).
- Senior Trade-offs: Heavier than simple uniques; test performance.

## 75) Modeling status transitions
- Good Answer: State machine table or enum + transition table; validate transitions via triggers or app logic.
- Senior Trade-offs: Stronger guarantees vs more overhead.

## 76) Batch updates with minimal locking
- Good Answer: Update in PK order, small batches; avoid hot WHERE patterns; monitor locks.
- Senior Trade-offs: Longer runtime; safer concurrency.

## 77) Idempotent consumers in event-driven systems
- Good Answer: Store processed message IDs with unique constraint; skip duplicates.
- Senior Trade-offs: Storage overhead; prevents reprocessing.

## 78) Distributed unique IDs
- Good Answer: Use UUIDv7 or snowflake IDs generated at edge; avoid central contention.
- Senior Trade-offs: Larger keys, ordering properties vary; ensure index-ability.

## 79) Check constraints for JSONB
- Good Answer: Use `jsonb_typeof` and path operators in `CHECK` for minimal validation.
- Senior Trade-offs: Complex checks better in app; keep DB checks simple.

## 80) Partial indexes for hot subsets
- Good Answer: Index active subsets; keep predicates aligned to queries.
- Senior Trade-offs: Maintenance complexity if predicates change.

## 81) Collation and case rules
- Good Answer: Use ICU collations where needed; for case-insensitive, prefer `citext` or `lower()` functional index.
- Senior Trade-offs: Changing collation requires rebuild; global impact on sorting.

## 82) RLS policy versioning
- Good Answer: Version policies with feature flags; test with representative data.
- Senior Trade-offs: Policy bugs are production incidents; invest in tests.

## 83) Bulk upsert patterns
- Good Answer: Use `INSERT ... ON CONFLICT ... DO UPDATE` with minimal update set; batch by key.
- Senior Trade-offs: Contention on hot keys; consider partitioning or queues.

## 84) Referential cycles
- Good Answer: Break cycles with nullable FK and post-insert updates or use deferrable constraints.
- Senior Trade-offs: Deferrable constraints add validation at commit; cycles complicate deletes.

## 85) Deferrable constraints for staging
- Good Answer: `DEFERRABLE INITIALLY DEFERRED` for complex loads; validate at commit.
- Senior Trade-offs: Errors discovered late; debugging harder.

## 86) Large table design for updates
- Good Answer: Group mutable columns into a separate table to reduce churn on wide rows.
- Senior Trade-offs: More joins; reduces bloat and improves cache locality.

## 87) Hot partition avoidance
- Good Answer: Hash sub-partition or add salt in keys; spread load.
- Senior Trade-offs: Increases partition count and complexity.

## 88) Time-zone handling in UI and DB
- Good Answer: Store as UTC `timestamptz`, convert at client/UI; never store local times.
- Senior Trade-offs: None significant; correctness improves.

## 89) Enforcing min/max cardinality
- Good Answer: Use triggers to enforce “at least one/at most N” relationships.
- Senior Trade-offs: Triggers add write overhead; sometimes better handled in app.

## 90) Data localization laws
- Good Answer: Shard by region and restrict cross-region PII; encrypt at rest with KMS per region.
- Senior Trade-offs: Operational complexity; satisfies compliance.

## 91) Read-your-writes consistency
- Good Answer: Serve reads from primary for sessions requiring RYW; or pin to primary temporarily.
- Senior Trade-offs: Higher latency; ensures correctness.

## 92) Statement timeouts
- Good Answer: Set `statement_timeout` per role or session; fail fast and retry where safe.
- Senior Trade-offs: False positives under transient load; tune with SLOs.

## 93) Enforcing invariants with exclusion constraints
- Good Answer: Use GiST/BRIN where fits (ranges, geospatial).
- Senior Trade-offs: More complex indexing and maintenance.

## 94) Data masking in lower envs
- Good Answer: ETL with masking of PII; preserve shapes and distributions.
- Senior Trade-offs: Masking cost; required for privacy.

## 95) Row version stamping
- Good Answer: `xmin` can be used for MVCC hints but not business logic; use explicit `version` column for optimistic locking.
- Senior Trade-offs: `xmin` resets on dump/restore; explicit version portable.

## 96) Multi-column search keys
- Good Answer: Composite indexes in query order; use covering indexes with INCLUDE for selects.
- Senior Trade-offs: More/larger indexes; balance against write cost.

## 97) Enforcing FK on large existing data
- Good Answer: Add `NOT VALID` constraint; validate separately to avoid long locks.
- Senior Trade-offs: Temporary window without full enforcement; plan validation window.

## 98) Tracking ownership changes over time
- Good Answer: Temporal table for ownership with valid ranges; use constraints to prevent overlap.
- Senior Trade-offs: Query complexity vs auditability.

## 99) Ensuring idempotent migrations
- Good Answer: Make migrations re-runnable (IF EXISTS/IF NOT EXISTS); include guards and checksums.
- Senior Trade-offs: More defensive code; safer deploys.

## 100) SLO-driven schema decisions
- Good Answer: Model to meet read/write latency and integrity SLOs; benchmark and iterate; keep migration paths open.
- Senior Trade-offs: Balancing correctness, cost, and agility is ongoing; prefer reversible decisions.

---

## Handy SQL Patterns
```sql
-- Optimistic locking
UPDATE accounts
SET balance = balance - 100, version = version + 1
WHERE id = $1 AND version = $2;

-- Soft delete with partial unique
UPDATE users SET deleted_at = now() WHERE id = $1;
-- Unique among active only
CREATE UNIQUE INDEX users_email_active_uniq ON users (lower(email)) WHERE deleted_at IS NULL;

-- Idempotent event outbox
CREATE TABLE outbox (
  id bigint generated always as identity primary key,
  aggregate_id uuid not null,
  type text not null,
  payload jsonb not null,
  created_at timestamptz default now(),
  published_at timestamptz
);

-- Validate FK without long lock
ALTER TABLE child
  ADD CONSTRAINT child_parent_fk FOREIGN KEY (parent_id)
  REFERENCES parent(id) NOT VALID;
ALTER TABLE child VALIDATE CONSTRAINT child_parent_fk;
```
