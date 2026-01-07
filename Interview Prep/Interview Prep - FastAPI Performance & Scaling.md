# FastAPI Performance & Scaling — 100 Scenario-Based Interview Questions

Each scenario includes a Good Answer and a Senior-Level trade-off explanation. Code examples are included where useful.

## Purpose & How To Use
- Interview flow: Identify bottleneck (CPU vs IO), ensure async purity, align worker counts with downstream pools, then add caching and resilience.
- Evaluate along four axes: correctness, event-loop friendliness (no blocking), production readiness (health, shutdown, canaries), and SLO thinking.
- Drill prompts: “What breaks under PgBouncer transaction pooling?”, “How do we avoid retry storms?”, “Where should compression happen?”
## What Senior Engineers (4-5 YOE) Should Demonstrate
1. **System Design**: Architect services for horizontal scaling; understand when to split vs keep monolithic; design for failure modes.
2. **Performance Engineering**: Profile before optimizing; quantify improvements with metrics; understand the full request lifecycle.
3. **Production Operations**: Design deployment strategies (blue-green, canary); implement circuit breakers and graceful degradation; plan capacity.
4. **Code Quality Leadership**: Establish patterns for the team; review PRs for performance anti-patterns; document architectural decisions.
5. **Incident Response**: Debug production issues methodically; communicate status; write actionable post-mortems.

## Architecture Decision Framework
When facing performance/scaling decisions, senior engineers should consider:

```
┌─────────────────────────────────────────────────────────────────┐
│                    Decision Framework                           │
├─────────────────────────────────────────────────────────────────┤
│ 1. MEASURE: What's the actual bottleneck? (CPU/IO/Memory/Net)   │
│ 2. QUANTIFY: What's the SLO? What's the current state?          │
│ 3. OPTIONS: List 2-3 approaches with trade-offs                 │
│ 4. DECIDE: Pick based on effort vs impact vs reversibility      │
│ 5. VALIDATE: How will we know it worked? Rollback plan?         │
└─────────────────────────────────────────────────────────────────┘
```
## Key Concepts Primer
- ASGI runtime: `uvicorn[standard]` (uvloop/httptools) for speed; gunicorn for pre-fork control and graceful rolling restarts.
- Event loop hygiene: Avoid blocking code in handlers; offload CPU to process pool, sync IO to threadpool.
- Pools & backpressure: DB/HTTP/cache pools must be bounded and aligned with worker count; introduce queuing and 503s on saturation.
- Validation/serialization: Pydantic v2 is faster; prefer `ORJSONResponse` for JSON; avoid double validation.
- Caching: Response caching (ETag/Last-Modified), Redis with TTL/versioning, in-process LRU for hot small items.
- Observability: Prometheus metrics, trace sampling (OTel), structured logs, and meaningful health/readiness signals.

## Mini Case Study: P99 Spikes After Feature Launch
Symptoms: P99 from 250ms→1.2s, CPU moderate, DB fine; threads at capacity.
Approach: Replace per-request `httpx` client with lifespan-scoped client, swap to `ORJSONResponse`, cap concurrency to downstream, and add route-level cache.

```python
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
import httpx

client: httpx.AsyncClient | None = None

async def startup():
    global client
    client = httpx.AsyncClient(timeout=5.0, limits=httpx.Limits(max_connections=200, max_keepalive_connections=50))

async def shutdown():
    await client.aclose()

app = FastAPI(default_response_class=ORJSONResponse, on_startup=[startup], on_shutdown=[shutdown])
```

## Production Debugging Playbook

### Scenario: Latency Spike During Peak Traffic

**Step 1: Triage (2 min)**
```bash
# Check if it's app or downstream
curl -w "@curl-format.txt" -o /dev/null -s https://your-service/health

# curl-format.txt:
#     time_namelookup:  %{time_namelookup}s\n
#     time_connect:     %{time_connect}s\n
#     time_appconnect:  %{time_appconnect}s\n
#     time_starttransfer: %{time_starttransfer}s\n
#     time_total:       %{time_total}s\n
```

