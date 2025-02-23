# Decorator Pattern

Decorator is a structural design pattern that lets you attach new behaviors to objects by placing these objects inside special wrapper objects that contain the behaviors.  
It differs from inheritance because the new feature is added only to that particular
object, not to the entire subclass.

## Why Use the Decorator Pattern?

✅ Extends functionality without modifying the original class  
✅ Follows Open-Closed Principle (open for extension, closed for modification)  
✅ Avoids subclass explosion (too many subclasses for every variation)  

## How It Works

The pattern consists of:

1. Component (Base Interface/Abstract Class) → Defines the common interface.
2. Concrete Component → The main object that we want to extend.
3. Decorator (Base Decorator Class) → Wraps around the Concrete Component.
Concrete Decorators → Add new behaviors dynamically.

## Example ( using classes)

```python
from abc import ABC, abstractmethod

# Step 1: Component (Base Interface)
class Coffee(ABC):
    @abstractmethod
    def cost(self):
        pass
    
    @abstractmethod
    def description(self):
        pass

# Step 2: Concrete Component
class SimpleCoffee(Coffee):
    def cost(self):
        return 50  # Base price

    def description(self):
        return "Simple Coffee"

# Step 3: Base Decorator (Wraps Coffee)
class CoffeeDecorator(Coffee):
    def __init__(self, coffee: Coffee):
        self._coffee = coffee  # Composition (has-a relationship)

    def cost(self):
        return self._coffee.cost()

    def description(self):
        return self._coffee.description()

# Step 4: Concrete Decorators (Add extra features)
class Milk(CoffeeDecorator):
    def cost(self):
        return self._coffee.cost() + 10  # Add milk price

    def description(self):
        return self._coffee.description() + ", Milk"

class Sugar(CoffeeDecorator):
    def cost(self):
        return self._coffee.cost() + 5  # Add sugar price

    def description(self):
        return self._coffee.description() + ", Sugar"

class Caramel(CoffeeDecorator):
    def cost(self):
        return self._coffee.cost() + 20  # Add caramel price

    def description(self):
        return self._coffee.description() + ", Caramel"

# Step 5: Using Decorators
coffee = SimpleCoffee()
print(coffee.description(), "-> Cost:", coffee.cost())

coffee = Milk(coffee)  # Add milk
coffee = Sugar(coffee)  # Add sugar
coffee = Caramel(coffee)  # Add caramel

print(coffee.description(), "-> Cost:", coffee.cost())
```

## Example 2 (functional)

```python
import time
from functools import wraps
def timing(func):
    """Decorator to measure execution time."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"{func.__name__} took {end - start:.4f} seconds")
        return result
    return wrapper

@timing
def slow_function():
    time.sleep(2)
    return "Completed"

slow_function()
```

## Key Points

✅ Extends behavior dynamically  
✅ Uses function wrapping (@decorator) in Python  
✅ Avoids modifying the original function
