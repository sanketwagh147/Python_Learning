# Python AsyncIO & Concurrency in Microservices — 100 Scenario-Based Interview Questions

Each scenario includes a Good Answer and a Senior-Level trade-off explanation. Code examples are included where useful.

## Purpose & How To Use
- Build from fundamentals (event loop, tasks, cancellations) to production concerns (backpressure, deadlines, idempotency, graceful shutdown).
- Evaluate for: async purity, bounded concurrency, clear timeout/cancellation semantics, and resilience under failures.
- Ask: “What happens if a downstream hangs?”, “How do we prevent threadpool starvation?”, “How do we propagate deadlines?”
## What Senior Engineers (4-5 YOE) Should Demonstrate
1. **Concurrency Mastery**: Understand event loop mechanics; design for cooperative multitasking; avoid common pitfalls (blocking, unbounded fan-out).
2. **Distributed Systems Thinking**: Design for partial failures; implement proper timeout/retry/circuit-breaker patterns; understand consistency trade-offs.
3. **Debugging Complex Issues**: Diagnose event loop stalls, memory leaks, and race conditions; use appropriate tooling (py-spy, tracemalloc).
4. **Code Review Excellence**: Spot async anti-patterns; ensure proper resource cleanup; verify cancellation safety.
5. **Team Enablement**: Establish async patterns for the team; write documentation; mentor on concurrency concepts.

## Mental Model: Async Request Lifecycle
```
Request In → ASGI → Middleware Stack → Route Handler
                                         │
                            ┌─────────────┴─────────────┐
                            │                          │
                      Await DB Query            Await HTTP Call
                            │                          │
                            └─────────────┬─────────────┘
                                         │
                                    Aggregate Results
                                         │
                              Response ← Serialize ← Validate

Key insight: While awaiting, the event loop serves OTHER requests.
Blocking anywhere = ALL requests suffer.
```
## Key Concepts Primer
- Event loop & tasks: Cooperative multitasking via `await`; avoid blocking calls.
- Concurrency controls: `Semaphore`, connection pools, bounded queues; prevent unbounded fan-out.
- Cancellation & deadlines: `asyncio.timeout`, `CancelledError` handling, `TaskGroup` structured concurrency.
- Offloading: CPU → process pool; blocking IO → threadpool; measure queue lengths to detect pressure.
- Context propagation: `contextvars` for request IDs and deadlines across awaits and threadpools.

## Mini Case Study: Fan-out with Deadline Budget
Goal: Aggregate 50 downstream calls with a 300ms deadline while avoiding overload.
Solution: Use bounded gather, per-call timeouts derived from a shared deadline, and cancel in-flight laggards.

```python
import asyncio, time

async def call_one(i, budget_s):
    return await asyncio.wait_for(asyncio.sleep(0.02), budget_s)

async def aggregate(ids, deadline_s=0.3, max_conc=10):
    start = time.monotonic()
    sem = asyncio.Semaphore(max_conc)
    async def wrap(i):
        async with sem:
            remaining = max(0.0, deadline_s - (time.monotonic() - start))
            return await call_one(i, remaining or 0.001)
    coros = [wrap(i) for i in ids]
    results = []
    for fut in asyncio.as_completed(coros, timeout=deadline_s):
        try:
            results.append(await fut)
        except Exception:
            pass
    return results
```

## Async Anti-Patterns & Fixes

### Anti-Pattern 1: Blocking the Event Loop
```python
# ❌ BAD: Blocks entire event loop
@app.get("/users/{user_id}")
async def get_user(user_id: int):
    user = db.query(User).filter(User.id == user_id).first()  # Sync call!
    return user

# ✅ GOOD: Use async driver
@app.get("/users/{user_id}")
async def get_user(user_id: int):
    async with async_session() as session:
        result = await session.execute(select(User).where(User.id == user_id))
        return result.scalar_one_or_none()

# ✅ GOOD: Offload to threadpool if async driver unavailable
@app.get("/users/{user_id}")
async def get_user(user_id: int):
    return await run_in_threadpool(sync_get_user, user_id)
```

