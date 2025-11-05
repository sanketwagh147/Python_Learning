# Single Responsibility Principle (Separation of concerns / SRP)

> **"A class should have only ONE reason to change."** - Robert C. Martin

## What is SRP?

The Single Responsibility Principle states that a class should have **only one responsibility** or **one job**. This is also known as **Separation of Concerns**.

### Key Concepts

- **One Reason to Change**: A class should change only when its single responsibility needs to change
- **High Cohesion**: All methods in a class should be related to its single purpose
- **Easier Maintenance**: When each class does one thing, bugs are easier to find and fix
- **Better Testing**: Small, focused classes are easier to test

### How to Identify Multiple Responsibilities?

Ask yourself: **"What does this class do?"** If your answer includes "AND" or "OR", it probably violates SRP!

❌ "This class manages employees AND saves them to the database"
✅ "This class manages employee data"

---

## Example 1: Employee Management

### ❌ Violates SRP

```python
class Employee:
    def __init__(self, name, salary):
        self.name = name
        self.salary = salary

    def calculate_salary(self):
        """Business logic for salary calculation"""
        bonus = self.salary * 0.1
        return self.salary + bonus

    def save_to_database(self):
        """Database operations"""
        print(f"Saving {self.name} to database...")
        # Database connection and SQL queries
        pass

    def generate_report(self):
        """Generate employee report"""
        print(f"Generating report for {self.name}...")
        return f"Employee: {self.name}, Salary: {self.salary}"
```

### Problems

1. **Multiple Responsibilities**: This class does THREE things:
   - Manages employee data
   - Handles salary calculations (business logic)
   - Performs database operations (persistence)
   - Generates reports (presentation)

2. **Multiple Reasons to Change**:
   - If salary calculation logic changes → modify this class
   - If database schema changes → modify this class
   - If report format changes → modify this class

3. **Hard to Test**: You need to mock database, setup business rules, etc., all at once

4. **Poor Reusability**: Can't reuse salary calculator for other entities

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

### ✅ Follows SRP

```python
class Employee:
    """Single Responsibility: Hold employee data"""
    def __init__(self, name, salary):
        self.name = name
        self.salary = salary


class SalaryCalculator:
    """Single Responsibility: Handle salary calculations"""
    def calculate_salary(self, employee):
        bonus = employee.salary * 0.1
        return employee.salary + bonus


class EmployeeRepository:
    """Single Responsibility: Handle database operations"""
    def save_to_database(self, employee):
        print(f"Saving {employee.name} to database...")
        # Database connection and SQL queries
        pass


class EmployeeReportGenerator:
    """Single Responsibility: Generate reports"""
    def generate_report(self, employee):
        return f"Employee: {employee.name}, Salary: {employee.salary}"


# Usage
emp = Employee("John Doe", 50000)
calculator = SalaryCalculator()
repository = EmployeeRepository()
report_gen = EmployeeReportGenerator()

total_salary = calculator.calculate_salary(emp)
repository.save_to_database(emp)
report = report_gen.generate_report(emp)
```

### Benefits

✅ **Separation of Concerns**: Each class has ONE clear purpose

✅ **Easy to Maintain**: Changing salary logic doesn't affect database code

✅ **Easy to Test**: Test each class independently

✅ **Reusable**: `SalaryCalculator` can be used for contractors, managers, etc.

✅ **Flexible**: Swap database implementation without touching business logic

---

## Example 2: E-Commerce Order System

### ❌ Violates SRP
```python
class Order:
    def __init__(self, items):
        self.items = items

    def calculate_total(self):
        """Calculate total price"""
        total = sum(item['price'] * item['quantity'] for item in self.items)
        return total

    def process_payment(self, payment_method):
        """Process payment"""
        print(f"Processing payment via {payment_method}...")
        # Payment gateway integration
        pass

    def send_invoice(self, email):
        """Send invoice to customer"""
        print(f"Sending invoice to {email}...")
        # Email service integration
        pass

    def save_to_database(self):
        """Save order to database"""
        print("Saving order to database...")
        # Database operations
        pass
```

### Problems

1. **Too Many Responsibilities**: This class handles:
   - Order data management
   - Price calculations (business logic)
   - Payment processing (external service)
   - Email notifications (external service)
   - Database persistence

2. **Hard Dependencies**: Tightly coupled to payment gateway, email service, and database

