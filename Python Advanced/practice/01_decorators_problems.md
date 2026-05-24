# Decorators Practice Problems

These problems move from basic cross-cutting concerns to production-grade wrappers.

## Problem 1 - Audit Critical Actions

Scenario: Your finance team wants an audit trail whenever a staff-only function updates a payout, refund, or invoice.

Build a decorator that:

- accepts an event name such as `refund_approved`
- logs the actor id, target id, timestamp, and execution time
- records both success and failure outcomes
- preserves the wrapped function's metadata

## Problem 2 - Permission Guard for Internal Tools

Scenario: An internal admin portal exposes functions like `freeze_account(user_id)` and `issue_credit(user_id, amount)`.

Build a decorator that:

- checks whether the caller has one of the required roles
- supports multiple allowed roles
- raises a clear exception when access is denied
- works on both standalone functions and instance methods

## Problem 3 - Response Cache with Expiry

Scenario: A shipping dashboard repeatedly calls the same pricing function for identical carts and destinations.

Build a decorator that:

- caches results based on positional and keyword arguments
- expires entries after a configurable TTL
- exposes a method to clear the cache manually
- avoids returning stale data after the TTL has passed

## Problem 4 - Retry Unstable Vendor Calls

Scenario: Your order service calls a flaky courier API that fails intermittently with timeout and connection errors.

Build a decorator that:

- retries only for configured exception types
- uses exponential backoff with jitter
- logs each retry attempt with delay information
- re-raises the final exception after the last attempt

## Problem 5 - Tenant-Aware Rate Limiting

Scenario: A notification service sends SMS through a paid provider, and each tenant has a separate throughput cap.

Build a decorator that:

- rate limits calls per tenant instead of globally
- uses a sliding time window
- is thread-safe
- exposes metrics so the operations team can inspect current call counts per tenant