### Anti-Pattern 2: Unbounded Concurrency
```python
# ❌ BAD: Can overwhelm downstream
async def fetch_all(urls: list[str]):
    return await asyncio.gather(*[fetch(url) for url in urls])

# ✅ GOOD: Bounded concurrency
async def fetch_all(urls: list[str], max_concurrent: int = 10):
    semaphore = asyncio.Semaphore(max_concurrent)
    async def fetch_with_limit(url):
        async with semaphore:
            return await fetch(url)
    return await asyncio.gather(*[fetch_with_limit(url) for url in urls])
```

### Anti-Pattern 3: Fire-and-Forget Without Tracking
```python
# ❌ BAD: Lost reference, no cleanup on shutdown
@app.post("/send-email")
async def send_email(email: EmailRequest):
    asyncio.create_task(actually_send_email(email))  # Fire and forget
    return {"status": "queued"}

# ✅ GOOD: Track tasks, cleanup on shutdown
background_tasks: set[asyncio.Task] = set()

@app.post("/send-email")
async def send_email(email: EmailRequest):
    task = asyncio.create_task(actually_send_email(email))
    background_tasks.add(task)
    task.add_done_callback(background_tasks.discard)
    return {"status": "queued"}

@app.on_event("shutdown")
async def cleanup():
    for task in background_tasks:
        task.cancel()
    await asyncio.gather(*background_tasks, return_exceptions=True)
```

### Anti-Pattern 4: Ignoring Cancellation
```python
# ❌ BAD: Doesn't handle cancellation
async def process_order(order_id: int):
    await charge_payment(order_id)
    await send_confirmation(order_id)  # If cancelled here, payment charged but no email

# ✅ GOOD: Cancellation-safe with compensation
async def process_order(order_id: int):
    payment_id = None
    try:
        payment_id = await charge_payment(order_id)
        await send_confirmation(order_id)
    except asyncio.CancelledError:
        if payment_id:
            await refund_payment(payment_id)  # Compensate
        raise  # Re-raise to propagate cancellation
```

## Debugging Async Issues

### Find Blocking Calls with py-spy
```bash
# Attach to running process
py-spy top --pid <PID>

# Record flame graph
py-spy record -o profile.svg --pid <PID> --duration 30
```

### Find Event Loop Stalls
```python
import asyncio

# Enable debug mode
asyncio.get_event_loop().set_debug(True)

# Or via environment
# PYTHONASYNCIODEBUG=1 python app.py
```

### Track Task Leaks
```python
async def debug_tasks():
    tasks = asyncio.all_tasks()
    for task in tasks:
        print(f"Task: {task.get_name()}, Done: {task.done()}, Cancelled: {task.cancelled()}")
        if not task.done():
            task.print_stack()
```

## Common Pitfalls
- Fire-and-forget tasks without references → zombie tasks; no cleanup on shutdown.
- Large blocking work on the event loop; starves unrelated requests.
- Unbounded `gather` over large lists; downstream overload and timeouts.
- Missing idempotency on retries; duplicate side effects.

## Evaluation Rubric (Interview)

### Junior (1-2 YOE)
- Understands `async`/`await` syntax
- Can write basic async endpoints
- Knows to avoid blocking calls

### Mid-Level (3-4 YOE)
- Uses semaphores and connection pools correctly
- Handles timeouts and basic error cases
- Can debug simple async issues

### Senior (4-5 YOE) — Target Level
- **Async rigor**: Designs cancellation-safe code; uses structured concurrency (`TaskGroup`); proper cleanup in all paths
- **Concurrency design**: Calculates pool sizes; implements backpressure; designs for bounded fan-out
- **Failure semantics**: Implements proper deadline propagation; designs retry strategies; uses circuit breakers effectively
- **Debugging**: Uses py-spy/tracemalloc; diagnoses event loop stalls; finds resource leaks
- **Leadership**: Establishes async patterns; reviews PRs for concurrency issues; mentors team