3. **Difficult Testing**: Need to mock payment systems, email servers, and databases

4. **Low Reusability**: Can't reuse payment logic for other entities

### ✅ Follows SRP

```python
class Order:
    """Single Responsibility: Hold order data"""
    def __init__(self, items):
        self.items = items


class OrderCalculator:
    """Single Responsibility: Calculate order totals"""
    def calculate_total(self, order):
        return sum(item['price'] * item['quantity'] for item in order.items)
    
    def calculate_tax(self, order, tax_rate=0.1):
        total = self.calculate_total(order)
        return total * tax_rate


class PaymentProcessor:
    """Single Responsibility: Process payments"""
    def process_payment(self, amount, payment_method):
        print(f"Processing ${amount} via {payment_method}...")
        # Integration with payment gateway (Stripe, PayPal, etc.)
        return {"status": "success", "transaction_id": "12345"}


class InvoiceSender:
    """Single Responsibility: Send invoices"""
    def send_invoice(self, order, email, total):
        print(f"Sending invoice for ${total} to {email}...")
        # Email service integration
        return True


class OrderRepository:
    """Single Responsibility: Database operations"""
    def save(self, order):
        print("Saving order to database...")
        # Database operations
        pass


# Usage
items = [
    {"name": "Laptop", "price": 1000, "quantity": 1},
    {"name": "Mouse", "price": 25, "quantity": 2}
]

order = Order(items)
calculator = OrderCalculator()
payment = PaymentProcessor()
invoice = InvoiceSender()
repository = OrderRepository()

# Each component does ONE thing
total = calculator.calculate_total(order)
tax = calculator.calculate_tax(order)
payment.process_payment(total + tax, "credit_card")
invoice.send_invoice(order, "customer@example.com", total + tax)
repository.save(order)
```

### Benefits

✅ **Modularity**: Each class is a standalone module

✅ **Easy to Replace**: Swap payment processors (Stripe → PayPal) without touching other code

✅ **Independent Testing**: Test calculator without needing database or email server

✅ **Clear Dependencies**: Each class's dependencies are explicit

---

## Example 3: User Authentication System

### ❌ Violates SRP
```python
class AuthService:
    def register_user(self, user_data):
        """Register new user"""
        print(f"Registering user: {user_data['username']}")
        # Validate data
        # Hash password
        # Save to database
        # Send welcome email
        pass

    def authenticate_user(self, username, password):
        """Check credentials"""
        print(f"Authenticating {username}...")
        # Query database
        # Compare password hash
        pass

    def send_welcome_email(self, email):
        """Send welcome email"""
        print(f"Sending welcome email to {email}...")
        # Email service logic
        pass

    def log_activity(self, user_id, action):
        """Log user activity"""
        print(f"Logging: User {user_id} performed {action}")
        # Logging logic
        pass
```

### Problems

1. **Mixed Concerns**: Registration, authentication, email, and logging all in one place

2. **Fragile Code**: Changing email template requires modifying authentication class

3. **Testing Nightmare**: Can't test authentication without email service being available

### ✅ Follows SRP

```python
class UserRegistrationService:
    """Single Responsibility: Handle user registration"""
    def __init__(self, user_repo, email_service, password_hasher):
        self.user_repo = user_repo
        self.email_service = email_service
        self.password_hasher = password_hasher
    
    def register(self, user_data):
        # Validate user data
        if not self._validate(user_data):
            return {"error": "Invalid data"}
        
        # Hash password
        hashed_password = self.password_hasher.hash(user_data['password'])
        
        # Save user
        user = self.user_repo.save({
            "username": user_data['username'],
            "email": user_data['email'],
            "password": hashed_password
        })
        
        # Send welcome email
        self.email_service.send_welcome_email(user['email'])
        
        return user
    
    def _validate(self, user_data):
        return 'username' in user_data and 'password' in user_data


class AuthenticationService:
    """Single Responsibility: Verify user credentials"""
    def __init__(self, user_repo, password_hasher):
        self.user_repo = user_repo
        self.password_hasher = password_hasher
    
    def authenticate(self, username, password):
        user = self.user_repo.find_by_username(username)
        if user and self.password_hasher.verify(password, user['password']):
            return {"authenticated": True, "user": user}
        return {"authenticated": False}


class EmailService:
    """Single Responsibility: Send emails"""
    def send_welcome_email(self, email):
        print(f"📧 Sending welcome email to {email}")
        # Email template and sending logic
        pass
    
    def send_password_reset(self, email, token):
        print(f"📧 Sending password reset to {email}")
        pass


class ActivityLogger:
    """Single Responsibility: Log user activities"""
    def log(self, user_id, action):
        print(f"📝 Log: User {user_id} - {action}")
        # Write to log file or logging service
        pass


class PasswordHasher:
    """Single Responsibility: Hash and verify passwords"""
    def hash(self, password):
        # Use bcrypt or similar
        return f"hashed_{password}"
    
    def verify(self, password, hashed):
        return f"hashed_{password}" == hashed


# Usage Example
user_repo = UserRepository()
email_service = EmailService()
hasher = PasswordHasher()
logger = ActivityLogger()

registration = UserRegistrationService(user_repo, email_service, hasher)
auth = AuthenticationService(user_repo, hasher)

# Register new user
new_user = registration.register({
    "username": "john_doe",
    "email": "john@example.com",
    "password": "secure123"
})

# Authenticate user
result = auth.authenticate("john_doe", "secure123")
if result['authenticated']:
    logger.log(result['user']['id'], "login")
```

