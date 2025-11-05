"""
Single Responsibility Principle (SRP) - Practical Examples

Key Concept: A class should have only ONE reason to change.
            A class should do ONE thing and do it well.

This file demonstrates SRP with runnable examples comparing BAD and GOOD designs.
"""

# ============================================================================
# Example 1: Employee Management System
# ============================================================================

print("\n" + "=" * 70)
print("EXAMPLE 1: Employee Management")
print("=" * 70)

# ❌ BAD: Multiple Responsibilities
print("\n--- BAD Design (Violates SRP) ---")


class BadEmployee:
    """This class violates SRP by handling too many responsibilities"""

    def __init__(self, name, salary):
        self.name = name
        self.salary = salary

    def calculate_salary(self):
        """Business logic"""
        bonus = self.salary * 0.1
        return self.salary + bonus

    def save_to_database(self):
        """Database operations"""
        print(f"💾 Saving {self.name} to database...")

    def generate_report(self):
        """Report generation"""
        return f"📄 Report: {self.name} earns ${self.salary}"


# Using BadEmployee
bad_emp = BadEmployee("Alice", 50000)
print(bad_emp.generate_report())
bad_emp.save_to_database()
print(f"Total salary: ${bad_emp.calculate_salary()}")
print("\n⚠️  Problem: This class has 3 reasons to change:")
print("   1. Business logic changes (salary calculation)")
print("   2. Database schema changes")
print("   3. Report format changes")


# ✅ GOOD: Separated Responsibilities
print("\n--- GOOD Design (Follows SRP) ---")


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

    def calculate_annual_salary(self, employee):
        monthly = self.calculate_salary(employee)
        return monthly * 12


class EmployeeRepository:
    """Single Responsibility: Handle database operations"""

    def save(self, employee):
        print(f"💾 Saving {employee.name} to database...")

    def find_by_name(self, name):
        print(f"🔍 Finding employee: {name}")
        return None


class EmployeeReportGenerator:
    """Single Responsibility: Generate reports"""

    def generate_report(self, employee, total_salary):
        return f"📄 Report: {employee.name} earns ${total_salary}"


# Using the good design
emp = Employee("Alice", 50000)
calculator = SalaryCalculator()
repository = EmployeeRepository()
report_gen = EmployeeReportGenerator()

total = calculator.calculate_salary(emp)
annual = calculator.calculate_annual_salary(emp)
repository.save(emp)
print(report_gen.generate_report(emp, total))
print(f"Annual salary: ${annual}")
print("\n✅ Benefit: Each class has ONE reason to change!")


# ============================================================================
# Example 2: E-Commerce Order System
# ============================================================================

print("\n" + "=" * 70)
print("EXAMPLE 2: E-Commerce Order System")
print("=" * 70)

# ❌ BAD: God Class (does everything)
print("\n--- BAD Design (God Class) ---")


class BadOrder:
    """This class tries to do EVERYTHING - a common anti-pattern"""

    def __init__(self, items):
        self.items = items

    def calculate_total(self):
        total = sum(item["price"] * item["qty"] for item in self.items)
        print(f"💰 Total: ${total}")
        return total

    def process_payment(self, payment_method):
        print(f"💳 Processing payment via {payment_method}...")
        # Payment gateway code here
        pass

    def send_invoice(self, email):
        print(f"📧 Sending invoice to {email}...")
        # Email service code here
        pass

    def save_to_database(self):
        print("💾 Saving order to database...")
        # Database code here
        pass


# Using BadOrder
bad_items = [{"name": "Laptop", "price": 1000, "qty": 1}]
bad_order = BadOrder(bad_items)
bad_order.calculate_total()
bad_order.process_payment("credit_card")
bad_order.send_invoice("customer@example.com")
bad_order.save_to_database()
print("\n⚠️  Problem: Tightly coupled to payment gateway, email service, and database!")


# ✅ GOOD: Separated Concerns
print("\n--- GOOD Design (Separated Concerns) ---")


class Order:
    """Single Responsibility: Hold order data"""

    def __init__(self, items):
        self.items = items
        self.id = None


class OrderCalculator:
    """Single Responsibility: Calculate order totals"""

    def calculate_total(self, order):
        total = sum(item["price"] * item["qty"] for item in order.items)
        print(f"💰 Total: ${total}")
        return total

    def calculate_tax(self, order, rate=0.1):
        total = self.calculate_total(order)
        return total * rate


class PaymentProcessor:
    """Single Responsibility: Process payments"""

    def process(self, amount, method):
        print(f"💳 Processing ${amount} via {method}...")
        return {"status": "success", "transaction_id": "TXN123"}


class InvoiceService:
    """Single Responsibility: Send invoices"""

    def send(self, order, email, amount):
        print(f"📧 Sending invoice for ${amount} to {email}...")
        return True


class OrderRepository:
    """Single Responsibility: Database operations"""

    def save(self, order):
        print("💾 Saving order to database...")
        order.id = "ORD123"
        return order


# Using the good design
items = [{"name": "Laptop", "price": 1000, "qty": 1}]
order = Order(items)

calc = OrderCalculator()
payment = PaymentProcessor()
invoice = InvoiceService()
repo = OrderRepository()