### Staff+ (6+ YOE)
- Designs async infrastructure (custom event loops, protocols)
- Establishes organization-wide concurrency patterns
- Contributes to async libraries or frameworks

---

## 1) Blocking I/O discovered in hot async endpoint
- Good Answer: Identify blocking calls (file, DNS, heavy CPU) and wrap with `asyncio.to_thread()` or `run_in_threadpool`, or move to a worker queue. Keep the event loop non-blocking.
- Senior Trade-offs: Threadpools hide blocking but add context switch overhead and can starve under bursty load; queues add durability and backpressure at the cost of latency and ops.

## 2) Handling CPU-bound work in async service
- Good Answer: Offload CPU-heavy tasks to a process pool or a separate worker (Celery/RQ); avoid blocking the event loop.
- Senior Trade-offs: Process pools bypass the GIL but cost memory and IPC; external queues add retries and monitoring complexity.

## 3) Diagnosing event loop stalls
- Good Answer: Enable `PYTHONASYNCIODEBUG=1`, use `asyncio.get_running_loop().slow_callback_duration`, add sampling profilers (`py-spy`) under load tests.
- Senior Trade-offs: Debugging adds overhead; enable only in staging or sampled in prod.

## 4) Preventing unbounded concurrency
- Good Answer: Use `asyncio.Semaphore` or connection pool limits; bound concurrent tasks per endpoint.
- Senior Trade-offs: Tight limits protect dependencies but may reduce throughput; size with load tests.

## 5) Coordinating cancellations safely
- Good Answer: Use `asyncio.TaskGroup` (3.11+) or cancel scopes; always `await` tasks and handle `CancelledError` to release resources.
- Senior Trade-offs: Eager cancellation reduces wasted work but risks partial effects; add compensating actions.

## 6) Proper timeout handling
- Good Answer: Wrap awaits in `asyncio.timeout()` or `asyncio.wait_for()` with clear error mapping; propagate deadlines across service calls.
- Senior Trade-offs: Aggressive timeouts fail fast but amplify retry storms; coordinate at the platform level.

## 7) Avoiding N+1 over HTTP
- Good Answer: Batch downstream requests, add bulk APIs, or use read-through caches; coordinate with downstream owners.
- Senior Trade-offs: Batching increases payload size and tail latency; requires pagination and partial-failure handling.

## 8) DNS resolution latency
- Good Answer: Reuse a single `httpx.AsyncClient`/`aiohttp.ClientSession` with connection pooling and DNS caching; tune TTLs.
- Senior Trade-offs: Long-lived caches risk stale DNS during failovers; add periodic refresh.

## 9) Preventing threadpool starvation
- Good Answer: Limit blocking work dispatched to threads; size threadpool based on CPU and blocking profile; monitor queue length.
- Senior Trade-offs: Too small blocks progress; too large thrashes and increases context switches.

## 10) Backpressure on inbound requests
- Good Answer: Implement a small internal request queue with limits; return 503 when saturated; expose queue depth.
- Senior Trade-offs: Shedding protects service but impacts availability; align with SLOs.

## 11) Async DB access best practices
- Good Answer: Use async drivers (`asyncpg`, SQLAlchemy 2.x async), keep transactions short, cap pool size per worker, avoid long-lived cursors.
- Senior Trade-offs: Async drivers need careful lifetime management; over-large pools degrade DB.

## 12) PgBouncer + prepared statements
- Good Answer: With transaction pooling, disable server-side prepared statements or upgrade PgBouncer to versions with better handling; prefer statement caching client-side.
- Senior Trade-offs: Prepared statements reduce latency but can break across pooled connections.

## 13) Connection leaks detection
- Good Answer: Use context managers for sessions; add leak detectors in tests; expose pool metrics and timeouts.
- Senior Trade-offs: Strict timeouts may fail healthy requests under transient slowness.

## 14) Handling partial failures across services
- Good Answer: Use timeouts + retries with idempotency; apply circuit breakers; provide graceful fallbacks.
- Senior Trade-offs: Fallbacks may serve stale/partial data; document behavior.

