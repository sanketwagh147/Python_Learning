# Dependency Inversion
- High-level modules (business logic) should not depend on low-level modules (implementation details). Both should depend on abstractions (interfaces or abstract classes).
- Abstractions should not depend on details. Instead, details (implementations) should depend on abstractions.


### Example 1 (violates dip)
```python
class MySQLDatabase:
    def connect(self):
        print("Connecting to MySQL database...")

class DataService:
    def __init__(self):
        self.db = MySQLDatabase()  # Direct dependency on a concrete class

    def fetch_data(self):
        self.db.connect()
        print("Fetching data...")
```

#### Problem:
 `DataService` is tightly coupled to `MySQLDatabase`, making it difficult to switch to another database (e.g., PostgreSQL).

### Example 1 (follows dip )
```python
from abc import ABC, abstractmethod

# Abstraction (Interface)
class Database(ABC):
    @abstractmethod
    def connect(self):
        pass

# Concrete Implementations
class MySQLDatabase(Database):
    def connect(self):
        print("Connecting to MySQL database...")

class PostgreSQLDatabase(Database):
    def connect(self):
        print("Connecting to PostgreSQL database...")

# High-Level Module
class DataService:
    def __init__(self, db: Database):  # Depend on abstraction
        self.db = db

    def fetch_data(self):
        self.db.connect()
        print("Fetching data...")

# Usage
db = MySQLDatabase()  # We can swap this with PostgreSQLDatabase easily
service = DataService(db)
service.fetch_data()
```
Here `DataService`, `PostgreSQLDatabase` and `MySQLDatabase` all depend on abstractions

### Example 2 ( violates dop)
```python 
class PayPalPayment:
    def process_payment(self, amount):
        print(f"Processing payment of ${amount} via PayPal.")

class OrderService:
    def __init__(self):
        self.payment_processor = PayPalPayment()  # Tight coupling to PayPal

    def checkout(self, amount):
        self.payment_processor.process_payment(amount)
        print("Order placed successfully!")

```
#### problems
- The `OrderService` is directly dependent on `PayPalPayment`.
- If we want to switch to another payment gateway (e.g., Stripe), we must modify `OrderService`.

### solution (follows DIP):
```python
from abc import ABC, abstractmethod

# Abstraction (Interface)
class PaymentProcessor(ABC):
    @abstractmethod
    def process_payment(self, amount):
        pass

# Concrete Implementations
class PayPalPayment(PaymentProcessor):
    def process_payment(self, amount):
        print(f"Processing payment of ${amount} via PayPal.")

class StripePayment(PaymentProcessor):
    def process_payment(self, amount):
        print(f"Processing payment of ${amount} via Stripe.")

# High-Level Module
class OrderService:
    def __init__(self, payment_processor: PaymentProcessor):  # Depend on abstraction
        self.payment_processor = payment_processor

    def checkout(self, amount):
        self.payment_processor.process_payment(amount)
        print("Order placed successfully!")

# Usage
payment = StripePayment()  # Can be swapped with PayPalPayment easily
order_service = OrderService(payment)
order_service.checkout(100)
```

#### Benefits
- `OrderService` depends on `PaymentProcessor` (abstraction) instead of a concrete class.
Easily switch between different payment gateways without modifying `OrderService`.
- Makes testing easier by mocking the `PaymentProcessor`.


## Conclusion
DIP helps build modular, maintainable, and scalable software by decoupling dependencies. It is best implemented with Dependency Injection (DI) and design patterns like Pub-Sub, Factory, and Strategy Patterns.