# Each component does ONE thing
total = calc.calculate_total(order)
result = payment.process(total, "credit_card")
if result["status"] == "success":
    invoice.send(order, "customer@example.com", total)
    repo.save(order)

print(f"\n✅ Benefit: Easy to swap payment processors or email services!")


# ============================================================================
# Example 3: User Authentication System
# ============================================================================

print("\n" + "=" * 70)
print("EXAMPLE 3: User Authentication System")
print("=" * 70)

# ❌ BAD: Mixed Concerns
print("\n--- BAD Design (Mixed Concerns) ---")


class BadAuthService:
    """Handles registration, authentication, email, and logging"""

    def register_user(self, username, password, email):
        print(f"👤 Registering {username}...")
        # Validation
        # Password hashing
        # Database save
        # Send email
        # Log activity
        print(f"📧 Sending welcome email to {email}...")
        print(f"📝 Logging registration...")
        return True

    def authenticate(self, username, password):
        print(f"🔐 Authenticating {username}...")
        # Database query
        # Password verification
        # Log activity
        return True


bad_auth = BadAuthService()
bad_auth.register_user("john", "pass123", "john@example.com")
bad_auth.authenticate("john", "pass123")
print("\n⚠️  Problem: Can't test auth without email service!")


# ✅ GOOD: Clear Separation
print("\n--- GOOD Design (Clear Separation) ---")


class User:
    """Single Responsibility: User data model"""

    def __init__(self, username, email, password_hash):
        self.username = username
        self.email = email
        self.password_hash = password_hash


class PasswordHasher:
    """Single Responsibility: Hash and verify passwords"""

    def hash(self, password):
        return f"hashed_{password}"

    def verify(self, password, hashed):
        return f"hashed_{password}" == hashed


class UserRepository:
    """Single Responsibility: User database operations"""

    def __init__(self):
        self.users = {}

    def save(self, user):
        self.users[user.username] = user
        print(f"💾 Saved user: {user.username}")
        return user

    def find_by_username(self, username):
        return self.users.get(username)


class EmailService:
    """Single Responsibility: Send emails"""

    def send_welcome_email(self, email):
        print(f"📧 Sending welcome email to {email}")

    def send_password_reset(self, email):
        print(f"📧 Sending password reset to {email}")


class ActivityLogger:
    """Single Responsibility: Log user activities"""

    def log(self, username, action):
        print(f"📝 Log: {username} - {action}")


class UserRegistrationService:
    """Single Responsibility: Coordinate user registration"""

    def __init__(self, user_repo, email_service, hasher, logger):
        self.user_repo = user_repo
        self.email_service = email_service
        self.hasher = hasher
        self.logger = logger

    def register(self, username, password, email):
        print(f"👤 Registering {username}...")

        # Hash password
        hashed = self.hasher.hash(password)

        # Create and save user
        user = User(username, email, hashed)
        self.user_repo.save(user)

        # Send email
        self.email_service.send_welcome_email(email)

        # Log activity
        self.logger.log(username, "registered")

        return user


class AuthenticationService:
    """Single Responsibility: Verify credentials"""

    def __init__(self, user_repo, hasher, logger):
        self.user_repo = user_repo
        self.hasher = hasher
        self.logger = logger

    def authenticate(self, username, password):
        print(f"🔐 Authenticating {username}...")

        user = self.user_repo.find_by_username(username)
        if user and self.hasher.verify(password, user.password_hash):
            self.logger.log(username, "logged in")
            return {"authenticated": True, "user": user}

        return {"authenticated": False}


# Using the good design
user_repo = UserRepository()
email_service = EmailService()
hasher = PasswordHasher()
logger = ActivityLogger()

registration = UserRegistrationService(user_repo, email_service, hasher, logger)
auth = AuthenticationService(user_repo, hasher, logger)

# Register new user
registration.register("john", "pass123", "john@example.com")

# Authenticate
result = auth.authenticate("john", "pass123")
if result["authenticated"]:
    user = result["user"]
    if isinstance(user, User):
        print(f"✅ Welcome back, {user.username}!")

print("\n✅ Benefit: Each service can be tested independently!")
print("✅ Benefit: Easy to mock email service for testing!")
print("✅ Benefit: Can swap hasher (bcrypt → argon2) without changing auth!")


# ============================================================================
# Summary
# ============================================================================

print("\n" + "=" * 70)
print("🎯 KEY TAKEAWAYS")
print("=" * 70)
print(
    """
1. ONE CLASS = ONE RESPONSIBILITY
   Each class should have a single, well-defined purpose.

2. ONE REASON TO CHANGE
   A class should change only when its single responsibility needs to change.

3. HIGH COHESION
   All methods in a class should relate to its core purpose.

4. LOOSE COUPLING
   Classes should depend on abstractions, not concrete implementations.

5. EASIER TESTING
   Small, focused classes are simple to test in isolation.

6. BETTER REUSABILITY
   Single-purpose classes can be reused across different contexts.

7. TEAM COLLABORATION
   Different developers can work on different classes without conflicts.

Remember: If you can describe your class with "AND" or "OR", 
it probably violates SRP! 🚫

"Do one thing, do it well, do only that thing." ✅
"""
)

print("=" * 70 + "\n")