**Step 2: Check Resource Saturation**
```python
# Add this endpoint for debugging (remove in prod or protect with auth)
@app.get("/debug/pools")
async def debug_pools():
    return {
        "db_pool": {
            "size": db_pool.size,
            "free": db_pool.freesize,
            "used": db_pool.size - db_pool.freesize,
        },
        "http_client": {
            "connections_in_pool": len(client._transport._pool._connections),
        },
        "active_tasks": len(asyncio.all_tasks()),
    }
```

**Step 3: Profile Hot Paths**
```python
import time
from functools import wraps

def profile_async(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = await func(*args, **kwargs)
        duration = time.perf_counter() - start
        if duration > 0.1:  # Log slow calls
            logger.warning(f"{func.__name__} took {duration:.3f}s")
        return result
    return wrapper
```

**Step 4: Common Culprits Checklist**
- [ ] DB pool exhausted (check `pg_stat_activity`)
- [ ] HTTP client not reused (socket exhaustion)
- [ ] Blocking call in async handler (check with `py-spy`)
- [ ] Missing index on new query pattern
- [ ] Cache miss storm (check Redis hit rate)
- [ ] Downstream service degraded (check circuit breaker state)

### Metrics Every Senior Engineer Should Track
```python
from prometheus_client import Counter, Histogram, Gauge

# Request metrics
REQUEST_LATENCY = Histogram(
    'http_request_duration_seconds',
    'Request latency',
    ['method', 'endpoint', 'status'],
    buckets=[.01, .025, .05, .1, .25, .5, 1, 2.5, 5, 10]
)

# Pool metrics
DB_POOL_SIZE = Gauge('db_pool_connections', 'DB pool size', ['state'])
HTTP_CLIENT_CONNECTIONS = Gauge('http_client_connections', 'HTTP client pool')

# Business metrics
REQUESTS_BY_TENANT = Counter('requests_by_tenant', 'Requests per tenant', ['tenant_id'])
```

## Common Pitfalls
- Creating DB/HTTP clients per request; causes socket and GC pressure.
- Too many workers vs DB pool size, leading to saturation and timeouts.
- Heavy logic in middleware or docs enabled in prod increasing latency/attack surface.
- Missing deadlines and retries, causing tail latency and user-visible hangs.

## Evaluation Rubric (Interview)

### Junior (1-2 YOE)
- Writes working async endpoints
- Understands basic request/response flow
- Can use ORM for simple queries

### Mid-Level (3-4 YOE)
- No blocking in hot paths; correct use of thread/process pools
- Understands connection pooling and basic caching
- Can debug simple performance issues with profiling

### Senior (4-5 YOE) — Target Level
- **Async correctness**: Identifies blocking code in code review; designs for concurrency safety
- **Capacity math**: Calculates worker/pool sizing based on load; predicts scaling needs
- **Reliability**: Implements comprehensive timeout/retry/circuit-breaker strategies; designs graceful degradation
- **Operations**: Sets up observability; plans zero-downtime deployments; writes runbooks
- **Leadership**: Establishes team patterns; mentors on performance; drives architectural decisions

### Staff+ (6+ YOE)
- Designs multi-service architectures for scale and reliability
- Establishes organization-wide API standards and patterns
- Drives platform-level improvements (service mesh, observability infrastructure)

---

## 1) Sudden P99 latency spike after release
- Good Answer: Profile endpoints with sampling (OpenTelemetry/ASGI middleware), check dependency changes (validation, serialization), ensure DB connection pool saturation isn’t occurring, and verify uvicorn worker count.
- Senior Trade-offs: Adding telemetry impacts latency but yields insight. More workers increase CPU and memory; balance with DB pool and cache limits.

