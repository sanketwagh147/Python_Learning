# Open Close Principle

## Software entities (such as classes, modules, and functions) should be open for extension but closed for modification

- **Open for extension** → You should be able to add new functionality without modifying existing code.

- **Closed for modification** → Once a class/module is written and tested, you shouldn’t need to change it to introduce new behavior.

## Example 1 ( Violates OCP)

```python
class AreaCalculator:
    def calculate_area(self, shape):
        if isinstance(shape, Rectangle):
            return shape.width * shape.height
        elif isinstance(shape, Circle):
            return 3.14 * shape.radius * shape.radius

```

### Problems

Every time a new shape is added we have to update calculate area function making class harder to test adn maintain

### Solution

```python
from abc import ABC, abstractmethod

class Shape(ABC):
    @abstractmethod
    def area(self):
        pass

class Rectangle(Shape):
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def area(self):
        return self.width * self.height

class Circle(Shape):
    def __init__(self, radius):
        self.radius = radius

    def area(self):
        return 3.14 * self.radius * self.radius

class AreaCalculator:
    def calculate_area(self, shape: Shape):
        return shape.area()

```

### Benefit of this approach

- If we want to add new shapes for ex a triangle or hexagon , we can just create a new class (open for extension )without modifying existing Area calculator thus it remains unchanged (closed for modification)

## Example 2 ( Violates OCP)

```python
class PaymentProcessor:
    def process_payment(self, payment_method, amount):
        if payment_method == "credit_card":
            print(f"Processing credit card payment of ${amount}")
        elif payment_method == "paypal":
            print(f"Processing PayPal payment of ${amount}")
        else:
            raise ValueError("Unsupported payment method")

```

### Problems

Every time we need to add a payment support we need to modify the Payment Processor thus increasing the risk of breaking it

### Solution

```python
from abc import ABC, abstractmethod

class PaymentMethod(ABC):
    @abstractmethod
    def pay(self, amount):
        pass

class CreditCardPayment(PaymentMethod):
    def pay(self, amount):
        print(f"Processing credit card payment of ${amount}")

class PayPalPayment(PaymentMethod):
    def pay(self, amount):
        print(f"Processing PayPal payment of ${amount}")

class GooglePayPayment(PaymentMethod):
    def pay(self, amount):
        print(f"Processing GPay payment of ${amount}")

class PaymentProcessor:
    def process_payment(self, payment_method: PaymentMethod, amount):
        payment_method.pay(amount)

# Usage
processor = PaymentProcessor()
processor.process_payment(CreditCardPayment(), 100)
processor.process_payment(PayPalPayment(), 200)

```

### Benefit of this approach

- If we want to add new payment, we can just create a new class (open for extension ) say GPya without modifying existing PaymentProcessor thus it remains unchanged (closed for modification)

## Example 3: Advanced Product Filter (From Your Code)

This is a powerful real-world example showing how to build a **flexible filtering system** that follows OCP.

### The Problem: Hard-coded Filters ❌

Imagine you need to filter products by color, size, and quality. A bad approach would be:

```python
class BadProductFilter:
    def filter_by_color(self, products, color):
        for p in products:
            if p.color == color:
                yield p
    
    def filter_by_size(self, products, size):
        for p in products:
            if p.size == size:
                yield p
    
    def filter_by_color_and_size(self, products, color, size):
        for p in products:
            if p.color == color and p.size == size:
                yield p
    
    # What if we need color AND size AND quality? 
    # What if we need color OR size?
    # We'd need to keep adding methods! 😱
```

**Problems:**

- Every new filter combination needs a new method
- Exponential growth: 3 attributes = 7+ possible combinations
- Violates OCP: keeps modifying the filter class

### The Solution: Specification Pattern ✅

The code uses the **Specification Pattern** to solve this elegantly:

```python
# Step 1: Define the abstract Specification
class Specification(ABC):
    @abstractmethod
    def is_satisfied(self, item: Product):
        """Check if item meets this specification"""
        pass
    
    def __and__(self, other):
        """Overload & operator for combining specs"""
        return AndSpecification(self, other)
```

**Key Insight:** Each specification is a **separate, reusable rule** that can be combined!

```python
# Step 2: Create specific specifications (EXTENSION, not modification!)
class ColorSpecification(Specification):
    def __init__(self, color):
        self.color = color
    
    def is_satisfied(self, item):
        return item.color == self.color

class SizeSpecification(Specification):
    def __init__(self, size):
        self.size = size
    
    def is_satisfied(self, item):
        return item.size == self.size

class QualitySpecification(Specification):
    def __init__(self, quality):
        self.quality = quality
    
    def is_satisfied(self, item):
        return item.quality == self.quality
```