## 15) Implementing rate limiting
- Good Answer: Token bucket in Redis with LUA/atomic ops; per-tenant/IP limits and burst handling.
- Senior Trade-offs: Central dependency; ensure HA and latency budgets.

## 16) Idempotency for POST
- Good Answer: Require idempotency keys stored in Redis/DB with TTL; dedupe on retries.
- Senior Trade-offs: Storage overhead and key management; race handling.

## 17) Managing large responses
- Good Answer: Use `StreamingResponse`/chunked encoding; support range requests; avoid buffering entire payloads.
- Senior Trade-offs: Streaming complicates error handling and backpressure.

## 18) Large uploads
- Good Answer: Stream uploads to disk/S3; enforce limits; virus scan async; return 202 if needed.
- Senior Trade-offs: Extra IO and temp storage; careful cleanup required.

## 19) WebSocket scaling
- Good Answer: Dedicated WS worker class; Redis pub/sub or message broker; shard by topic/tenant.
- Senior Trade-offs: WS state complicates horizontal scaling; consider SSE for one-way feeds.

## 20) Async file IO
- Good Answer: Use `aiofiles` for local disk; avoid synchronous file ops in hot paths.
- Senior Trade-offs: Filesystems may still block under contention.

## 21) Structured concurrency
- Good Answer: Prefer `asyncio.TaskGroup` for grouped tasks with shared cancellation semantics.
- Senior Trade-offs: Cancelling the group aborts all tasks; design idempotent work units.

## 22) Context propagation
- Good Answer: Use `contextvars` to propagate request IDs and auth context across tasks and threadpools.
- Senior Trade-offs: Crossing process boundaries loses context; serialize in headers/metadata.

## 23) Hedged requests to slow downstream
- Good Answer: Issue a second request after a small delay; cancel slower one when a fast response returns.
- Senior Trade-offs: Doubles load; restrict to critical endpoints and high percentiles.

## 24) Retry storms mitigation
- Good Answer: Global jittered backoff, max-inflight caps, and circuit breakers; cap retries per hop.
- Senior Trade-offs: Complexity in coordination; prevents meltdowns.

## 25) Async metrics and tracing
- Good Answer: Non-blocking instrumentation; batch exports; sampling for traces.
- Senior Trade-offs: Lower fidelity vs lower overhead; pick per-SLO.

## 26) Memory leaks in long-lived services
- Good Answer: Use `tracemalloc`, periodic heap snapshots; check caches and task lifetimes; load test to steady state.
- Senior Trade-offs: Profiling perturbs performance; run in staging.

## 27) Managing event loop per process
- Good Answer: One loop per process; do not share across threads. In worker setups, initialize clients in startup hooks.
- Senior Trade-offs: Multiprocess increases memory; isolate failures.

## 28) Async ORM pitfalls
- Good Answer: Avoid implicit lazy loads; use explicit `selectinload`/`joinedload`; keep sessions short.
- Senior Trade-offs: Eager loading can over-fetch; measure queries.

## 29) Fairness among tasks
- Good Answer: Avoid long CPU loops; `await` periodically; use queues and cooperative design.
- Senior Trade-offs: More awaits can add overhead; balance fairness vs throughput.

## 30) Deadlocks in async code
- Good Answer: Avoid holding semaphores across awaits to foreign code; define consistent lock order; use timeouts.
- Senior Trade-offs: Fine-grained locks reduce contention but increase complexity.

## 31) Async-friendly caches
- Good Answer: Use `aioredis`/`redis.asyncio`; stampede protection with locks; set TTL and version keys.
- Senior Trade-offs: Locks can serialize; use short TTLs and jitter.

## 32) Graceful shutdown
- Good Answer: Implement lifespan shutdown to close pools/clients; stop accepting new work; await task groups.
- Senior Trade-offs: Longer drain increases deploy times; too short risks lost work.

## 33) Ephemeral port exhaustion
- Good Answer: Reuse connections (keep-alive), bound concurrency, increase client pool; avoid per-request client creation.
- Senior Trade-offs: Long-lived connections need health checks and DNS refresh.

