# CQRS Pattern — Question 3 (Hard)

## Problem: CQRS + Event Sourcing with Replay and Snapshots

Build a full CQRS system with event sourcing: the write side stores events (not state), and the read side is rebuilt by replaying events. Add snapshot support for performance.

### Requirements

#### Event Store
```python
class EventStore:
    def append(self, aggregate_id: str, event: DomainEvent, expected_version: int): ...
    def get_events(self, aggregate_id: str, after_version: int = 0) -> list[DomainEvent]: ...
    def get_all_events(self) -> list[DomainEvent]: ...  # for rebuilding projections
```

#### Aggregate (Write Side)
```python
class BankAccount:
    """Event-sourced aggregate — no direct state mutation."""
    
    def deposit(self, amount): ...   # emits AccountCreditedEvent
    def withdraw(self, amount): ...  # emits AccountDebitedEvent
    def transfer(self, target_id, amount): ... # emits TransferInitiatedEvent
    
    # Reconstitute from events
    @classmethod
    def from_events(cls, events: list[DomainEvent]) -> "BankAccount": ...
    
    def _apply(self, event: DomainEvent): ...  # updates in-memory state
```

#### Events
```python
class AccountOpenedEvent: account_id, owner, initial_balance, timestamp
class AccountCreditedEvent: account_id, amount, timestamp
class AccountDebitedEvent: account_id, amount, timestamp
class TransferInitiatedEvent: from_id, to_id, amount, timestamp
```

#### Read Side (Projections)
```python
class AccountBalanceProjection:
    """Maintains current balance view by replaying events."""
    def handle(self, event: DomainEvent): ...
    def get_balance(self, account_id: str) -> float: ...

class TransactionHistoryProjection:
    """Maintains a list of all transactions per account."""
    def handle(self, event: DomainEvent): ...
    def get_history(self, account_id: str) -> list[Transaction]: ...
```

#### Snapshots
```python
class SnapshotStore:
    def save(self, aggregate_id: str, snapshot: dict, version: int): ...
    def load(self, aggregate_id: str) -> tuple[dict, int] | None: ...
```

### Expected Usage

```python
# Open accounts via commands
cmd_handler.handle(OpenAccountCommand("ACC-1", "Alice", 1000))
cmd_handler.handle(OpenAccountCommand("ACC-2", "Bob", 500))

# Deposit & withdraw
cmd_handler.handle(DepositCommand("ACC-1", 200))
cmd_handler.handle(WithdrawCommand("ACC-1", 50))
cmd_handler.handle(TransferCommand("ACC-1", "ACC-2", 100))

# Query read model
print(balance_projection.get_balance("ACC-1"))  # → 1050
print(balance_projection.get_balance("ACC-2"))  # → 600

history = history_projection.get_history("ACC-1")
# → [Opened(1000), Credit(200), Debit(50), Transfer(-100 to ACC-2)]

# Rebuild from scratch
new_projection = AccountBalanceProjection()
for event in event_store.get_all_events():
    new_projection.handle(event)
# Produces identical state as original projection!

# Snapshot: after 100 events, save a snapshot
snapshot_store.save("ACC-1", {"balance": 1050, "owner": "Alice"}, version=4)
# Next load: restore from snapshot + replay events after version 4 only
```

### Constraints

- The write side NEVER stores state directly — only appends events.
- `expected_version` in `append()` provides optimistic concurrency control.
- Projections can be rebuilt from scratch by replaying ALL events.
- Snapshots: every N events, save aggregate state. On reload, start from snapshot + replay newer events.
- `TransferCommand` must debit source AND credit target atomically (both events in one batch).

### Think About

- What happens if the projection crashes mid-replay? How do you handle idempotency?
- Why is optimistic concurrency (`expected_version`) important in event sourcing?
- How does this compare to traditional CRUD? What are the storage trade-offs?
- Real systems: how do Axon, EventStoreDB, or Kafka implement this?
