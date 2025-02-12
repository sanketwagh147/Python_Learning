# Single Responsibility Principle (Separation of concerns)
The Single Responsibility Principle (SRP) states that a class should have &**only one reason to change**.

In other words, a class should have only **one responsibility or one job**

# Example 1
## Violates SRP
```python
class Employee:
    def __init__(self, name, salary):
        self.name = name
        self.salary = salary

    def calculate_salary(self):
        # Business logic for salary calculation
        pass

    def save_to_database(self):
        # Logic to save employee data to DB
        pass
```

### Problem
This class handles both salary calculations and database operations. These are two separate concerns

## Follows SRP
```python
class Employee:
    def __init__(self, name, salary):
        self.name = name
        self.salary = salary

class SalaryCalculator:
    def calculate_salary(self, employee):
        # Business logic for salary calculation
        pass

class EmployeeRepository:
    def save_to_database(self, employee):
        # Logic to save employee data to DB
        pass

```
### Solution
- Employee only holds employee data.
- SalaryCalculator handles salary logic.
- EmployeeRepository is responsible for database operations.

# Example 2
## Violates SRP
```python
class Order:
    def __init__(self, items):
        self.items = items

    def calculate_total(self):
        # Business logic to calculate total price
        pass

    def process_payment(self):
        # Logic to process payment
        pass

    def send_invoice(self):
        # Logic to send invoice email
        pass

```

### Problem
The Order class does too many things—handling total calculation, payment processing, and invoice sending.

## Follows SRP
```python
class Order:
    def __init__(self, items):
        self.items = items

class OrderCalculator:
    def calculate_total(self, order):
        # Business logic to calculate total price
        pass

class PaymentProcessor:
    def process_payment(self, order):
        # Logic to process payment
        pass

class InvoiceSender:
    def send_invoice(self, order):
        # Logic to send invoice email
        pass


```
### Solution
- Order just holds order details.
- OrderCalculator calculates the total.
- PaymentProcessor processes payments.
- InvoiceSender sends invoices

# Example 3
## Violates SRP
```python
class AuthService:
    def register_user(self, user_data):
        # Logic to register user
        pass

    def authenticate_user(self, username, password):
        # Logic to check credentials
        pass

    def send_welcome_email(self, email):
        # Logic to send a welcome email
        pass


```

### Problem
This class handles user registration, authentication, and email sending—three separate concerns.

## Follows SRP
```python
class UserService:
    def register_user(self, user_data):
        # Logic to register user
        pass

class AuthService:
    def authenticate_user(self, username, password):
        # Logic to check credentials
        pass

class EmailService:
    def send_welcome_email(self, email):
        # Logic to send a welcome email
        pass
```
### Solution
- UserService manages user registration.
- AuthService handles authentication.
- EmailService sends emails.

## Conclusion
- SRP helps keep classes focused and easy to maintain.
- Code changes are easier since different concerns are separated.
- Testing is simpler, as each class has only one responsibility.
