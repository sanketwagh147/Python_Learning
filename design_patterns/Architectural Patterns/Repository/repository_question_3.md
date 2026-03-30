# Repository Pattern — Question 3 (Hard)

## Problem: Unit of Work with Multiple Repositories

Build a Unit of Work that coordinates changes across multiple repositories and commits/rolls back as a single atomic transaction.

### Requirements

#### Unit of Work
```python
class UnitOfWork:
    users: UserRepository
    orders: OrderRepository
    products: ProductRepository
    
    def __enter__(self): ...
    def __exit__(self, exc_type, exc_val, exc_tb): ...
    def commit(self): ...
    def rollback(self): ...
```

#### Tracked Changes
```python
class TrackedRepository(Repository[T]):
    """Wraps a base repository and tracks all changes."""
    new: list[T]       # entities added
    dirty: list[T]     # entities modified
    removed: list[T]   # entities deleted
    
    def commit(self): ...   # flush all tracked changes to base
    def rollback(self): ... # discard all tracked changes
```

### Expected Usage

```python
with UnitOfWork() as uow:
    # Read
    user = uow.users.get_by_id("U1")
    product = uow.products.get_by_id("P1")
    
    # Modify
    user.balance -= product.price
    uow.users.update(user)
    
    product.stock -= 1
    uow.products.update(product)
    
    order = Order(user_id="U1", product_id="P1", amount=product.price)
    uow.orders.add(order)
    
    # All changes committed together
    uow.commit()

# If an exception occurs, everything rolls back
with UnitOfWork() as uow:
    uow.users.get_by_id("U1").balance -= 1000
    uow.products.get_by_id("P1").stock -= 1
    raise ValueError("Something went wrong")
    # __exit__ called → rollback → no changes persisted
```

### Constraints

- `TrackedRepository` wraps any `InMemoryRepository` and tracks changes without flushing until `commit()`.
- `rollback()` discards all tracked changes (new, dirty, removed become empty).
- `commit()` applies all changes atomically — if any operation fails, none are applied.
- The UoW acts as a context manager (`with` statement).
- Identity map: if the same entity is loaded twice, return the same object (not two copies).

### Think About

- How does SQLAlchemy's `Session` implement the Unit of Work pattern?
- What is the "identity map" and why is it important?
- How would this scale to a real database with actual transactions?