## 34) Timeout budgets across hops
- Good Answer: Propagate deadline headers; subtract local processing time; enforce at each hop.
- Senior Trade-offs: Strict budgets drop work; choose SLAs per endpoint.

## 35) Async schedulers vs cron
- Good Answer: Use APScheduler/Arq for async cron; separate scheduling process from request handling.
- Senior Trade-offs: Separate services add ops overhead but isolate failures.

## 36) Batching DB writes
- Good Answer: Use `executemany` or COPY for bulk, within transaction limits; apply chunking.
- Senior Trade-offs: Large transactions lock longer; chunk to balance.

## 37) Queue backpressure
- Good Answer: Use bounded `asyncio.Queue`; producers `await` when full; expose metrics.
- Senior Trade-offs: Too small queue hurts throughput; too large hides pressure.

## 38) Async file parsing large JSON
- Good Answer: Stream parser or chunked processing; avoid building huge dicts; validate in pieces.
- Senior Trade-offs: Complex validation; error handling across chunks.

## 39) SSE vs WebSockets
- Good Answer: SSE for one-way updates; WS for bidirectional low-latency comms.
- Senior Trade-offs: SSE simpler but limited; WS needs state and scaling support.

## 40) Using uvloop
- Good Answer: Prefer `uvicorn[standard]` to get uvloop; validate library compatibility.
- Senior Trade-offs: uvloop is faster but not universal.

## 41) Async test strategies
- Good Answer: Use `pytest-asyncio` and `anyio` fixtures; fake downstreams with `respx`/`aioresponses`.
- Senior Trade-offs: Async tests can be slower; run a representative subset in CI.

## 42) Circuit breaker implementation
- Good Answer: Track failure rates/timeouts; open circuit and probe via half-open; integrate with retries and deadlines.
- Senior Trade-offs: Mis-tuned breakers cause unnecessary failures.

## 43) Distributed locks
- Good Answer: Use Redis Redlock cautiously or Postgres advisory locks; keep timeouts short.
- Senior Trade-offs: Redlock guarantees debated; prefer single-writer designs when possible.

## 44) Context managers for resources
- Good Answer: Wrap sessions/clients in async context managers; ensure `aclose()` on shutdown.
- Senior Trade-offs: More boilerplate but fewer leaks.

## 45) Handling client disconnects
- Good Answer: Check `request.is_disconnected()` (framework-specific); cancel work promptly.
- Senior Trade-offs: Early cancel saves resources but complicates idempotency.

## 46) Pool sizing math
- Good Answer: Align HTTP and DB pools with worker count and SLO; e.g., per process 10–20 DB connections max.
- Senior Trade-offs: Overprovisioning pools harms downstreams; underprovisioning wastes CPU.

## 47) Request-scoped vs app-scoped dependencies
- Good Answer: App-scope singletons for clients/pools; request-scope for per-request context.
- Senior Trade-offs: Singletons risk state leaks; immutable design mitigates.

## 48) AnyIO vs asyncio
- Good Answer: AnyIO provides portability (Trio/asyncio) and structured concurrency; good for libraries.
- Senior Trade-offs: Abstraction adds dependency and potential overhead.

## 49) Async generator cleanup
- Good Answer: Ensure `aclose()` on async generators; use `async with` patterns.
- Senior Trade-offs: Leaks otherwise; slightly more code.

## 50) Cancellation safety around DB
- Good Answer: Use `shield` or finalize statements to avoid half-written state; wrap critical sections.
- Senior Trade-offs: Shielding reduces responsiveness to cancel; use sparingly.

## 51) Handling partial results aggregation
- Good Answer: Use `gather(return_exceptions=True)` and filter results; avoid all-or-nothing when acceptable.
- Senior Trade-offs: Needs clear error semantics for clients.

## 52) Dealing with slow GC
- Good Answer: Tune GC thresholds; prefer object reuse; avoid large cyclical graphs.
- Senior Trade-offs: Aggressive tuning risks memory growth.

