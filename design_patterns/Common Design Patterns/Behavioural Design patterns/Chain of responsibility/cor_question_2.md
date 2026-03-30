# Chain of Responsibility — Question 2 (Medium)

## Problem: Middleware Pipeline for Web Request Validation

Build a request validation chain for a REST API. Each middleware validates one aspect and either passes the request along or rejects it.

### Requirements

- `Middleware(ABC)`: `handle(request: dict) -> dict` (returns response)
- Chain order:
  1. **IPWhitelistMiddleware**: rejects if `request["ip"]` not in allowed list
  2. **AuthMiddleware**: rejects if `"Authorization"` header missing or invalid token
  3. **RateLimitMiddleware**: tracks requests per IP, rejects if > 100/min
  4. **InputSanitizationMiddleware**: strips HTML tags from body fields
  5. **RouteHandler**: the actual endpoint logic (final handler)

### Expected Usage

```python
handler = build_middleware_chain(
    allowed_ips=["192.168.1.0/24", "10.0.0.0/8"],
    valid_tokens=["token-abc", "token-xyz"],
    rate_limit=100,
)

# Pass all checks
response = handler.handle({
    "ip": "192.168.1.50",
    "headers": {"Authorization": "Bearer token-abc"},
    "method": "POST",
    "path": "/api/users",
    "body": {"name": "Alice <script>alert('xss')</script>"}
})
# → {"status": 200, "body": {"name": "Alice"}}  # HTML stripped!

# Fail at auth
response = handler.handle({
    "ip": "192.168.1.50",
    "headers": {},
    "method": "GET",
    "path": "/api/users",
})
# → {"status": 401, "body": "Missing Authorization header"}
```

### Constraints

- Each middleware is independent — removing one shouldn't break others.
- The sanitization middleware must handle nested dicts recursively.
- Rate limiter must track per-IP (use a dict with timestamps).

### Think About

- How is this different from Pipeline pattern? (CoR can halt early; Pipeline always runs all stages.)
- How does FastAPI/Django middleware work compared to this?
