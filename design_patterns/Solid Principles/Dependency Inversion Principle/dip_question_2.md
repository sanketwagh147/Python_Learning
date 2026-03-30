# Dependency Inversion Principle — Question 2 (Medium)

## Problem: Multi-Layer Application with Proper Dependency Direction

Build a 3-layer application (Controller → Service → Repository) where ALL dependencies point toward abstractions, not implementations.

### The Violating Architecture

```
Controller → ConcreteService → ConcreteRepository → PostgresDB
```
Every layer depends directly on the layer below. Changing the DB requires changing the repository, service, and potentially the controller.

### Requirements

#### Abstractions (owned by the domain/service layer)
```python
class UserRepository(ABC):
    @abstractmethod
    def find_by_id(self, user_id: str) -> User | None: ...
    @abstractmethod
    def save(self, user: User) -> None: ...

class NotificationPort(ABC):
    @abstractmethod
    def send(self, to: str, message: str) -> None: ...

class UserService:
    """Depends on abstractions, not implementations."""
    def __init__(self, repo: UserRepository, notifier: NotificationPort): ...
```

#### Implementations (depend on abstractions)
```python
class PostgresUserRepository(UserRepository): ...
class InMemoryUserRepository(UserRepository): ...   # for testing
class EmailNotifier(NotificationPort): ...
class MockNotifier(NotificationPort): ...            # for testing
```

#### Wiring (composition root)
```python
def create_app(env: str):
    if env == "production":
        repo = PostgresUserRepository(db_conn)
        notifier = EmailNotifier(smtp)
    else:
        repo = InMemoryUserRepository()
        notifier = MockNotifier()
    
    service = UserService(repo, notifier)
    controller = UserController(service)
    return controller
```

### Expected Usage

```python
# Production
app = create_app("production")
app.handle_request({"action": "register", "name": "Alice", "email": "a@x.com"})

# Test — exact same code paths, but with fakes
app = create_app("test")
app.handle_request({"action": "register", "name": "Bob", "email": "b@x.com"})
```

### Constraints

- `UserService` imports ZERO concrete classes — only abstractions.
- Abstractions are defined in the service layer (not the infrastructure layer).
- The composition root (wiring) is the ONLY place that knows about concrete classes.
- Write tests for `UserService` using `InMemoryUserRepository` and `MockNotifier`.

### Think About

- Why should the abstraction be defined by the consumer (service) rather than the provider (repository)?
- How does this relate to Hexagonal Architecture (Ports and Adapters)?
- What is a "Composition Root" and why should it be at the application's entry point?
