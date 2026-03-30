# Repository Pattern — Question 1 (Easy)

## Problem: In-Memory User Repository

Abstract data access for a `User` entity with a clean interface, backed by an in-memory store.

### Requirements

```python
class UserRepository(ABC):
    def add(self, user: User) -> None: ...
    def get_by_id(self, user_id: str) -> User: ...
    def get_all(self) -> list[User]: ...
    def update(self, user: User) -> None: ...
    def delete(self, user_id: str) -> None: ...

class InMemoryUserRepository(UserRepository):
    """Stores users in a dictionary."""
```

### Expected Usage

```python
repo = InMemoryUserRepository()

repo.add(User(id="1", name="Alice", email="alice@example.com"))
repo.add(User(id="2", name="Bob", email="bob@example.com"))

user = repo.get_by_id("1")
print(user.name)  # → "Alice"

user.name = "Alice Smith"
repo.update(user)

all_users = repo.get_all()
print(len(all_users))  # → 2

repo.delete("2")
print(len(repo.get_all()))  # → 1
```

### Constraints

- `get_by_id` raises `UserNotFoundError` if not found.
- `User` is a dataclass: `id`, `name`, `email`.
- The repository hides ALL storage details — callers don't know it's a dictionary.
