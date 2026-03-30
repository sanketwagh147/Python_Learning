# Repository Pattern — Question 2 (Medium)

## Problem: Generic Repository with Query Specification

Build a generic repository that works with any entity type and supports flexible querying via the Specification pattern.

### Requirements

#### Generic Repository
```python
class Repository(ABC, Generic[T]):
    def add(self, entity: T) -> None: ...
    def get_by_id(self, entity_id: str) -> T: ...
    def find(self, spec: Specification[T]) -> list[T]: ...
    def find_one(self, spec: Specification[T]) -> T | None: ...
    def update(self, entity: T) -> None: ...
    def delete(self, entity_id: str) -> None: ...
    def count(self, spec: Specification[T] | None = None) -> int: ...
```

#### Specification
```python
class Specification(ABC, Generic[T]):
    def is_satisfied_by(self, entity: T) -> bool: ...
    def __and__(self, other): return AndSpec(self, other)
    def __or__(self, other): return OrSpec(self, other)
    def __invert__(self): return NotSpec(self)
```

#### Concrete Specs
```python
class AgeGreaterThan(Specification[User]): ...
class NameContains(Specification[User]): ...
class IsActive(Specification[User]): ...
```

### Expected Usage

```python
repo: Repository[User] = InMemoryRepository()
# ... add users ...

# Find active users over 30 whose name contains "A"
spec = IsActive() & AgeGreaterThan(30) & NameContains("A")
results = repo.find(spec)

# Find inactive OR young users
spec2 = ~IsActive() | AgeGreaterThan(50)
results2 = repo.find(spec2)

count = repo.count(IsActive())
```

### Constraints

- The same `InMemoryRepository` class works for any entity type.
- Specifications are composable with `&`, `|`, `~` operators.
- Entities must have an `id` attribute.
- `find()` with no spec returns all entities.

### Think About

- How does this compare to Django's `QuerySet.filter()` or SQLAlchemy's `session.query().filter()`?
- What if you wanted to sort or paginate results?
