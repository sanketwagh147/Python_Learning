# Singleton Pattern — Question 1 (Easy)

## Problem: Application Configuration Manager

An app needs a single shared configuration object that's loaded once and accessed everywhere.

### Requirements

- `ConfigManager` is a singleton — only one instance ever exists.
- It loads settings from a dictionary (simulating a config file).
- `get(key)` returns a setting, `set(key, value)` updates it.
- Multiple calls to `ConfigManager()` return the same instance.

### Expected Usage

```python
config1 = ConfigManager()
config1.load({"debug": True, "db_host": "localhost", "db_port": 5432})

config2 = ConfigManager()
print(config2.get("db_host"))  # → "localhost"
print(config1 is config2)       # → True

config2.set("debug", False)
print(config1.get("debug"))     # → False (same instance!)
```

### Constraints

- Implement using `__new__` override.
- `load()` should only work once — subsequent calls are ignored (already loaded).

### Hints

```python
class ConfigManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
```