```python
# Step 3: Combine specifications with AND/OR logic
class AndSpecification(Specification):
    def __init__(self, *args):
        self.args = args
    
    def is_satisfied(self, item):
        # ALL specifications must be satisfied
        return all(map(lambda spec: spec.is_satisfied(item), self.args))

class OrSpecification(Specification):
    def __init__(self, *args):
        self.args = args
    
    def is_satisfied(self, item):
        # ANY specification must be satisfied
        return any(map(lambda spec: spec.is_satisfied(item), self.args))
```

```python
# Step 4: Single Filter class (NEVER needs modification!)
class Filter:
    def filter(self, items, spec):
        for item in items:
            if spec.is_satisfied(item):
                yield item
```

### How to Use It 🚀

```python
# Create products
apple = Product("Apple", Color.GREEN, Size.SMALL, Quality.ECONOMY)
tree = Product("Tree", Color.GREEN, Size.LARGE, Quality.MEDIUM)
house = Product("House", Color.BLUE, Size.LARGE, Quality.PREMIUM)

products = [apple, tree, house]

# Create the filter (only once!)
filter = Filter()

# Example 1: Simple filter - all green products
green_spec = ColorSpecification(Color.GREEN)
for p in filter.filter(products, green_spec):
    print(f"Green: {p.name}")
# Output: Apple, Tree

# Example 2: Combined filter - large AND blue AND premium
large_blue_premium = (
    SizeSpecification(Size.LARGE) & 
    ColorSpecification(Color.BLUE) & 
    QualitySpecification(Quality.PREMIUM)
)
for p in filter.filter(products, large_blue_premium):
    print(f"Large, Blue, Premium: {p.name}")
# Output: House

# Example 3: OR logic - small OR economy quality
small_or_economy = OrSpecification(
    SizeSpecification(Size.SMALL),
    QualitySpecification(Quality.ECONOMY)
)
for p in filter.filter(products, small_or_economy):
    print(f"Small OR Economy: {p.name}")
# Output: Apple
```

### Why This Follows OCP ✨

| Aspect | How it follows OCP |
|--------|-------------------|
| **Adding new attribute** | Just create a new `XxxSpecification` class - no modification of existing code |
| **Adding new combination** | Use `&` operator or create `AndSpecification`/`OrSpecification` - Filter class unchanged |
| **Adding new logic** | Create `NotSpecification`, `XorSpecification`, etc. - existing classes untouched |
| **Filter class** | Completely generic - works with ANY specification without knowing implementation details |

### Real-World Benefits 🎯

1. **Scalability**: Add 100 new product attributes? Just create 100 new specification classes!
2. **Testability**: Each specification is small and independently testable
3. **Reusability**: `ColorSpecification(Color.GREEN)` can be reused across the application
4. **Composition**: Build complex filters from simple building blocks
5. **Maintainability**: Bug in color filtering? Only fix `ColorSpecification`, nothing else breaks

### Operator Overloading Magic 🪄

The `__and__` method overloads the `&` operator:

```python
def __and__(self, other):
    return AndSpecification(self, other)

# This allows:
spec = ColorSpecification(Color.GREEN) & SizeSpecification(Size.LARGE)

# Instead of:
spec = AndSpecification(ColorSpecification(Color.GREEN), SizeSpecification(Size.LARGE))
```

**⚠️ Important:** Use `&` (bitwise AND), not `and` (logical AND)!

## Conclusion: Open/Closed Principle (OCP)

The **Open/Closed Principle (OCP)** ensures code is **open for extension but closed for modification**, allowing new features without altering existing code.

### Benefits of OCP

- **Maintainability** – Stable, bug-free code remains untouched  
- **Scalability** – Easy feature expansion without risk  
- **Flexibility** – Encourages abstraction & polymorphism  
- **Testability** – Existing tests don't break with new features
- **Reduced Bugs** – Less modification = fewer chances to introduce bugs

### 🔹 How to Apply OCP

1. **Use abstract classes & interfaces** – Define contracts, not implementations
2. **Apply inheritance or composition** – Extend behavior through new classes
3. **Follow dependency injection** – Depend on abstractions, not concrete types
4. **Use design patterns** – Strategy, Specification, Template Method, etc.
5. **Think "plug-and-play"** – New features should plug in like USB devices

### 🎓 Key Takeaway

> "Write code that is **open for extension** (easy to add features) but **closed for modification** (existing code stays stable). This makes your codebase resilient to change and easy to grow."