## 53) Async-friendly pagination
- Good Answer: Keyset pagination to reduce server work and latency.
- Senior Trade-offs: Client complexity and strict sort requirements.

## 54) Protecting downstream databases
- Good Answer: Use concurrency semaphores per dependency; queue excess requests.
- Senior Trade-offs: Limits latency; prioritize critical traffic.

## 55) Handling long polls
- Good Answer: Prefer SSE/WS; if long-poll, cap duration and frequency.
- Senior Trade-offs: Long polls tie connections; scale accordingly.

## 56) Coordinating multiple deadlines
- Good Answer: Use a single deadline budget object propagated via headers/context.
- Senior Trade-offs: Extra plumbing but consistent behavior.

## 57) Async retries with idempotency
- Good Answer: Only retry idempotent operations; add dedupe keys for POST.
- Senior Trade-offs: Complexity in key lifecycle; storage overhead.

## 58) Event-driven microservices
- Good Answer: Use Kafka/NATS; process with async consumers; commit offsets after durable write.
- Senior Trade-offs: At-least-once processing requires idempotency; exactly-once is complex.

## 59) Consumer backpressure
- Good Answer: Limit max in-flight messages; pause/resume consumption; scale consumer groups.
- Senior Trade-offs: Lag increases; manage replay windows.

## 60) Ordering guarantees
- Good Answer: Use partition keys for per-entity ordering; avoid cross-partition ordering assumptions.
- Senior Trade-offs: Hot partitions under skew; trade ordering vs balance.

## 61) Saga patterns
- Good Answer: Orchestrate via a saga coordinator or choreography with compensations; design idempotent steps.
- Senior Trade-offs: More moving parts; eventual consistency windows.

## 62) Telemetry correlation
- Good Answer: Pass traceparent/request-id via headers; store in `contextvars` for logs/metrics.
- Senior Trade-offs: PII handling; sampling strategies.

## 63) Graceful degrade modes
- Good Answer: Feature flags to disable heavy features; serve cached results.
- Senior Trade-offs: Product impact; ensure UX fallbacks.

## 64) Async feature flag checks
- Good Answer: Cache flag state per process; refresh periodically; avoid per-request DB calls.
- Senior Trade-offs: Stale flags briefly; acceptable for resilience.

## 65) JSON serialization hot path
- Good Answer: Use `orjson` for dumps; pre-serialize large responses; avoid double-validation.
- Senior Trade-offs: Strict types; compatibility checks.

## 66) Guarding against runaway tasks
- Good Answer: Track tasks via registry; cancel on shutdown; add watchdog for long-runners.
- Senior Trade-offs: False positives; careful thresholds.

## 67) Handling SIGTERM/SIGINT
- Good Answer: Register signal handlers to trigger graceful shutdown; stop intake; drain tasks.
- Senior Trade-offs: Too slow → force kill; too fast → lost work.

## 68) Partial updates aggregation
- Good Answer: Use async maps with concurrency limits; short-circuit on threshold failures.
- Senior Trade-offs: More complex state machine; better tail latency.

## 69) Tuning `uvicorn` workers and connections
- Good Answer: Balance `--workers` and `--worker-connections` with CPU and downstream limits; validate via load tests.
- Senior Trade-offs: Too many workers starve DB; too few underutilize CPU.

## 70) Async-compatible crypto
- Good Answer: Heavy crypto to process pool; avoid blocking in event loop; consider libsodium bindings.
- Senior Trade-offs: IPC overhead vs security needs.

## 71) Caching auth results
- Good Answer: Short-lived cache for JWT verification results/JWKS; refresh keys periodically.
- Senior Trade-offs: Stale revocations vs performance; keep TTL low.

## 72) Duplex streaming with gRPC
- Good Answer: Use aio gRPC for bidirectional streams; bound per-stream buffers; handle flow control.
- Senior Trade-offs: More complex than unary; tooling maturity varies.

## 73) Handling clock skew
- Good Answer: Use monotonic clocks for timeouts; NTP sync nodes.
- Senior Trade-offs: External dependencies on time can still fail; add leeway.

