# Dependency Inversion Principle — Question 3 (Hard)

## Problem: Implement a DI Container with Auto-Resolution

Build a lightweight Dependency Injection container that automatically resolves dependencies by inspecting constructor type hints.

### Requirements

#### DI Container
```python
class Container:
    def register(self, interface: type, implementation: type, singleton: bool = False): ...
    def register_instance(self, interface: type, instance: object): ...
    def resolve(self, interface: type) -> object: ...
```

#### Auto-Resolution
The container inspects `__init__` type hints to resolve dependencies recursively:

```python
class UserRepository(ABC): ...
class PostgresUserRepository(UserRepository): ...

class NotificationService(ABC): ...
class EmailNotificationService(NotificationService): ...

class UserService:
    def __init__(self, repo: UserRepository, notifier: NotificationService):
        self.repo = repo
        self.notifier = notifier

class UserController:
    def __init__(self, service: UserService):
        self.service = service
```

### Expected Usage

```python
container = Container()

# Register mappings
container.register(UserRepository, PostgresUserRepository)
container.register(NotificationService, EmailNotificationService, singleton=True)
container.register(UserService, UserService)
container.register(UserController, UserController)

# Auto-resolve entire dependency tree
controller = container.resolve(UserController)
# Container sees UserController needs UserService
# UserService needs UserRepository + NotificationService
# Resolves PostgresUserRepository and EmailNotificationService
# Assembles everything automatically!

assert isinstance(controller.service.repo, PostgresUserRepository)
assert isinstance(controller.service.notifier, EmailNotificationService)

# Singleton: same instance every time
notifier1 = container.resolve(NotificationService)
notifier2 = container.resolve(NotificationService)
assert notifier1 is notifier2  # Same object!
```

### Advanced Features

#### Scope Management
```python
with container.create_scope() as scope:
    # Scoped instances are shared within the scope, destroyed after
    service1 = scope.resolve(UserService)
    service2 = scope.resolve(UserService)
    assert service1 is service2  # same within scope
# scope ends — scoped instances are gone
```

#### Circular Dependency Detection
```python
class A:
    def __init__(self, b: "B"): ...
class B:
    def __init__(self, a: A): ...

container.register(A, A)
container.register(B, B)
container.resolve(A)  # → CircularDependencyError: A → B → A
```

### Constraints

- Use `typing.get_type_hints()` or `inspect.signature()` to read constructor params.
- Support: transient (new each time), singleton (one instance), scoped (one per scope).
- Detect circular dependencies and raise clear error with the dependency chain.
- `resolve()` is recursive — resolves the entire dependency graph.
- Handle cases where a param has no type hint or a default value.

### Think About

- How does this compare to Python DI frameworks like `dependency-injector` or `injector`?
- How does FastAPI's `Depends()` achieve DI?
- What are the trade-offs of auto-wiring vs explicit wiring?
- Why do some teams prefer explicit composition roots over containers?
