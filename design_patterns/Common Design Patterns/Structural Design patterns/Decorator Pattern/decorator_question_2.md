# Decorator Pattern — Question 2 (Medium)

## Problem: API Request Handler with Stackable Middleware

Build a request processing system where middleware decorators add cross-cutting concerns (logging, auth, rate limiting, caching) to a base handler.

### Requirements

- `Handler(ABC)`: `handle(request: dict) -> dict`
- `BaseHandler`: processes the request and returns `{"status": 200, "body": "OK"}`
- Decorators:
  - `LoggingDecorator`: prints request/response, passes through
  - `AuthDecorator`: checks `request["token"]` == "valid-token", returns 401 if not
  - `RateLimitDecorator(max_calls, period_seconds)`: tracks calls, returns 429 if exceeded
  - `CacheDecorator`: caches responses by request URL, returns cached if available

### Expected Usage

```python
handler = BaseHandler()
handler = LoggingDecorator(handler)
handler = AuthDecorator(handler)
handler = RateLimitDecorator(handler, max_calls=3, period_seconds=60)
handler = CacheDecorator(handler)

# First call — goes through all layers
response = handler.handle({"url": "/api/data", "token": "valid-token"})
# [LOG] Request: /api/data
# → {"status": 200, "body": "OK"}

# Second identical call — served from cache
response = handler.handle({"url": "/api/data", "token": "valid-token"})
# [CACHE HIT] /api/data

# Bad auth
response = handler.handle({"url": "/api/data", "token": "wrong"})
# → {"status": 401, "body": "Unauthorized"}
```

### Constraints

- Order matters! Auth should run before rate-limiting (no point rate-limiting unauthenticated requests).
- `CacheDecorator` must store results in a dict keyed by URL.
- `RateLimitDecorator` tracks timestamps — use `time.time()`.

### Think About

- How does the order of wrapping affect behavior?
- How is this similar to middleware in FastAPI/Django?
