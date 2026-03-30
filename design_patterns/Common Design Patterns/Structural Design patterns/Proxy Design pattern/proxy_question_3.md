# Proxy Pattern — Question 3 (Hard)

## Problem: Virtual Proxy + Remote Proxy for Microservice Client

Build a proxy that acts as a local stand-in for a remote microservice. It handles caching, connection retry, circuit breaking, and transparent fallback.

### Requirements

#### Remote Service Interface
```python
class ProductService(ABC):
    def get_product(self, product_id: str) -> dict: ...
    def search(self, query: str, limit: int = 10) -> list[dict]: ...
    def update_stock(self, product_id: str, quantity: int) -> bool: ...
```

#### Real Remote Client
```python
class RemoteProductService(ProductService):
    """Makes actual HTTP calls (simulated with random failures)."""
    def __init__(self, base_url: str): ...
```

#### Smart Proxy
```python
class SmartProductProxy(ProductService):
    def __init__(self, remote: RemoteProductService, cache_ttl: int = 60): ...
```

The proxy must:
1. **Cache** — GET operations (`get_product`, `search`) are cached with TTL. Write operations (`update_stock`) invalidate cache.
2. **Retry** — On connection error, retry up to 3 times with exponential backoff.
3. **Circuit Breaker** — After 5 consecutive failures, stop calling remote for 30 seconds (return cached data if available, otherwise raise).
4. **Fallback** — If the circuit is open and cached data exists, serve stale cache with a warning.

### Expected Usage

```python
remote = RemoteProductService("http://products-api:8080")
proxy = SmartProductProxy(remote, cache_ttl=120)

# Normal flow
product = proxy.get_product("P001")  # calls remote, caches result
product = proxy.get_product("P001")  # served from cache

# Remote goes down
# ... after 5 failures ...
product = proxy.get_product("P001")  # circuit OPEN, serves stale cache
# → WARNING: Serving stale data (circuit breaker open)

product = proxy.get_product("P999")  # not in cache, circuit open
# → ServiceUnavailableError: Circuit breaker open, no cached data for P999

# After 30 seconds, circuit half-opens
product = proxy.get_product("P001")  # tries remote once (half-open)
# If succeeds → circuit closes, normal operation resumes
```

### Constraints

- Implement all three proxy types in one class (Virtual + Remote + Protection proxy).
- Cache must handle TTL expiry and stale-while-revalidate.
- Circuit breaker states: CLOSED → OPEN → HALF_OPEN → CLOSED.
- Use `time.monotonic()` for timing (not `time.time()`).
- Thread-safe: cache and circuit breaker must work correctly with concurrent access.

### Think About

- This combines Proxy + Circuit Breaker + Cache-Aside patterns. Where does Proxy end and the others begin?
- How does this compare to libraries like `tenacity` (retry) and `pybreaker` (circuit breaker)?
- In production, would you implement this yourself or use a service mesh (Istio/Envoy)?
