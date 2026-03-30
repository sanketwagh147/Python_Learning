# Memento Pattern — Question 3 (Hard)

## Problem: Database Transaction Rollback System

Build a transaction system for an in-memory database that supports `BEGIN`, `COMMIT`, `ROLLBACK`, and **nested transactions** (savepoints).

### Requirements

#### Database (Originator)
```python
class InMemoryDB:
    def begin(self) -> None: ...       # start transaction (push savepoint)
    def commit(self) -> None: ...      # commit current transaction level
    def rollback(self) -> None: ...    # rollback to last savepoint
    def set(self, key: str, value: Any) -> None: ...
    def get(self, key: str) -> Any: ...
    def delete(self, key: str) -> None: ...
```

#### Nested Transactions

```python
db = InMemoryDB()
db.set("a", 1)

db.begin()          # Transaction 1
db.set("a", 2)
db.set("b", 10)

db.begin()          # Transaction 2 (nested)
db.set("a", 3)
db.delete("b")

print(db.get("a"))  # → 3
print(db.get("b"))  # → KeyError (deleted)

db.rollback()       # Rollback Transaction 2
print(db.get("a"))  # → 2 (back to Transaction 1 state)
print(db.get("b"))  # → 10 (restored!)

db.commit()         # Commit Transaction 1
print(db.get("a"))  # → 2
print(db.get("b"))  # → 10

db.rollback()       # No active transaction → raise TransactionError
```

### Constraints

- Each `begin()` pushes a snapshot (memento) onto a stack.
- `rollback()` restores the last snapshot. `commit()` discards it (makes changes permanent at that level).
- Mementos must deep-copy the entire data store.
- Operations outside a transaction are immediately permanent (no rollback).
- `rollback()` or `commit()` without an active transaction raises `TransactionError`.
- Must support arbitrary nesting depth.

### Bonus

Add a `history()` method that returns a log of all operations:
```python
db.history()
# → [("SET", "a", 1), ("BEGIN",), ("SET", "a", 2), ("SET", "b", 10),
#    ("BEGIN",), ("SET", "a", 3), ("DELETE", "b"), ("ROLLBACK",), ("COMMIT",)]
```

### Think About

- How does this compare to PostgreSQL's `SAVEPOINT` mechanism?
- What's the memory cost of snapshotting the entire DB on each `begin()`?
- Could you optimize by storing only the **diff** (changed keys) instead of full snapshots?
