# Singleton Pattern — Question 3 (Hard)

## Problem: Plugin Manager with Monostate (Borg) + Testability

A plugin system needs global state (registered plugins) shared across all instances, BUT must be testable (resettable between tests).

### Requirements

#### Part A: Borg Pattern (Shared State)

Instead of enforcing one instance, use the **Borg/Monostate** pattern — every instance shares the same `__dict__`.

```python
class PluginManager:
    _shared_state = {}

    def __new__(cls):
        obj = super().__new__(cls)
        obj.__dict__ = cls._shared_state
        return obj
```

- `register(name, plugin_cls)` — registers a plugin class.
- `get(name) -> Plugin` — instantiates and returns a plugin.
- `list_plugins() -> list[str]` — returns registered plugin names.

#### Part B: Plugin Interface

```python
class Plugin(ABC):
    @abstractmethod
    def execute(self, data: dict) -> dict: ...

class LoggingPlugin(Plugin): ...      # Adds a "logged_at" timestamp
class ValidationPlugin(Plugin): ...   # Raises if required keys missing
class TransformPlugin(Plugin): ...    # Uppercases all string values
```

#### Part C: Testability

Add a `reset()` **class method** that clears all shared state — designed for use in test teardown.

```python
# In test
def test_register_plugin():
    PluginManager.reset()
    pm = PluginManager()
    pm.register("logger", LoggingPlugin)
    assert "logger" in pm.list_plugins()
```

#### Part D: Compare Approaches

Write the same `PluginManager` using THREE different singleton techniques:
1. **Borg** (shared `__dict__`)
2. **`__new__` override** (classic singleton)
3. **Metaclass** (`SingletonMeta`)

### Expected Usage

```python
pm1 = PluginManager()
pm1.register("logger", LoggingPlugin)
pm1.register("validator", ValidationPlugin)

pm2 = PluginManager()
print(pm2.list_plugins())  # ["logger", "validator"]

result = pm2.get("logger").execute({"user": "Alice"})
print(result)  # {"user": "Alice", "logged_at": "2024-01-15T10:30:00"}
```

### Constraints

- Demonstrate that Borg allows multiple instances (different `id()`) but shared state.
- Classic singleton has same `id()`.
- All three versions must pass the same test suite.
- `reset()` must work correctly for each approach.

### Think About

- When would you prefer Borg over classic Singleton?
- Why is Singleton considered an **anti-pattern** in many codebases?
- How would you replace Singleton with **dependency injection** instead?
