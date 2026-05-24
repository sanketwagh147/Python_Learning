# Decorators Practice Solutions

## Solution 1 - Audit Critical Actions
Use a decorator factory and log inside `finally` so failures are captured too.

```python
import functools
import time


def audit(event_name, sink):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(actor_id, target_id, *args, **kwargs):
            started = time.perf_counter()
            status = "success"
            try:
                return func(actor_id, target_id, *args, **kwargs)
            except Exception:
                status = "failure"
                raise
            finally:
                sink.write(
                    {
                        "event": event_name,
                        "actor_id": actor_id,
                        "target_id": target_id,
                        "status": status,
                        "duration_ms": round((time.perf_counter() - started) * 1000, 2),
                    }
                )

        return wrapper

    return decorator
```

## Solution 2 - Permission Guard for Internal Tools
Accept an actor explicitly, or resolve it from `self.actor` for bound methods.

```python
import functools


def require_roles(*allowed_roles):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            actor = kwargs.get("actor")
            if actor is None and args and hasattr(args[0], "actor"):
                actor = args[0].actor
            if actor is None or actor.role not in allowed_roles:
                raise PermissionError(f"{func.__name__} requires one of {allowed_roles}")
            return func(*args, **kwargs)

        return wrapper

    return decorator
```

## Solution 3 - Response Cache with Expiry
Use argument tuples as cache keys and `time.monotonic()` for TTL checks.

```python
import functools
import time


def ttl_cache(ttl_seconds):
    def decorator(func):
        cache = {}

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            key = (args, tuple(sorted(kwargs.items())))
            now = time.monotonic()
            if key in cache:
                value, stored_at = cache[key]
                if now - stored_at < ttl_seconds:
                    return value
            value = func(*args, **kwargs)
            cache[key] = (value, now)
            return value

        wrapper.clear_cache = cache.clear
        return wrapper

    return decorator
```

## Solution 4 - Retry Unstable Vendor Calls
Retry only known transient failures and add jitter so many workers do not retry in lockstep.

```python
import functools
import random
import time


def retry(max_attempts, retry_for, base_delay=0.25):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except retry_for:
                    if attempt == max_attempts:
                        raise
                    delay = base_delay * (2 ** (attempt - 1)) + random.uniform(0, 0.1)
                    time.sleep(delay)

        return wrapper

    return decorator
```

## Solution 5 - Tenant-Aware Rate Limiting
Store timestamps per tenant and protect them with a lock.

```python
import functools
import threading
import time
from collections import defaultdict, deque


def tenant_rate_limit(max_calls, period_seconds):
    calls = defaultdict(deque)
    lock = threading.Lock()

    def decorator(func):
        @functools.wraps(func)
        def wrapper(tenant_id, *args, **kwargs):
            with lock:
                window = calls[tenant_id]
                now = time.monotonic()
                while window and window[0] <= now - period_seconds:
                    window.popleft()
                if len(window) >= max_calls:
                    raise RuntimeError(f"rate limit exceeded for {tenant_id}")
                window.append(now)
            return func(tenant_id, *args, **kwargs)

        wrapper.metrics = calls
        return wrapper

    return decorator
```