## 2) Choosing ASGI server/runtime
- Good Answer: Use `uvicorn[standard]` (uvloop + httptools) in prod; for multiprocess, run via gunicorn with `uvicorn.workers.UvicornWorker`.
- Senior Trade-offs: Pure uvicorn is simpler; gunicorn adds pre-fork resilience and rolling restarts at the cost of extra memory.

## 3) Optimal worker model for CPU vs IO workloads
- Good Answer: IO-bound: more uvicorn workers with async endpoints. CPU-bound: offload to process pool or a job queue; don’t block the event loop.
- Senior Trade-offs: Too many workers contending for CPU hurts cache locality; process pools add IPC overhead.

## 4) Pydantic v1 vs v2 validation overhead
- Good Answer: Prefer Pydantic v2 for speed; avoid heavy custom validators in hot paths; consider `response_model=None` for internal endpoints.
- Senior Trade-offs: Disabling validation increases risk; selectively relax on internal trusted flows.

## 5) JSON serialization performance
- Good Answer: Use `ORJSONResponse` or `orjson` for faster dumps; pre-serialize large payloads.
- Senior Trade-offs: orjson is fast but strict; ensure types are serializable and stable across versions.

```python
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
app = FastAPI(default_response_class=ORJSONResponse)
```

## 6) Connection pool saturation to PostgreSQL
- Good Answer: Use async drivers (`asyncpg` or SQLAlchemy 2.0 async engine), cap pool size per process, and align with DB/PgBouncer limits.
- Senior Trade-offs: Oversized pools cause thrashing and timeouts; undersized pools underutilize CPU.

## 7) Blocking code inside async endpoint
- Good Answer: Wrap blocking work with `run_in_threadpool()` or move to background tasks/queue.
- Senior Trade-offs: Threadpools add context switching; use sparingly.

```python
from starlette.concurrency import run_in_threadpool

@app.get("/hash")
async def hash_data():
    return await run_in_threadpool(cpu_heavy_hash)
```

## 8) Choosing gzip vs brotli
- Good Answer: Use gzip for broad compatibility; enable brotli behind a proxy/CDN for better compression.
- Senior Trade-offs: Brotli offers smaller sizes at higher CPU cost; offload to edge if possible.

## 9) Docs overhead in production
- Good Answer: Disable Swagger/Redoc in prod or protect behind auth; generate OpenAPI offline.
- Senior Trade-offs: Docs are convenient but add routes and memory.

## 10) Rate limiting strategy
- Good Answer: Apply token-bucket using Redis; per-tenant/per-IP keys; use middleware for uniform enforcement.
- Senior Trade-offs: Centralized limits create single point of failure; ensure Redis HA.

## 11) Caching layer selection
- Good Answer: Use Redis for request/response or computed results caching with TTL and cache keys; apply ETag/Last-Modified for idempotent GETs.
- Senior Trade-offs: Stale cache risk; build invalidation on writes.

## 12) Idempotency for POST
- Good Answer: Idempotency keys stored in Redis/DB to guard retries under timeouts.
- Senior Trade-offs: Storage overhead; ensure TTL and conflict resolution policy.

## 13) Streaming large responses
- Good Answer: Use `StreamingResponse` to stream files/chunks; avoid loading into memory.
- Senior Trade-offs: Backpressure handling and client disconnects complicate flow.

## 14) Handling large file uploads
- Good Answer: Stream to disk/S3 using chunked uploads; set size limits; validate MIME type early.
- Senior Trade-offs: Streaming reduces memory footprint but increases complexity and temp storage needs.

## 15) HTTP client reuse
- Good Answer: Use a single `httpx.AsyncClient` per process with keep-alive; create in `lifespan` or startup event.
- Senior Trade-offs: Long-lived clients need DNS refresh and timeout tuning.

