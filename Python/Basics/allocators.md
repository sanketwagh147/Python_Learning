# `__new__` Method as an Allocator in Python

The `__new__` method in Python is often referred to as an **allocator** because it is responsible for **allocating memory** for a new instance of a class before `__init__` initializes it.

## Why is `__new__` Called an Allocator?

- It **creates and returns** a new instance of the class.  
- It is used for **customizing instance creation**, especially in **immutable types** (like `int`, `str`, `tuple`).  
- Unlike `__init__`, which **modifies an existing instance**, `__new__` ensures that the instance is **allocated first**.  

## Example: Customizing `__new__` for Immutable Objects

```python
class CustomInt(int):
    def __new__(cls, value):
        print("Allocating memory for CustomInt")
        return super().__new__(cls, value)

# Creating an instance
num = CustomInt(10)
print(num)  # Output: 10

```

## Key Differences Between `__new__` and `__init__`

| Feature       | `__new__`                                | `__init__`                      |
|--------------|----------------------------------------|--------------------------------|
| **Purpose**   | Allocates memory (acts as an allocator) | Initializes the instance       |
| **Return Value** | New instance of the class             | Always `None`                  |
| **When Called** | Before `__init__`                      | After `__new__`                |
| **Used In**   | Singleton, Metaclasses, Immutable Objects | General object initialization |
