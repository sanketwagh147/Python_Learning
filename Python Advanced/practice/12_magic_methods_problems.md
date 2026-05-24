# Magic Methods Practice Problems

These problems focus on domain objects that feel natural to use because they implement the right dunder methods.

## Problem 1 - Money Value Object
Scenario: A billing system needs a `Money` object that behaves safely in arithmetic.

Build a class that:
- supports addition and subtraction for matching currencies
- compares values correctly
- has a readable string representation
- refuses to combine mismatched currencies silently

## Problem 2 - Inventory Batch Container
Scenario: A warehouse app wants an `InventoryBatch` object that feels like a small collection.

Build a class that:
- implements truthiness based on whether stock remains
- supports `len()` and `in`
- returns a useful developer-facing `repr`
- keeps the API intuitive for day-to-day use

## Problem 3 - Time Window Membership
Scenario: A scheduling service repeatedly checks whether timestamps fall inside support windows and maintenance windows.

Build a class that:
- supports `timestamp in window`
- provides a clean text representation
- optionally supports iteration over boundary markers
- handles overnight windows correctly

## Problem 4 - Query Filter Composition
Scenario: An internal reporting tool wants business analysts to compose filters with natural syntax.

Build a class that:
- overloads `&` and `|` to combine filters
- keeps combinations immutable
- can render itself into a SQL-like or API filter expression
- makes debugging easier through `repr`

## Problem 5 - Weighted Scorecard Object
Scenario: A risk engine evaluates many signals and wants scorecards to combine, compare, and normalize cleanly.

Build a class that:
- implements arithmetic where it makes sense
- defines ordering intentionally
- supports iteration over named components
- avoids surprising behavior for unsupported operations