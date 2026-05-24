# Dataclasses and slots Practice Problems

These exercises focus on cleaner data models, immutability, and memory-conscious objects.

## Problem 1 - Order Data Transfer Object

Scenario: An order service passes order records between pricing, shipping, and billing modules.

Build a dataclass that:

- models the essential fields cleanly
- provides sensible defaults for optional values
- exposes a computed property such as `total_items`
- remains easy to serialize later

## Problem 2 - Immutable Configuration Snapshot

Scenario: A deployment job should receive a frozen snapshot of runtime configuration so later mutations do not affect an in-progress release.

Build a dataclass that:

- is immutable
- stores release metadata and feature flags
- validates required values in `__post_init__`
- makes accidental mutation impossible

## Problem 3 - Derived Fields for Shipment Planning

Scenario: A warehouse app stores item dimensions and wants volume and dimensional weight calculated automatically.

Build a dataclass that:

- accepts raw dimensions and actual weight
- computes derived fields in `__post_init__`
- raises clear errors for invalid dimensions
- keeps calculation logic close to the data model

## Problem 4 - Memory-Efficient Telemetry Events

Scenario: An analytics agent creates millions of short-lived event objects per hour.

Build a slotted dataclass that:

- minimizes per-instance memory overhead
- still provides type hints and readable repr output
- models only the fields you truly need
- explains why `slots=True` helps here

## Problem 5 - Auditable Financial Records

Scenario: Accounting needs immutable ledger entries that can be ordered, hashed, and stored in sets or deduplicated streams.

Build a dataclass design that:

- supports equality and ordering semantics intentionally
- is safe to hash
- keeps money fields precise
- stays explicit about which fields participate in comparisons
