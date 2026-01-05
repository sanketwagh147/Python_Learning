# 01. Core Python & Fundamentals

## 🧠 Data Structures & Algorithms (Simplified)
*Refresher with Python examples.*

### Key Concepts
- **Big O Notation Dictionary:**
  - **O(1)**: Constant time (Hash map lookup)
  - **O(n)**: Linear time (Looping through a list)
  - **O(log n)**: Logarithmic time (Binary search)
  - **O(n log n)**: Log-linear time (Fast sorting like Merge Sort)

### 1. Lists & Arrays
- **Concept:** Ordered collection of items. Lists in Python are dynamic arrays.
- **Complexity:** Access: O(1), Append: O(1), Insert/Delete: O(n).
```python
# List comprehension (Pythonic way to create lists)
squares = [x**2 for x in range(10)] 
```

### 2. Hash Tables (Dictionaries)
- **Concept:** Key-value pairs. Uses a hashing function to compute an index.
- **Complexity:** Average case O(1) for lookup, insert, delete.
- **Use Case:** Fast lookups, counting frequency.
```python
# Dictionary comprehension
char_count = {char: "hello".count(char) for char in "hello"}
# {'h': 1, 'e': 1, 'l': 2, 'o': 1}
```

### 3. Stacks & Queues
- **Stack (LIFO):** Last In, First Out. Use `list.append()` and `list.pop()`.
- **Queue (FIFO):** First In, First Out. Use `collections.deque` (faster than list for queues).
```python
from collections import deque
queue = deque(["a", "b", "c"])
queue.append("d")
queue.popleft() # Returns "a" - O(1) operation
```

### 4. Trees & Graphs (Simplified)
- **Tree:** Hierarchical structure. Root node with child nodes.
  - **BST (Binary Search Tree):** Left child < Parent < Right child.
- **Graph:** Nodes (vertices) connected by edges. Used for networks, maps.
  - **BFS (Breadth-First Search):** Explore layer by layer (Shortest path).
  - **DFS (Depth-First Search):** Explore as deep as possible (Mazes, puzzles).

---

## 🐍 Python 3 Internal Mechanic (Deep Dive)

### 1. The Global Interpreter Lock (GIL)
**Explainer:** The GIL is a mutex that protects access to Python objects, preventing multiple native threads from executing Python bytecodes at once.
- **Impact:** Python threads are great for **I/O bound** tasks (API calls, file reading) but bad for **CPU bound** tasks (number crunching).
- **Workaround:** Use `multiprocessing` for CPU-heavy tasks to bypass GIL.

### 2. Memory Management & Garbage Collection
**Reference Counting:**
- Every object includes a reference count. When it drops to 0, memory is freed immediately.
**Cycle Detector (Garbage Collector):**
- Handles reference cycles (A references B, B references A).
- Generational GC: Objects start in Generation 0. If they survive a collection, they move to Gen 1, then Gen 2.

### 3. Iterators and Generators
**Iterators:** Objects implementing `__iter__()` and `__next__()`.
**Generators:** Functions that use `yield`. They are lazy (compute values on the fly) and memory efficient.
```python
def infinite_sequence():
    num = 0
    while True:
        yield num
        num += 1

# Consumes negligible memory compared to a list
for i in infinite_sequence():
    if i > 5: break
    print(i)
```

### 4. Decorators
**Concept:** Higher-order functions that modify the behavior of other functions without changing their code.
**Use Cases:** Logging, Authentication, Timing, Caching.
```python
import functools

def debug(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        print(f"Calling {func.__name__} with args: {args}")
        result = func(*args, **kwargs)
        print(f"{func.__name__} returned: {result}")
        return result
    return wrapper

@debug
def add(x, y):
    return x + y
```

### 5. Context Managers (`with` statement)
**Mechanism:** Define `__enter__` and `__exit__`.
**Why:** Ensures resources (files, locks, DB interactions) are properly cleaned up even if exceptions occur.

### 6. `*args` and `**kwargs`
**Concept:** Capture a variable number of arguments.
- `*args`: Collects extra positional arguments as a tuple.
- `**kwargs`: Collects extra keyword arguments as a dictionary.
```python
def greet(*names, **options):
    greeting = options.get("greeting", "Hello")
    for name in names:
        print(f"{greeting}, {name}!")

greet("Alice", "Bob", greeting="Hi")  # Hi, Alice! Hi, Bob!
```
**Use Case:** Writing wrapper functions, decorators, and flexible APIs.

