# Closures and Scoping Practice Problems

These exercises focus on state capture, configuration factories, and avoiding scoping bugs.

## Problem 1 - Discount Rule Factory

Scenario: A commerce team wants reusable discount calculators for seasonal promotions without hard-coding values all over the codebase.

Build a closure that:

- captures a discount percentage and minimum cart total
- returns a calculator function
- applies the discount only when the threshold is met
- keeps configuration immutable from the caller's perspective

## Problem 2 - Log Redaction Builder

Scenario: Different services need custom redaction rules for logs based on their own sensitive field lists.

Build a closure that:

- captures a set of sensitive keys
- returns a function that redacts matching fields in a payload dict
- supports custom replacement text
- does not mutate the original payload

## Problem 3 - Stateful Alert Counter

Scenario: Operations wants a lightweight way to count repeated failures before sending an escalation alert.

Build a closure that:

- tracks how many consecutive failures have occurred
- resets on success
- emits an alert payload only after a configured threshold
- uses `nonlocal` correctly instead of global state

## Problem 4 - Retry Policy Builder

Scenario: Different integrations use different timeout, retry, and backoff settings, and you want a small factory instead of repeated logic.

Build a closure-based factory that:

- captures retry configuration once
- returns a wrapper function for outbound calls
- tracks attempt counts for observability
- avoids late-binding bugs when factories are created inside loops

## Problem 5 - Tenant Router Without Late Binding Bugs

Scenario: A SaaS platform builds per-tenant callback functions dynamically, but previous attempts routed all traffic to the last tenant created in the loop.

Build a solution that:

- returns one callback per tenant
- ensures each callback keeps the correct tenant id and routing rules
- supports optional per-tenant feature flags
- makes the scoping behavior obvious to future readers