```python
from contextlib import asynccontextmanager
import httpx

client: httpx.AsyncClient | None = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    global client
    client = httpx.AsyncClient(timeout=5.0)
    yield
    await client.aclose()

app = FastAPI(lifespan=lifespan)
```

## 16) Observability stack
- Good Answer: Add Prometheus metrics, OpenTelemetry tracing, and structured JSON logs; track latency, error rate, concurrency, and pool stats.
- Senior Trade-offs: Over-instrumentation adds overhead; sample wisely and aggregate centrally.

## 17) ASGI middleware cost
- Good Answer: Limit number/order of middleware; keep them lightweight and stateless; avoid heavy DB calls inside middleware.
- Senior Trade-offs: Middleware centralizes cross-cutting concerns but can stack latency.

## 18) Dependency injection overhead
- Good Answer: Prefer `Depends` that are fast/pure; avoid DB/session creation per request; reuse sessions via factories.
- Senior Trade-offs: DI improves testability but can hide expensive work.

## 19) BackgroundTask vs task queues
- Good Answer: Use FastAPI `BackgroundTasks` for small, fire-and-forget tasks; use Celery/RQ/Dramatiq for retries, scheduling, and durability.
- Senior Trade-offs: BackgroundTasks die on worker crash; queues add ops overhead.

## 20) Graceful shutdown under load
- Good Answer: Enable gunicorn `--graceful-timeout`, add healthcheck flip to drain traffic, and close pools on lifespan shutdown.
- Senior Trade-offs: Longer drain times delay deploys; too short risks request loss.

## 21) Gunicorn worker count
- Good Answer: Start with workers ~= cores for async workloads (e.g., `2-4 x cores` total across pods), tune via load tests.
- Senior Trade-offs: Too many workers starve memory/DB; too few underutilize CPU.

## 22) Uvicorn reload in dev
- Good Answer: Disable reload in prod; it adds file watchers and overhead.
- Senior Trade-offs: Convenience vs performance.

## 23) TLS termination
- Good Answer: Terminate TLS at reverse proxy (Nginx/Envoy) and keep internal HTTP; enable HTTP/2 at the edge.
- Senior Trade-offs: Offloading reduces app CPU but adds network hops.

## 24) CDN for static/content
- Good Answer: Serve static files from CDN/object storage; avoid app-level file serving.
- Senior Trade-offs: Requires cache invalidation and versioning.

## 25) Response compression at proxy
- Good Answer: Let Nginx/Envoy handle gzip/brotli with proper MIME filters.
- Senior Trade-offs: Offloads CPU but adds proxy complexity.

## 26) Fast pagination
- Good Answer: Use keyset pagination; avoid deep `OFFSET`.
- Senior Trade-offs: Requires stable sort keys; client-side complexity.

## 27) ORM selection and overhead
- Good Answer: SQLAlchemy Core/2.0 ORM with async engine; avoid N+1 via eager loading/query design.
- Senior Trade-offs: ORMs speed dev but add overhead; for hot paths, use direct SQL/asyncpg.

## 28) Validation on internal services
- Good Answer: Reduce heavy model validation for internal trusted services; keep strict validation at edges.
- Senior Trade-offs: Faster internal calls but risk of propagation of bad data.

## 29) Redis vs in-process cache
- Good Answer: Use in-process LRU for small, hot data; Redis for shared cache across replicas.
- Senior Trade-offs: In-process is fast but not shared; eviction behavior matters.

## 30) ETag/Last-Modified
- Good Answer: Support conditional GET with `ETag` and `If-None-Match` to save bandwidth.
- Senior Trade-offs: Requires consistent hashing of responses; care with personalization.

## 31) Handling head-of-line blocking
- Good Answer: Keep handlers non-blocking; apply timeouts to outbound calls; prefer concurrent awaits where independent.
- Senior Trade-offs: Concurrency increases complexity and potential race conditions.

