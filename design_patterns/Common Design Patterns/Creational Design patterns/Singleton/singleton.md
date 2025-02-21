# Singleton Design Pattern

The **Singleton Design Pattern** is a **creational pattern** that ensures a class has only **one instance** and provides a **global access point** to it. It is commonly used when exactly one object is needed to coordinate actions across a system.

## Key Features of Singleton Pattern

- **Single Instance:** Ensures that only one instance of the class exists.  
- **Global Access Point:** The instance is accessible throughout the application.  
<!-- TODO REVIEW below point-->
- **Lazy Initialization (optional):** The instance is created only when first accessed.  

## When to Use Singleton?

- Logging  
- Database connections  
- Configuration management  
- Thread pools  
- Caching  

## [Implementation in python](singleton.py)

```python
class singleton:
    # private class attribute to hold the instance
    _instance = none  

    def __new__(cls, *args, **kwargs):
        if cls._instance is none:  # check if instance exists
            cls._instance = super().__new__(cls)
        return cls._instance  # return the single instance

# usage
obj1 = singleton()
obj2 = singleton()
print(obj1 is obj2)  # output: true (both variables point to the same instance)

```

### Implementation using decorator

```python
def singleton(cls):
    instances = {}

    def get_instance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]

    return get_instance

@singleton
class SingletonClass:
    pass

obj1 = SingletonClass()
obj2 = SingletonClass()

print(obj1 is obj2)  # Output: True
```

### Implementation using Metaclass

```python
class SingletonMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]

class Singleton(metaclass=SingletonMeta):
    pass

obj1 = Singleton()
obj2 = Singleton()

print(obj1 is obj2)  # Output: True
```

## ✅ Advantages

- **Saves memory** by preventing multiple instances.
- **Centralized control** over an instance.
- **Useful for shared resources**, such as database connections, logging, caching, and configuration management.
- **Lazy initialization (optional)** can delay instance creation until needed, improving performance.
- **Thread safety** (if implemented correctly) ensures that multiple threads don’t create duplicate instances.

## ❌ Disadvantages

- **Introduces global state**, making debugging and testing harder.
- **Increases tight coupling**, making the code less flexible and harder to modify.
- **Difficult to subclass or extend**, as enforcing a single instance can restrict inheritance.
- **Concurrency issues** can arise if the singleton is not implemented with proper thread safety.
- **Hidden dependencies** make it harder to track where the instance is used.

### 🔹 When to Use Singleton?

- **Logging** (single logger instance throughout the app).
- **Database connections** (reuse the same connection instead of opening new ones).
- **Configuration management** (load settings once and reuse them).
- **Thread pools** (manage a fixed number of worker threads).
- **Caching systems** (store frequently accessed data).

### 🔹 When to Avoid Singleton?

- When you need a **scalable and flexible design**.
- When multiple instances **don't harm performance or logic**.
- When **unit testing** is a priority (singletons make mocking harder).
