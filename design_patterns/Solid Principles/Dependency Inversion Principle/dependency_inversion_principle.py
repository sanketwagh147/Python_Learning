"""Examples on dependency inversion and dependency injection"""

from abc import ABC, abstractmethod


# ============================================================
# EXAMPLE 1: Notification System
# ============================================================

# ❌ BAD — Violates DIP
# OrderService directly depends on a concrete EmailSender class.
# If we later want to send SMS or push notifications, we must
# modify OrderService itself — tightly coupling business logic
# to a specific notification channel.

class EmailSender:
    def send(self, to: str, message: str):
        print(f"Sending EMAIL to {to}: {message}")


class BadOrderService:
    def __init__(self):
        self.notifier = EmailSender()          # ← hard-coded dependency

    def place_order(self, customer_email: str):
        print("Order placed!")
        self.notifier.send(customer_email, "Your order has been confirmed.")


# ✅ GOOD — Follows DIP
# Both the high-level module (OrderService) and the low-level
# modules (EmailNotifier, SMSNotifier, PushNotifier) depend on
# the Notifier abstraction. We can swap notification channels
# without touching OrderService at all.

class Notifier(ABC):
    @abstractmethod
    def send(self, to: str, message: str) -> None:
        pass


class EmailNotifier(Notifier):
    def send(self, to: str, message: str) -> None:
        print(f"📧 EMAIL to {to}: {message}")


class SMSNotifier(Notifier):
    def send(self, to: str, message: str) -> None:
        print(f"📱 SMS to {to}: {message}")


class PushNotifier(Notifier):
    def send(self, to: str, message: str) -> None:
        print(f"🔔 PUSH to {to}: {message}")


class GoodOrderService:
    def __init__(self, notifier: Notifier):    # ← depends on abstraction
        self.notifier = notifier

    def place_order(self, customer_contact: str):
        print("Order placed!")
        self.notifier.send(customer_contact, "Your order has been confirmed.")


# Usage — easy to swap
print("=== Example 1: Notification System ===")
email_order = GoodOrderService(EmailNotifier())
email_order.place_order("alice@example.com")

sms_order = GoodOrderService(SMSNotifier())
sms_order.place_order("+1-555-0100")


# ============================================================
# EXAMPLE 2: Data Storage / Repository Pattern
# ============================================================

# ❌ BAD — Violates DIP
# UserService directly creates a PostgresDB connection inside
# itself. Switching to MongoDB, an in-memory cache, or a test
# double means rewriting UserService.

class PostgresDB:
    def query(self, sql: str):
        print(f"[Postgres] Running: {sql}")
        return [{"id": 1, "name": "Alice"}]


class BadUserService:
    def __init__(self):
        self.db = PostgresDB()                 # ← hard-coded dependency

    def get_user(self, user_id: int):
        return self.db.query(f"SELECT * FROM users WHERE id = {user_id}")


# ✅ GOOD — Follows DIP
# UserService depends on a UserRepository abstraction.
# We can plug in Postgres, MongoDB, or an in-memory fake
# without changing a single line in UserService.

class UserRepository(ABC):
    @abstractmethod
    def find_by_id(self, user_id: int) -> dict:
        pass


class PostgresUserRepository(UserRepository):
    def find_by_id(self, user_id: int) -> dict:
        print(f"[Postgres] SELECT * FROM users WHERE id = {user_id}")
        return {"id": user_id, "name": "Alice"}


class MongoUserRepository(UserRepository):
    def find_by_id(self, user_id: int) -> dict:
        print(f"[MongoDB] db.users.findOne({{id: {user_id}}})")
        return {"id": user_id, "name": "Alice"}


class InMemoryUserRepository(UserRepository):
    """Perfect for unit tests — no real DB needed."""
    def __init__(self):
        self._store = {1: {"id": 1, "name": "Alice"}}

    def find_by_id(self, user_id: int) -> dict:
        print(f"[InMemory] Looking up user {user_id}")
        return self._store.get(user_id, {})


class GoodUserService:
    def __init__(self, repo: UserRepository):  # ← depends on abstraction
        self.repo = repo

    def get_user(self, user_id: int) -> dict:
        return self.repo.find_by_id(user_id)


print("\n=== Example 2: Data Storage ===")
service = GoodUserService(PostgresUserRepository())
print(service.get_user(1))

test_service = GoodUserService(InMemoryUserRepository())
print(test_service.get_user(1))


# ============================================================
# EXAMPLE 3: Logging System
# ============================================================