## 32) Batch outbound requests
- Good Answer: Batch/read-through caches to limit downstream QPS; use bulk endpoints.
- Senior Trade-offs: Larger payloads and N+1 on failures; implement partial successes.

## 33) Circuit breakers and timeouts
- Good Answer: Use `pybreaker` or custom with failure thresholds; set client timeouts and fallbacks.
- Senior Trade-offs: Prevents cascades but may fail closed; tune carefully.

## 34) Retry policies
- Good Answer: Exponential backoff + jitter for transient errors; idempotent only.
- Senior Trade-offs: Retries increase load during incidents; cap attempts and add deadlines.

## 35) Route-level caching
- Good Answer: Cache pure GET endpoints via middleware or decorator with key derivation from path/query/user.
- Senior Trade-offs: Memory growth and invalidation complexity.

## 36) Hot path micro-optimizations
- Good Answer: Avoid per-request object allocations; reuse compiled regex; pre-parse configs.
- Senior Trade-offs: Premature optimization vs measurable benefit.

## 37) JSON vs MessagePack
- Good Answer: For internal RPC, consider MessagePack to reduce payload size/CPU.
- Senior Trade-offs: Requires client support; observability tooling less mature.

## 38) WebSocket scale
- Good Answer: Use dedicated WS pods/worker class; sticky sessions or shared Redis pub/sub; limit per-connection memory.
- Senior Trade-offs: WS complicates scaling and load balancing; consider SSE when feasible.

## 39) SSE for server push
- Good Answer: Use SSE for one-way streams with `text/event-stream`; simpler than WS for broadcast.
- Senior Trade-offs: SSE is HTTP/1.1 friendly but limited vs WS.

## 40) Multipart forms performance
- Good Answer: Stream parse; set `max_request_size`; avoid copying buffers.
- Senior Trade-offs: Complexity and temp storage cleanup.

## 41) Handling slow clients
- Good Answer: Apply send/receive timeouts; proxy buffering where possible.
- Senior Trade-offs: Timeouts risk client-visible errors; set SLA-aligned values.

## 42) Startup initialization
- Good Answer: Lazy-init expensive dependencies; move heavy tasks out of startup.
- Senior Trade-offs: First-request latency vs faster pod starts.

## 43) Measuring cold starts
- Good Answer: Add boot metrics; warm pods before traffic; pre-jit modules if relevant.
- Senior Trade-offs: Warming costs resources.

## 44) Path operation function structure
- Good Answer: Keep handlers thin; push logic to services for reuse and testability.
- Senior Trade-offs: More indirection but easier to optimize hotspots.

## 45) Dependency scopes
- Good Answer: Use application-scoped singletons for clients/pools; request-scoped for per-request context.
- Senior Trade-offs: Singletons risk state leaks if misused.

## 46) Template rendering performance
- Good Answer: Cache templates and partials; offload rendering to CDN when possible.
- Senior Trade-offs: Less dynamic flexibility.

## 47) Content negotiation
- Good Answer: Default to JSON; avoid unnecessary format conversions.
- Senior Trade-offs: Supporting many formats increases code paths and test matrix.

## 48) 413 Payload Too Large handling
- Good Answer: Reject early at proxy; return useful error; document limits.
- Senior Trade-offs: Strict limits block edge cases; provide chunked upload alternative.

## 49) Memory leak debugging
- Good Answer: Use `tracemalloc`, heapprof, and load tests; check global caches, unclosed clients.
- Senior Trade-offs: Profiling can perturb performance; test in staging.

## 50) Starlette vs FastAPI overhead
- Good Answer: For minimal overhead, Starlette-only for micro endpoints; FastAPI’s validation/docs add weight but productivity.
- Senior Trade-offs: Maintainability vs micro-optimizing framework.

## 51) Sync endpoints in async app
- Good Answer: Acceptable for light CPU, but wrap heavy sync in threadpool.
- Senior Trade-offs: Too many sync handlers block threads; watch threadpool size.