### Why This is Better

✅ **Clear Separation**: Each service has ONE well-defined job

✅ **Easy to Mock**: Test authentication without sending real emails

✅ **Swappable Components**: Change email provider without touching auth logic

✅ **Dependency Injection**: Dependencies are explicit and injectable

✅ **Single Reason to Change**: Email template change? Only modify `EmailService`

---

## Real-World Benefits of SRP

### 🎯 Maintainability

- **Before**: "Where do I fix the email bug?" → Search through 500-line class
- **After**: "Email issue? Check `EmailService`" → 50-line focused class

### 🧪 Testability

- **Before**: Need to mock database, email, payment gateway for one test
- **After**: Test each component independently with simple mocks

### 🔄 Reusability

- **Before**: Copy-paste code because it's tangled with other logic
- **After**: Import and reuse `EmailService` in any project

### 👥 Team Collaboration

- **Before**: Merge conflicts when multiple people edit same giant class
- **After**: Different developers work on different classes

### 🐛 Debugging

- **Before**: Bug could be anywhere in the 1000-line class
- **After**: Bug is in the specific, small, focused class

---

## How to Apply SRP

### Step 1: Identify Responsibilities

List what your class does. If you use "AND", you likely have multiple responsibilities.

### Step 2: Extract Classes

Create separate classes for each responsibility.

### Step 3: Use Dependency Injection

Pass dependencies through constructor instead of creating them inside.

### Step 4: Test Each Class

If a class is hard to test, it probably has too many responsibilities.

---

## Common Signs of SRP Violation

❌ **Class names with "Manager", "Handler", "Controller"** (too generic)

❌ **Methods that don't use the class's properties** (probably belongs elsewhere)

❌ **Many import statements** (too many dependencies)

❌ **Large classes** (>200 lines often indicates multiple responsibilities)

❌ **Difficult to name the class** (unclear responsibility)

---

## Conclusion

The **Single Responsibility Principle** is the foundation of clean, maintainable code:

### Key Takeaways

✅ **One Class, One Job**: Each class should do ONE thing well

✅ **One Reason to Change**: A class should change only when its single responsibility changes

✅ **High Cohesion**: All methods in a class should relate to its purpose

✅ **Loose Coupling**: Classes should depend on abstractions, not concrete implementations

### Remember

> "Do one thing, do it well, do only that thing." - Unix Philosophy

When in doubt, ask yourself: **"If I need to change X, how many classes do I need to modify?"**

If the answer is "more than one", you might be violating SRP! 🎯

---

## Quick Reference Card

### ✅ DO

```python
class UserRepository:
    """Handles only database operations"""
    def save(self, user): pass
    def find(self, id): pass
    def delete(self, id): pass
```

### ❌ DON'T

```python
class UserManager:
    """Does everything - BAD!"""
    def save(self, user): pass
    def send_email(self, user): pass
    def calculate_age(self, user): pass
    def log_activity(self, user): pass
```

### Questions to Ask

1. **Can I describe this class in one sentence without using "AND"?**
2. **How many reasons does this class have to change?**
3. **Can I test this class without mocking multiple external services?**
4. **Would I reuse this class in another project?**
5. **Is the class name specific enough?**

If any answer is problematic, consider refactoring! 🔨
