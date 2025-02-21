# Understanding Singleton with Metaclass

## What is a Metaclass?

A **metaclass** is a "class of a class"—it defines how a class itself is constructed.  
By defining `SingletonMeta` as a metaclass, we **control the instantiation behavior** of any class that uses it.

---

## ️⃣ Understanding the Code

### 🔹 `SingletonMeta` (Metaclass)

```python
class SingletonMeta(type):
    _instances = {}  # Stores the single instance of each class using this metaclass

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)  # Create instance if not exists
        return cls._instances[cls]  # Return the same instance every time
```

## ️⃣ Why Use a Metaclass for Singleton?

✅ **Cleaner & More Pythonic** than using decorators or `__new__`.  
✅ **Works for all subclasses** of `Singleton` automatically.  
✅ **Avoids overriding `__new__`** in each class, keeping instance creation centralized.  

---

## When to Use This Approach?

- **Database connections** (only one connection object).  
- **Configuration management** (shared settings instance).  
- **Thread pools** (reuse the same set of threads).  
- **Logging** (a single logging instance across the application).  

---

### Key Takeaways

- `SingletonMeta` **ensures only one instance** of a class exists.  
- `__call__()` in the metaclass **controls instance creation**.  
- Any class using `metaclass=SingletonMeta` **automatically becomes a Singleton**.  
- It’s **cleaner than using decorators or overriding `__new__`**.  