## 74) Async-safe caches in-memory
- Good Answer: Protect with `asyncio.Lock`; avoid blocking operations inside critical sections.
- Senior Trade-offs: Locks serialize; keep scope minimal.

## 75) Bounded map concurrency utility
- Good Answer: Implement `bounded_gather` with semaphore to limit concurrent awaits over large lists.
- Senior Trade-offs: Lower peak but stable latency and resource use.

## 76) Handling slow clients (uploads/downloads)
- Good Answer: Apply per-connection timeouts and streaming; proxy buffering when possible.
- Senior Trade-offs: Timeouts frustrate slow networks; tune per endpoint.

## 77) Cross-service schema evolution
- Good Answer: Backward-compatible JSON contracts; optional fields; server tolerant of unknowns.
- Senior Trade-offs: More validation paths; cleanup debt.

## 78) Async safe temp files
- Good Answer: Use `TemporaryDirectory` with async wrappers or ensure cleanup in finally.
- Senior Trade-offs: Disk pressure; monitor.

## 79) Tuning Python version
- Good Answer: Use Python 3.11/3.12 for faster `asyncio`, `TaskGroup`, and perf improvements.
- Senior Trade-offs: Upgrade/testing cost; watch C-ext compatibility.

## 80) Handling oversized request bodies
- Good Answer: Enforce `Content-Length` limits at proxy; parse streams incrementally.
- Senior Trade-offs: Strict limits reject edge cases; offer chunked alternatives.

## 81) Multitenant fairness
- Good Answer: Per-tenant semaphores/quotas; isolate noisy neighbors.
- Senior Trade-offs: Complexity vs predictable SLOs.

## 82) Large fan-out request
- Good Answer: Use concurrency limits and fallback grouping; cancel slow subsets when budget exceeded.
- Senior Trade-offs: Incomplete results; client-side reconciliation needed.

## 83) Async signal timeouts to DB
- Good Answer: Wrap DB calls with deadlines; ensure server-side statement timeouts.
- Senior Trade-offs: Server-side timeouts avoid zombie queries but may rollback work.

## 84) Handling per-request caches
- Good Answer: Store small per-request memoization in `request.state` or contextvars; clear after response.
- Senior Trade-offs: Memory overhead per request; ensure cleanup.

## 85) Avoiding shared mutable state
- Good Answer: Treat singletons as immutable or guarded by locks; prefer pure functions.
- Senior Trade-offs: Copies increase memory; immutability improves safety.

## 86) Async friendly CSV/Parquet
- Good Answer: Stream CSV line-by-line; offload Parquet to worker due to native libs.
- Senior Trade-offs: CPU-heavy formats require process pools.

## 87) Preventing zombie tasks
- Good Answer: Keep references to tasks in registries and cancel on shutdown; use `TaskGroup`.
- Senior Trade-offs: Slight memory overhead; avoids leaks.

## 88) Testing cancellation paths
- Good Answer: Unit test `CancelledError` handling; fuzz with random cancellation points in CI.
- Senior Trade-offs: More test time; better resilience.

## 89) TLS handshake cost
- Good Answer: Keep-alive connections; HTTP/2 multiplexing; session tickets.
- Senior Trade-offs: Security settings vs latency; edge offload helps.

## 90) Async SMTP/email
- Good Answer: Queue emails for out-of-band send; use async SMTP clients or provider APIs.
- Senior Trade-offs: Deliverability vs latency; retries and DLQs.

## 91) Middlewares and ordering
- Good Answer: Place tracing/logging early, auth next, business logic later; avoid I/O in early middlewares.
- Senior Trade-offs: Ordering affects visibility and cost.

## 92) Payload decompression cost
- Good Answer: Offload decompression to proxy where possible; limit accepted encodings.
- Senior Trade-offs: Less CPU in app; more proxy responsibility.

## 93) Per-request time slicing
- Good Answer: Avoid long CPU-bound loops; insert `await asyncio.sleep(0)` in rare cases to yield.
- Senior Trade-offs: Sleep(0) is a hint; misuse can degrade throughput.

