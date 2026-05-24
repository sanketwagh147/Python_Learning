# Descriptors Practice Problems

These problems show where descriptors are more precise than plain properties.

## Problem 1 - Positive Money Fields
Scenario: A billing object has `subtotal`, `tax`, and `shipping_cost` fields that must always be non-negative decimals.

Build a descriptor that:
- validates numeric input
- converts values to `Decimal`
- rejects negatives
- stores per-instance data safely

## Problem 2 - Normalized Contact Fields
Scenario: A CRM model stores customer emails and phone numbers but wants a single place to normalize and validate them.

Build a descriptor that:
- trims whitespace
- lowercases emails
- runs simple validation rules
- raises descriptive errors for bad values

## Problem 3 - Lazy Secret Lookup
Scenario: A service object needs an API key from a secret manager, but fetching it is expensive and should happen only when first accessed.

Build a descriptor that:
- fetches the value lazily on first access
- caches it per instance
- supports manual invalidation
- hides direct access to internal storage details

## Problem 4 - Unit-Aware Measurement Field
Scenario: A logistics model stores package weight internally in kilograms but users may set values in pounds or grams.

Build a descriptor that:
- normalizes input into kilograms
- exposes a way to read the value in different units
- rejects impossible values like negative weight
- keeps conversion logic out of the business methods

## Problem 5 - Permissioned Attribute Access with Audit
Scenario: A healthcare application stores sensitive patient notes and wants read/write access checked centrally.

Build a descriptor that:
- checks the current actor before get or set operations
- logs every successful or denied access attempt
- supports different permissions for reading and writing
- keeps the model API clean for the rest of the codebase