### 7. Exception Handling Best Practices
- **Catch Specific Exceptions:** `except ValueError:` not `except Exception:`.
- **Use `else` clause:** Code that runs if NO exception occurred.
- **Use `finally` clause:** Cleanup code that ALWAYS runs.
- **Custom Exceptions:** Create classes inheriting from `Exception`.
```python
class InsufficientFundsError(Exception):
    pass

def withdraw(balance, amount):
    if amount > balance:
        raise InsufficientFundsError(f"Cannot withdraw {amount}")
    return balance - amount
```

---

## 🏗️ Object-Oriented Programming (Deep Dive)

### 1. Metaclasses
**Concept:** "Classes of classes". They define how a class behaves. A class is an instance of a metaclass.
- **Default:** `type` is the default metaclass.
- **Usage:** Validating class attributes at creation time, automatically registering classes (e.g., for plugins).

### 2. MRO (Method Resolution Order)
**Rule:** Python uses the **C3 Linearization** algorithm.
- Determines the order in which base classes are searched when executing a method.
- **Check MRO:** `ClassName.mro()` or `ClassName.__mro__`.
- **Key:** In multiple inheritance, it ensures consistency and that no class is visited twice.

### 3. Abstract Base Classes (ABC)
**Concept:** Define an interface that subclasses must implement.
```python
from abc import ABC, abstractmethod

class PaymentProcessor(ABC):
    @abstractmethod
    def process_payment(self, amount: float) -> bool:
        pass

class StripeProcessor(PaymentProcessor):
    def process_payment(self, amount: float) -> bool:
        # Stripe-specific logic
        return True
```
**Why:** Enforces a contract. `PaymentProcessor()` raises `TypeError` if instantiated directly.

### 4. Composition vs Inheritance
- **Inheritance ("is-a"):** `Dog` is an `Animal`. Tight coupling.
- **Composition ("has-a"):** `Car` has an `Engine`. Loose coupling. Preferred!
```python
# Composition - Engine is injected
class Engine:
    def start(self): print("Engine started")

class Car:
    def __init__(self, engine: Engine):
        self.engine = engine
    def start(self):
        self.engine.start()
```
**Rule of thumb:** Favor composition over inheritance.

### 5. Design Patterns (Common in Python)

#### Singleton
Ensures a class has only one instance.
```python
class Singleton:
    _instance = None
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
```

#### Factory
Creates objects without exposing the instantiation logic.
```python
def get_serializer(format: str):
    if format == "json":
        return JsonSerializer()
    elif format == "xml":
        return XmlSerializer()
```

#### Strategy
Define a family of algorithms, encapsulate each, and make them interchangeable.
```python
class CompressionStrategy(ABC):
    @abstractmethod
    def compress(self, data): pass

class ZipCompression(CompressionStrategy):
    def compress(self, data): return zip_it(data)
```

#### Decorator (Pattern, not Python syntax)
Wraps an object to add behavior.
```python
class LoggingDecorator:
    def __init__(self, component):
        self._component = component
    def operation(self):
        print("Logging before...")
        self._component.operation()
```

### 6. SOLID Principles in Python
- **S (Single Responsibility):** A class should have one reason to change.
- **O (Open/Closed):** Open for extension, closed for modification. (Use inheritance/strategies).
- **L (Liskov Substitution):** Subtypes must be substitutable for their base types.
- **I (Interface Segregation):** Clients shouldn't depend on interfaces they don't use.
- **D (Dependency Inversion):** Depend on abstractions, not concretions.

---

## ❓ Interview Questions & Answers

**Q1: What is the difference between `__str__` and `__repr__`?**
> **A:** `__str__` is for end-users (readable), while `__repr__` is for developers (unambiguous representation). Ideally, `eval(repr(obj)) == obj`.

**Q2: How does `dict` lookup work internally?**
> **A:** It calculates the hash of the key (`hash(key)`). This hash determines the index in the internal array. If a collision occurs (two keys hash to the same slot), Python handles it (classically open addressing/probing, modern implementations are optimized).

**Q3: Explain the `walrus` operator (`:=`).**
> **A:** Introduced in Python 3.8, it assigns values to variables as part of a larger expression.
> `if (n := len(data)) > 10: print(f"List is too long: {n}")`

**Q4: What are the differences between `@staticmethod` and `@classmethod`?**
> **A:** `@classmethod` takes `cls` as first argument and can access class state. `@staticmethod` takes neither `self` nor `cls` and behaves like a regular function belonging to the class namespace.

---

## 🔗 Recommended Resources

- **Resource:** [Real Python: Python Memory Management](https://realpython.com/python-memory-management/)
- **Resource:** [Python MRO documentation](https://www.python.org/download/releases/2.3/mro/)
- **Forum:** [r/Python on Reddit - Daily Discussions](https://www.reddit.com/r/Python/)