## 52) Garbage collection tuning
- Good Answer: Tune Python GC thresholds for request-heavy workloads; consider `gc.disable()` in hot sections cautiously.
- Senior Trade-offs: Disabling GC risks memory growth; measure carefully.

## 53) Using uvloop
- Good Answer: Ensure `uvicorn[standard]` which includes uvloop; verify event loop policy at startup.
- Senior Trade-offs: uvloop is faster, but watch compatibility with some libs.

## 54) Pre-fork vs threads
- Good Answer: Pre-fork workers isolate GIL; threads share memory and GIL; for CPU-bound, prefer multiprocess.
- Senior Trade-offs: Processes cost memory; threads risk contention.

## 55) Response models and exclude_unset
- Good Answer: Use `exclude_unset=True` to reduce payload size; define lean response models.
- Senior Trade-offs: Clients may rely on explicit fields; coordinate contracts.

## 56) 429 handling and backoff hints
- Good Answer: Include `Retry-After` and document client behavior.
- Senior Trade-offs: Encourages well-behaved clients but can be ignored.

## 57) Idempotent retries at proxy
- Good Answer: Allow retry for GET/HEAD/PUT/DELETE; require idempotency key for POST.
- Senior Trade-offs: Proxies may retry unexpectedly; ensure safe server logic.

## 58) Slow downstream services
- Good Answer: Add hedged requests with timeout+cancel; cache positive results.
- Senior Trade-offs: Doubles load; use sparingly.

## 59) Backpressure
- Good Answer: Queue requests internally with limits; return 503 when saturated; expose queue depth metric.
- Senior Trade-offs: Dropping traffic protects health but affects availability.

## 60) Timeouts matrix
- Good Answer: Configure server, proxy, and client timeouts coherently; set deadlines per endpoint.
- Senior Trade-offs: Too aggressive timeouts hurt UX; too lax ties resources.

## 61) Health checks
- Good Answer: Liveness: process up; Readiness: dependencies ok; Startup: initial warmup complete.
- Senior Trade-offs: Overly strict readiness can cause flapping.

## 62) DB transactions per request
- Good Answer: Keep transactions short; avoid long-held connections; use per-request sessions with context manager.
- Senior Trade-offs: Frequent session create/destroy overhead; reuse pools.

## 63) ORM lazy loading
- Good Answer: Disable or control lazy loading; prefer explicit eager options.
- Senior Trade-offs: Lazy loads cause N+1; eager loads can over-fetch.

## 64) Multi-tenant throttling
- Good Answer: Per-tenant rate limits and quotas; backpressure on noisy neighbors.
- Senior Trade-offs: Complexity in keying and fairness.

## 65) API gateway caching
- Good Answer: Cache GET responses at gateway with TTL + Vary headers.
- Senior Trade-offs: Stale data risk; version carefully.

## 66) Canary releases
- Good Answer: Route small % traffic to canary; compare SLOs; auto-rollback.
- Senior Trade-offs: Requires routing control and telemetry.

## 67) Async file IO
- Good Answer: Use aiofiles for local disk; stream results.
- Senior Trade-offs: File systems may still block; monitor.

## 68) Security impacts on performance
- Good Answer: Cache JWT key sets (JWKS), reuse decoders; use short-lived caches for auth results.
- Senior Trade-offs: Caching auth risks stale revocations; set low TTL.

## 69) CORS overhead
- Good Answer: Restrict origins and headers; avoid wildcard; preflight caching via `Access-Control-Max-Age`.
- Senior Trade-offs: Strict CORS improves security but complicates clients.

## 70) Request parsing cost
- Good Answer: Limit body size, parse JSON once, avoid double validation.
- Senior Trade-offs: Strict limits may reject valid large requests.

## 71) Schema migration with zero downtime
- Good Answer: Backward-compatible changes, dual-write/read, then switch; avoid blocking migrations.
- Senior Trade-offs: More code paths temporarily; requires cleanup.