## 94) Async RPC libraries
- Good Answer: For internal RPC, evaluate gRPC aio or async HTTP with MessagePack; enforce deadlines and budgets.
- Senior Trade-offs: Tooling and observability maturity.

## 95) Handling fan-in aggregation
- Good Answer: Use `asyncio.as_completed` to stream partial results; time-bound aggregation.
- Senior Trade-offs: Ordering differs; extra logic for completeness.

## 96) Protecting critical sections
- Good Answer: Use `asyncio.Lock` or optimistic concurrency with retries; minimize lock scope.
- Senior Trade-offs: Locks lower concurrency; optimistic retries may spin.

## 97) Observability of pools
- Good Answer: Export pool metrics (in-use, idle, waiters) for DB/HTTP/cache; alert on saturation.
- Senior Trade-offs: Extra instrumentation overhead.

## 98) Hot reload in dev
- Good Answer: Use `--reload` only locally; disable in staging/prod to avoid watcher overhead.
- Senior Trade-offs: Developer convenience vs performance.

## 99) Async safe cleanup on exceptions
- Good Answer: Use `try/finally` with awaited cleanup; ensure context managers cover all resources.
- Senior Trade-offs: Boilerplate; prevents leaks.

## 100) SLO-driven concurrency controls
- Good Answer: Set concurrency/timeout/rate limits to meet latency/error SLOs; continuously tune with load tests and prod telemetry.
- Senior Trade-offs: SLO goals drive trade-offs between cost, latency, and availability.

---

## Code Snippets

### Bounded gather utility
```python
import asyncio
from collections.abc import Iterable, Awaitable, Callable

async def bounded_gather(n: int, coros: Iterable[Callable[[], Awaitable]]):
    sem = asyncio.Semaphore(n)
    async def run(fn):
        async with sem:
            return await fn()
    return await asyncio.gather(*(run(c) for c in coros))
```

### TaskGroup with cancellation safety (Python 3.11+)
```python
import asyncio

async def fetch_one(i):
    await asyncio.sleep(0.1)
    return i

async def fetch_all(ids):
    results = []
    try:
        async with asyncio.TaskGroup() as tg:
            tasks = [tg.create_task(fetch_one(i)) for i in ids]
        for t in tasks:
            results.append(t.result())
    except* Exception as eg:
        # handle grouped exceptions
        raise
    return results
```

### Deadline propagation via contextvars
```python
import asyncio, contextvars, time

deadline_var = contextvars.ContextVar("deadline", default=None)

class Deadline:
    def __init__(self, ms: int):
        self.end = time.monotonic() + ms/1000
    def remaining(self):
        return max(0, self.end - time.monotonic())

async def with_deadline(ms: int):
    token = deadline_var.set(Deadline(ms))
    try:
        yield
    finally:
        deadline_var.reset(token)

async def call_downstream():
    d = deadline_var.get()
    timeout = d.remaining() if d else 1.0
    return await asyncio.wait_for(asyncio.sleep(0.05), timeout)
```

### Using to_thread for blocking calls
```python
import asyncio, hashlib

def cpu_heavy(data: bytes):
    for _ in range(1_000_000):
        hashlib.sha256(data).digest()
    return True

async def handler(data: bytes):
    return await asyncio.to_thread(cpu_heavy, data)
```

### Async HTTP client reuse with httpx
```python
import httpx

client: httpx.AsyncClient | None = None

async def startup():
    global client
    client = httpx.AsyncClient(timeout=5.0, limits=httpx.Limits(max_connections=100, max_keepalive_connections=20))

async def shutdown():
    await client.aclose()
```

---

## Quick Operational Checklist
- Event loop: Keep it non-blocking; offload CPU-bound work.
- Concurrency: Bound with semaphores; align pools with worker counts.
- Timeouts: Enforce deadlines per hop; propagate and budget.
- Backpressure: Use queues and shed load gracefully when saturated.
- Observability: Instrument pools, queue depths, timeouts, and cancellations.
- Resilience: Retries with idempotency, circuit breakers, and graceful shutdown.
