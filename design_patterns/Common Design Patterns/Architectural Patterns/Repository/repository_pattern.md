# Repository Pattern

The Repository Pattern abstracts data access behind an interface, decoupling business logic from the storage mechanism (database, API, file, cache).

## Key Concepts

- **Repository Interface**: An abstract class defining data access methods (CRUD).
- **Concrete Repository**: Implements the interface for a specific storage (Postgres, MongoDB, in-memory).
- **Client / Service**: Depends on the interface, never on the concrete implementation (DIP).

## Why Use It?

| Problem | Solution |
|---|---|
| Business logic is tightly coupled to SQL queries | Repository hides all query details behind methods like `find_by_id()` |
| Can't unit test without a real database | Swap in an `InMemoryRepository` for tests |
| Switching from Postgres to MongoDB means rewriting services | Only the concrete repository changes; services are untouched |

## Structure

```
Service (high-level)
   │
   ▼
Repository (abstraction / interface)
   │
   ├── PostgresRepository (concrete)
   ├── MongoRepository (concrete)
   └── InMemoryRepository (concrete — for tests)
```

## Example

```python
from abc import ABC, abstractmethod

class UserRepository(ABC):
    @abstractmethod
    def find_by_id(self, user_id: int) -> dict: ...

    @abstractmethod
    def save(self, user: dict) -> dict: ...

    @abstractmethod
    def delete(self, user_id: int) -> bool: ...


class PostgresUserRepository(UserRepository):
    def __init__(self, session):
        self._session = session

    def find_by_id(self, user_id: int) -> dict:
        row = self._session.execute("SELECT ...", {"id": user_id})
        return row

    def save(self, user: dict) -> dict:
        self._session.execute("INSERT ...", user)
        self._session.commit()
        return user

    def delete(self, user_id: int) -> bool:
        self._session.execute("DELETE ...", {"id": user_id})
        self._session.commit()
        return True


class InMemoryUserRepository(UserRepository):
    def __init__(self):
        self._store = {}

    def find_by_id(self, user_id: int) -> dict:
        return self._store.get(user_id, {})

    def save(self, user: dict) -> dict:
        self._store[user["id"]] = user
        return user

    def delete(self, user_id: int) -> bool:
        return self._store.pop(user_id, None) is not None


# Service depends on abstraction — not on Postgres or InMemory
class UserService:
    def __init__(self, repo: UserRepository):
        self._repo = repo

    def get_user(self, user_id: int) -> dict:
        return self._repo.find_by_id(user_id)
```

## Relationship to Other Patterns

- **Unit of Work** — often paired with Repository to group operations in a transaction
- **DIP (SOLID)** — Repository is the textbook example of Dependency Inversion
- **Factory** — can be used to create the correct Repository implementation

## When to Use

✅ You want to decouple business logic from data access  
✅ You need to swap storage backends (DB, cache, mock)  
✅ You want testable services without a real database  

## When NOT to Use

❌ Trivial CRUD apps where SQLAlchemy models are enough  
❌ One-off scripts that will never need a different data source