## 72) HOT paths and profiling
- Good Answer: Use `py-spy`, `scalene`, or `yappi` under load tests; measure before/after.
- Senior Trade-offs: Profilers add overhead; rely on sampling in prod.

## 73) A/B testing features
- Good Answer: Feature flags with low overhead; avoid per-request database checks.
- Senior Trade-offs: Increases complexity of code paths.

## 74) Data compression on responses
- Good Answer: Compress only over threshold (e.g., >1KB) and compressible types.
- Senior Trade-offs: Small payloads get slower with compression.

## 75) Large JSON payloads
- Good Answer: Paginate, filter fields, or switch to streaming.
- Senior Trade-offs: More round trips; ensure client can handle.

## 76) Fast startup for serverless
- Good Answer: Minimize imports at module scope; lazy-init; pre-build wheels; avoid heavy global models.
- Senior Trade-offs: Increases runtime latency for first use.

## 77) Serverless concurrency
- Good Answer: Keep functions stateless; use external caches/DB; avoid global connection reuse across ephemeral instances.
- Senior Trade-offs: Cold start and provider limits dominate performance.

## 78) Pre-computing expensive results
- Good Answer: Materialize aggregates periodically; invalidate on writes.
- Senior Trade-offs: Freshness vs latency.

## 79) Threadpool size tuning
- Good Answer: Tune `anyio`/Starlette threadpool for blocking tasks; monitor queue length.
- Senior Trade-offs: Too small blocks; too large thrashes.

## 80) Async DB drivers maturity
- Good Answer: Prefer battle-tested (asyncpg, sqlalchemy[asyncio]); avoid mixing sync/async DB access.
- Senior Trade-offs: Async drivers need careful transaction handling and connection lifetimes.

## 81) Prepared statements and PgBouncer
- Good Answer: With transaction pooling, prefer server-side prepared statements disabled or use `PgBouncer` 1.20+ `server_reset_query_always=0` and prepared statement spoofing features.
- Senior Trade-offs: Prepared statements improve latency but may break with transaction pooling; test.

## 82) Preventing 502s on deploy
- Good Answer: Use rolling deploys, readiness gates, and connection draining; keep N-1 healthy before killing old pods.
- Senior Trade-offs: Longer deploys vs zero-downtime.

## 83) Limiting response models for nested data
- Good Answer: Project fields at SQL level; return lean DTOs.
- Senior Trade-offs: More query code but less CPU/IO.

## 84) Handling spikes (flash sales)
- Good Answer: Queue writes, cache reads, use token buckets, pre-warm autoscaling.
- Senior Trade-offs: Increased complexity; consistency windows.

## 85) Autoscaling signals
- Good Answer: Scale on CPU, concurrency, queue depth, and latency SLO breaches.
- Senior Trade-offs: Wrong signals cause oscillations; use dampening.

## 86) Aggregating logs
- Good Answer: Structured logs (JSON) with request IDs; centralize in ELK/Loki.
- Senior Trade-offs: Logging volume costs; sample non-errors.

## 87) Latency budgets per hop
- Good Answer: Set per-hop budgets (auth, DB, cache, downstream) to meet P95.
- Senior Trade-offs: Strict budgets require tight enforcement.

## 88) Cross-cutting retry storms
- Good Answer: Global jittered backoff and max-inflight caps.
- Senior Trade-offs: Complex coordination; necessary to avoid meltdowns.

## 89) Safe request body parsing
- Good Answer: Use streaming parsers for very large JSON (or offload to batch ingestion); avoid building giant dicts.
- Senior Trade-offs: Streaming complicates validation and error handling.

## 90) Pre-aggregated auth context
- Good Answer: Compute authz context once in middleware and attach to `request.state`.
- Senior Trade-offs: Increases request state coupling.

