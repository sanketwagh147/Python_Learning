# Open Close Principle

#### Software entities (such as classes, modules, and functions) should be open for extension but closed for modification.
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

## Conclusion: Open/Closed Principle (OCP)

The **Open/Closed Principle (OCP)** ensures code is **open for extension but closed for modification**, allowing new features without altering existing code.

###  Benefits of OCP:
- **Maintainability** – Stable, bug-free code.  
- **Scalability** – Easy feature expansion.  
- **Flexibility** – Encourages abstraction & polymorphism.  

### 🔹 How to Apply OCP:
- Use **abstract classes & interfaces**.  
- Apply **inheritance or composition**.  
- Follow **dependency injection**.  

