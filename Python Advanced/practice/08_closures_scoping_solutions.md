# Closures and Scoping Practice Solutions

## Solution 1 - Discount Rule Factory

Closures are a clean way to capture stable pricing rules.

```python
def make_discount_calculator(percent, minimum_total):
    rate = percent / 100

    def calculate(cart_total):
        if cart_total < minimum_total:
            return cart_total
        return round(cart_total * (1 - rate), 2)

    return calculate
```

## Solution 2 - Log Redaction Builder

Capture the sensitive key set once and return a pure transformation function.

```python
def build_redactor(sensitive_keys, replacement="***"):
    protected = set(sensitive_keys)

    def redact(payload):
        return {key: (replacement if key in protected else value) for key, value in payload.items()}

    return redact
```

## Solution 3 - Stateful Alert Counter

`nonlocal` keeps the state private without reaching for globals.

```python
def build_alert_counter(threshold):
    failures = 0

    def update(success):
        nonlocal failures
        failures = 0 if success else failures + 1
        if failures >= threshold:
            return {"severity": "high", "consecutive_failures": failures}
        return None

    return update
```

## Solution 4 - Retry Policy Builder

The factory captures config once and returns a wrapper tuned for that integration.

```python
import time


def make_retry_wrapper(max_attempts, delay_seconds):
    def wrap(func):
        def call(*args, **kwargs):
            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except Exception:
                    if attempt == max_attempts:
                        raise
                    time.sleep(delay_seconds * attempt)

        return call

    return wrap
```

## Solution 5 - Tenant Router Without Late Binding Bugs

Bind the loop variable immediately with a default argument.

```python
def build_tenant_handlers(tenants):
    handlers = {}
    for tenant in tenants:
        handlers[tenant["id"]] = lambda payload, tenant=tenant: {
            "tenant_id": tenant["id"],
            "route": tenant["route"],
            "payload": payload,
        }
    return handlers
```