## 91) API gateway versus service mesh
- Good Answer: Gateway for north-south (auth, routing, caching); mesh for east-west (mTLS, retries, telemetry).
- Senior Trade-offs: Mesh adds sidecar overhead and complexity.

## 92) Binary payloads
- Good Answer: Use `application/octet-stream` and stream; avoid base64 in JSON.
- Senior Trade-offs: Simpler JSON has overhead; binary is efficient but less debuggable.

## 93) Batching writes
- Good Answer: Accept batches in endpoint and DB `INSERT ... VALUES` or COPY; validate limits.
- Senior Trade-offs: Larger transactions hold locks; apply chunking.

## 94) Pre-warming caches
- Good Answer: Warm Redis/CDN after deploy; use backfill jobs.
- Senior Trade-offs: Risk warming stale content; coordinate invalidation.

## 95) Error handling cost
- Good Answer: Centralize exception handlers; avoid expensive formatting; return concise payloads.
- Senior Trade-offs: Less verbose errors hinder debugging for clients; provide correlation IDs.

## 96) Response headers bloat
- Good Answer: Keep headers minimal; avoid per-request debug headers in prod.
- Senior Trade-offs: Extra bytes add up; use feature flags for diagnostics.

## 97) Python version upgrades
- Good Answer: Use modern Python (3.11/3.12) for perf; validate C-ext compatibility.
- Senior Trade-offs: Upgrades need testing; perf gains can be substantial.

## 98) Using C extensions
- Good Answer: For heavy compute, use NumPy/Cython/Rust extensions; call from async via thread/process pool.
- Senior Trade-offs: Build complexity vs performance.

## 99) Partial responses
- Good Answer: Support sparse fieldsets (`fields=a,b`); compute only requested fields.
- Senior Trade-offs: API complexity; great for large resources.

## 100) SLO-driven engineering
- Good Answer: Define and monitor SLOs (availability, latency, error rates); prioritize work via error budgets.
- Senior Trade-offs: SLO focus aligns effort but requires discipline and tooling.

---

## Code Snippets

### Gunicorn + Uvicorn worker
```bash
gunicorn app.main:app \
  -k uvicorn.workers.UvicornWorker \
  --workers 4 --worker-connections 1000 \
  --graceful-timeout 30 --timeout 60 --log-level info
```

### Redis-backed rate limiter (sketch)
```python
import aioredis
from starlette.middleware.base import BaseHTTPMiddleware

class RateLimitMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, redis: aioredis.Redis, limit: int, window: int):
        super().__init__(app)
        self.redis = redis
        self.limit = limit
        self.window = window

    async def dispatch(self, request, call_next):
        key = f"rl:{request.client.host}:{request.url.path}"
        pipe = self.redis.pipeline()
        pipe.incr(key)
        pipe.expire(key, self.window)
        count, _ = await pipe.execute()
        if count and int(count) > self.limit:
            return JSONResponse({"detail": "rate limit"}, status_code=429)
        return await call_next(request)
```

### Async SQLAlchemy engine
```python
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
engine = create_async_engine("postgresql+asyncpg://...", pool_size=10, max_overflow=20)
AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False)
```

### ORJSON response and caching decorator (sketch)
```python
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from functools import lru_cache

app = FastAPI(default_response_class=ORJSONResponse)

@lru_cache(maxsize=1024)
def heavy_calc(key: str):
    ...

@app.get("/compute")
async def compute(key: str):
    return heavy_calc(key)
```

---

## Quick Operational Checklist
- Capacity: Align uvicorn workers, DB pool, and Redis connections.
- Async purity: No blocking calls in hot paths; use thread/process pool where needed.
- Caching: Redis for shared, LRU for local; define TTL and invalidation.
- Observability: Traces + metrics + logs with sampling and budgets.
- Resilience: Timeouts, retries, circuit breakers, and backpressure.
- Deploys: Graceful shutdown, canaries, and health checks.