# ❌ BAD — Violates DIP
# PaymentProcessor writes directly to a file. You can't log
# to the console, a remote service, or suppress logs in tests
# without editing PaymentProcessor.

class BadPaymentProcessor:
    def process(self, amount: float):
        print(f"Processing ${amount}...")
        with open("payments.log", "a") as f:   # ← hard-coded file logging
            f.write(f"Processed ${amount}\n")


# ✅ GOOD — Follows DIP
# PaymentProcessor depends on a Logger abstraction.
# Swap between file, console, or remote logging freely.

class Logger(ABC):
    @abstractmethod
    def log(self, message: str) -> None:
        pass


class ConsoleLogger(Logger):
    def log(self, message: str) -> None:
        print(f"[LOG] {message}")


class FileLogger(Logger):
    def __init__(self, path: str):
        self.path = path

    def log(self, message: str) -> None:
        # In production you'd actually write to the file
        print(f"[FILE → {self.path}] {message}")


class RemoteLogger(Logger):
    def __init__(self, endpoint: str):
        self.endpoint = endpoint

    def log(self, message: str) -> None:
        print(f"[REMOTE → {self.endpoint}] {message}")


class GoodPaymentProcessor:
    def __init__(self, logger: Logger):        # ← depends on abstraction
        self.logger = logger

    def process(self, amount: float):
        print(f"Processing ${amount}...")
        self.logger.log(f"Processed ${amount}")


print("\n=== Example 3: Logging System ===")
processor = GoodPaymentProcessor(ConsoleLogger())
processor.process(49.99)

remote_processor = GoodPaymentProcessor(RemoteLogger("https://logs.example.com"))
remote_processor.process(149.99)


# ============================================================
# EXAMPLE 4: Authentication — Multiple Strategies
# ============================================================

# ❌ BAD — Violates DIP
# LoginService hard-codes username/password auth.
# Adding OAuth, API-key, or biometric login means gutting
# this class with if/else branches.

class BadLoginService:
    def login(self, username: str, password: str) -> bool:
        # hard-coded to one auth mechanism
        if username == "admin" and password == "secret":
            print("Logged in!")
            return True
        print("Invalid credentials.")
        return False


# ✅ GOOD — Follows DIP
# LoginService depends on an AuthProvider abstraction.
# Each auth strategy is its own class; adding a new one
# requires zero changes to LoginService.

class AuthProvider(ABC):
    @abstractmethod
    def authenticate(self, **credentials) -> bool:
        pass


class PasswordAuth(AuthProvider):
    def authenticate(self, **credentials) -> bool:
        valid = credentials.get("username") == "admin" and credentials.get("password") == "secret"
        print(f"🔑 Password auth → {'success' if valid else 'failure'}")
        return valid


class OAuthProvider(AuthProvider):
    def authenticate(self, **credentials) -> bool:
        token = credentials.get("token", "")
        valid = len(token) > 10  # simplified check
        print(f"🌐 OAuth auth → {'success' if valid else 'failure'}")
        return valid


class APIKeyAuth(AuthProvider):
    def authenticate(self, **credentials) -> bool:
        key = credentials.get("api_key", "")
        valid = key.startswith("sk-")
        print(f"🗝️  API key auth → {'success' if valid else 'failure'}")
        return valid


class GoodLoginService:
    def __init__(self, auth_provider: AuthProvider):  # ← depends on abstraction
        self.auth_provider = auth_provider

    def login(self, **credentials) -> bool:
        if self.auth_provider.authenticate(**credentials):
            print("✅ User authenticated successfully.")
            return True
        print("❌ Authentication failed.")
        return False


print("\n=== Example 4: Authentication ===")
password_login = GoodLoginService(PasswordAuth())
password_login.login(username="admin", password="secret")

oauth_login = GoodLoginService(OAuthProvider())
oauth_login.login(token="ghp_abc123xyz789")

api_login = GoodLoginService(APIKeyAuth())
api_login.login(api_key="sk-live-abc123")


# ============================================================
# KEY TAKEAWAYS
# ============================================================
# 1. BAD pattern  → High-level class creates the low-level dependency
#                    inside __init__ (tight coupling).
#
# 2. GOOD pattern → High-level class *receives* an abstraction via
#                    __init__ (dependency injection + inversion).
#
# 3. Benefits:
#    • Swap implementations without modifying business logic.
#    • Unit-test with fakes/mocks — no real DB, network, or files.
#    • Follow Open/Closed Principle — extend via new classes,
#      don't modify existing ones.
