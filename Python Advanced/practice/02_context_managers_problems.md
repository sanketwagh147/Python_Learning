# Context Managers Practice Problems

These exercises focus on resource safety, rollback behavior, and multi-resource orchestration.

## Problem 1 - Temporary Environment Override
Scenario: A support engineer needs to run a script with temporary API and feature-flag settings without polluting the shell session.

Create a context manager that:
- temporarily sets environment variables
- restores original values on exit
- removes variables that did not exist before entering
- works correctly even if an exception occurs inside the block

## Problem 2 - Transaction Scope for Order Updates
Scenario: An order workflow updates inventory, writes a payment record, and marks the order as paid.

Create a context manager that:
- begins a transaction on entry
- commits on success
- rolls back on any exception
- exposes the database session to the caller

## Problem 3 - File Lock Around Monthly Reports
Scenario: Two scheduled jobs can generate the same monthly payout report, and duplicate files cause accounting issues.

Create a context manager that:
- acquires a file-based lock before generating the report
- times out if the lock cannot be acquired
- always releases the lock on exit
- writes a useful diagnostic message when contention happens

## Problem 4 - Reversible Feature-Flag Rollout
Scenario: Product managers want to enable a risky flag during a single import job and automatically restore the previous value afterward.

Create a context manager that:
- snapshots a mutable configuration object
- applies a temporary override set
- restores the original values even after failures
- tracks which flags actually changed for audit output

## Problem 5 - Coordinated Cleanup Across Services
Scenario: A migration job opens a DB transaction, a temp directory, and an outbound API session. If any step fails, every resource must be cleaned up safely.

Create a solution using a context manager or `ExitStack` that:
- acquires resources dynamically
- tears them down in reverse order
- keeps the control flow readable
- avoids resource leaks when only some resources were created