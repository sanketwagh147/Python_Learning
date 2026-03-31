"""
================================================================================
  ABSTRACT BASE CLASSES & PROTOCOLS — From Fundamentals to Production Mastery
================================================================================
  Author: Senior Software Engineer Practice Guide
  Goal:   Master ABCs for enforced interfaces, Protocols for structural subtyping,
          and know when to use each for clean plugin/adapter architecture.
================================================================================
"""

# ─────────────────────────────────────────────────────────────────────────────
# SECTION 1: UNDER THE HOOD — ABCs vs Protocols
# ─────────────────────────────────────────────────────────────────────────────
"""
TWO APPROACHES TO INTERFACES IN PYTHON:

┌──────────────────────────────────────────────────────────────────────────┐
│  ABC (Abstract Base Class)          │  Protocol (Structural Subtyping)  │
├─────────────────────────────────────┼──────────────────────────────────-─┤
│  NOMINAL typing                     │  STRUCTURAL typing                │
│  "Is-a" relationship (inheritance)  │  "Has-a" relationship (duck type) │
│  Must explicitly inherit            │  No inheritance needed            │
│  Runtime enforcement (TypeError)    │  Static checker enforcement       │
│  from abc import ABC, abstractmethod│  from typing import Protocol      │
│  Python 2.6+                        │  Python 3.8+                      │
└─────────────────────────────────────┴───────────────────────────────────-┘

ABC — Abstract Base Class:
    
    from abc import ABC, abstractmethod

    class Shape(ABC):
        @abstractmethod
        def area(self) -> float:
            ...
    
    s = Shape()  # TypeError: Can't instantiate abstract class!
    
    class Circle(Shape):
        def __init__(self, radius):
            self.radius = radius
        def area(self) -> float:
            return 3.14159 * self.radius ** 2  # Must implement!

    How it works:
    1. ABCMeta (the metaclass) tracks abstract methods in cls.__abstractmethods__
    2. type.__call__ checks __abstractmethods__ before creating an instance
    3. If any abstractmethod is not overridden → TypeError


Protocol — Structural Subtyping:

    from typing import Protocol

    class Drawable(Protocol):
        def draw(self) -> None: ...

    class Circle:  # No inheritance from Drawable!
        def draw(self) -> None:
            print("Drawing circle")

    def render(obj: Drawable) -> None:
        obj.draw()

    render(Circle())  # Works! Circle has .draw() → satisfies Protocol
    
    How it works:
    1. Protocols define a "shape" — required methods and attributes
    2. Type checkers (mypy, pyright) verify structural compatibility
    3. No runtime enforcement by default
    4. Use runtime_checkable for isinstance() checks (limited)


WHEN TO USE WHICH:

    Use ABC when:
    - You need RUNTIME enforcement (fail at instantiation, not at usage)
    - You provide shared implementation in the base class
    - You're building a plugin system where plugins MUST inherit
    - You want isinstance() checks

    Use Protocol when:
    - You want duck typing with type safety
    - You're working with third-party classes you can't modify
    - You want loose coupling (no forced inheritance hierarchy)
    - You're defining callback/handler signatures
"""

from abc import ABC, abstractmethod
from typing import Protocol, runtime_checkable, Optional, Any
from dataclasses import dataclass


# ── Proof: ABC enforcement ──────────────────────────────────────────────────

class Shape(ABC):
    """Abstract base — cannot be instantiated without implementing all methods."""

    @abstractmethod
    def area(self) -> float:
        """Calculate area."""
        ...

    @abstractmethod
    def perimeter(self) -> float:
        """Calculate perimeter."""
        ...

    def describe(self) -> str:
        """Concrete method — inherited by all subclasses (shared logic)."""
        return f"{self.__class__.__name__}: area={self.area():.2f}, perimeter={self.perimeter():.2f}"


class Circle(Shape):
    def __init__(self, radius: float):
        self.radius = radius

    def area(self) -> float:
        return 3.14159 * self.radius ** 2

    def perimeter(self) -> float:
        return 2 * 3.14159 * self.radius


# Uncomment to see enforcement:
# s = Shape()  # TypeError: Can't instantiate abstract class Shape
# class Incomplete(Shape):
#     def area(self): return 0
# i = Incomplete()  # TypeError: Can't instantiate (missing perimeter)


# ── Proof: Protocol structural subtyping ────────────────────────────────────

@runtime_checkable
class Renderable(Protocol):
    """Any object with a render() method satisfies this Protocol."""
    def render(self) -> str: ...


class HTMLWidget:
    """Satisfies Renderable WITHOUT inheriting from it."""
    def render(self) -> str:
        return "<div>Widget</div>"


class JSONSerializer:
    """Does NOT satisfy Renderable — no render() method."""
    def serialize(self) -> str:
        return "{}"


def display(obj: Renderable) -> str:
    """Type checker ensures obj has .render()."""
    return obj.render()


# Uncomment to test:
# print(display(HTMLWidget()))       # Works — has render()
# print(display(JSONSerializer()))   # Type checker error (missing render)
# print(isinstance(HTMLWidget(), Renderable))       # True (runtime_checkable)
# print(isinstance(JSONSerializer(), Renderable))   # False


# ─────────────────────────────────────────────────────────────────────────────
# SECTION 2: PRODUCTION-READY EXAMPLES
# ─────────────────────────────────────────────────────────────────────────────

# ── Example 1: Plugin Architecture with ABC ─────────────────────────────────

class NotificationChannel(ABC):
    """
    Abstract base for notification plugins.
    
    Provides:
    - Enforced interface (send, validate_config)
    - Shared retry logic (concrete method)
    - Registration pattern
    """
    _registry: dict = {}

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        if hasattr(cls, 'channel_name'):
            NotificationChannel._registry[cls.channel_name] = cls

    @abstractmethod
    def send(self, recipient: str, message: str) -> bool:
        """Send a notification. Must be implemented by plugins."""
        ...

    @abstractmethod
    def validate_config(self) -> bool:
        """Check that the channel is properly configured."""
        ...

    def send_with_retry(self, recipient: str, message: str,
                        max_retries: int = 3) -> bool:
        """Shared retry logic — all plugins get this for free."""
        for attempt in range(max_retries):
            try:
                if self.send(recipient, message):
                    return True
            except Exception as e:
                if attempt == max_retries - 1:
                    raise
        return False

    @classmethod
    def get_channel(cls, name: str) -> Optional['NotificationChannel']:
        channel_cls = cls._registry.get(name)
        return channel_cls() if channel_cls else None


class EmailChannel(NotificationChannel):
    channel_name = "email"

    def __init__(self, smtp_host: str = "smtp.example.com"):
        self.smtp_host = smtp_host

    def send(self, recipient: str, message: str) -> bool:
        # In production: use smtplib
        return True

    def validate_config(self) -> bool:
        return bool(self.smtp_host)


class SlackChannel(NotificationChannel):
    channel_name = "slack"

    def __init__(self, webhook_url: str = "https://hooks.slack.com/..."):
        self.webhook_url = webhook_url

    def send(self, recipient: str, message: str) -> bool:
        # In production: use requests
        return True

    def validate_config(self) -> bool:
        return self.webhook_url.startswith("https://")


# ── Example 2: Repository Pattern with Protocol ────────────────────────────

@dataclass
class User:
    id: int
    name: str
    email: str


class UserRepository(Protocol):
    """
    Protocol for user data access.  Any class with these methods
    satisfies the interface — no inheritance needed.
    
    This lets you:
    - Swap PostgresUserRepo for InMemoryUserRepo in tests
    - Use third-party ORMs that don't inherit from your protocol
    """

    def get_by_id(self, user_id: int) -> Optional[User]: ...
    def get_by_email(self, email: str) -> Optional[User]: ...
    def save(self, user: User) -> User: ...
    def delete(self, user_id: int) -> bool: ...


class InMemoryUserRepo:
    """Test double — satisfies UserRepository Protocol without inheriting."""

    def __init__(self):
        self._store: dict[int, User] = {}
        self._next_id = 1

    def get_by_id(self, user_id: int) -> Optional[User]:
        return self._store.get(user_id)

    def get_by_email(self, email: str) -> Optional[User]:
        for user in self._store.values():
            if user.email == email:
                return user
        return None

    def save(self, user: User) -> User:
        if user.id == 0:
            user = User(id=self._next_id, name=user.name, email=user.email)
            self._next_id += 1
        self._store[user.id] = user
        return user

    def delete(self, user_id: int) -> bool:
        return self._store.pop(user_id, None) is not None


class UserService:
    """Business logic — depends on the Protocol, not a concrete class."""

    def __init__(self, repo: UserRepository):
        self.repo = repo

    def register(self, name: str, email: str) -> User:
        existing = self.repo.get_by_email(email)
        if existing:
            raise ValueError(f"Email already registered: {email}")
        user = User(id=0, name=name, email=email)
        return self.repo.save(user)

    def get_user(self, user_id: int) -> User:
        user = self.repo.get_by_id(user_id)
        if not user:
            raise LookupError(f"User {user_id} not found")
        return user


# ── Example 3: Combining ABC + Protocol for Layered Architecture ───────────

class Serializable(Protocol):
    """Protocol: anything that can be serialized to dict."""
    def to_dict(self) -> dict: ...


class Persistable(ABC):
    """ABC: entities that know how to save/load themselves."""

    @abstractmethod
    def save(self) -> None: ...

    @abstractmethod
    def load(self, id: Any) -> 'Persistable': ...


class Cacheable(Protocol):
    """Protocol: anything with a cache key."""
    @property
    def cache_key(self) -> str: ...


def cache_and_persist(obj: Any) -> dict:
    """
    Works with any object satisfying BOTH Cacheable and Serializable.
    No forced inheritance hierarchy — pure duck typing.
    """
    data = obj.to_dict()   # Serializable
    key = obj.cache_key     # Cacheable
    # In production: redis.set(key, json.dumps(data))
    return {"cached_key": key, "data": data}


# ── Example 4: Abstract Properties and Class Methods ───────────────────────

class DataSource(ABC):
    """ABC with abstract property and classmethod."""

    @property
    @abstractmethod
    def source_type(self) -> str:
        """The type of data source (e.g., 'file', 'database', 'api')."""
        ...

    @classmethod
    @abstractmethod
    def from_config(cls, config: dict) -> 'DataSource':
        """Factory method — create from configuration."""
        ...

    @abstractmethod
    def read(self) -> list[dict]:
        """Read all data from the source."""
        ...

    def read_filtered(self, predicate) -> list[dict]:
        """Shared filtering logic."""
        return [row for row in self.read() if predicate(row)]


class CSVDataSource(DataSource):
    def __init__(self, filepath: str):
        self.filepath = filepath

    @property
    def source_type(self) -> str:
        return "csv"

    @classmethod
    def from_config(cls, config: dict) -> 'CSVDataSource':
        return cls(filepath=config["filepath"])

    def read(self) -> list[dict]:
        # In production: use csv.DictReader
        return [{"name": "Alice", "age": 30}, {"name": "Bob", "age": 25}]


# ─────────────────────────────────────────────────────────────────────────────
# SECTION 3: COMMON PITFALLS — Top 3 Bugs Juniors Introduce
# ─────────────────────────────────────────────────────────────────────────────
"""
PITFALL 1: ABC with __init__ arguments not calling super().__init__()
───────────────────────────────────────────────────────────────────────────
    class Base(ABC):
        def __init__(self, name):
            self.name = name
        @abstractmethod
        def process(self): ...
    
    class Child(Base):
        def __init__(self, name, value):
            # BUG: Missing super().__init__(name)
            self.value = value
        def process(self):
            print(self.name)  # AttributeError: 'Child' has no attribute 'name'
    
    FIX: Always call super().__init__() in subclass __init__.


PITFALL 2: Confusing runtime_checkable Protocol limitations
───────────────────────────────────────────────────────────────────────────
    @runtime_checkable
    class Sized(Protocol):
        def __len__(self) -> int: ...
    
    isinstance("hello", Sized)  # True ← string has __len__
    isinstance(42, Sized)       # False ← int has no __len__
    
    BUT: runtime_checkable only checks method EXISTENCE, not SIGNATURES!
    
    class Wrong:
        def __len__(self) -> str:   # Returns str, not int
            return "not a number"
    
    isinstance(Wrong(), Sized)  # True ← only checks if __len__ exists!
    
    FIX: runtime_checkable is a rough check. For full type safety,
         rely on static type checkers (mypy/pyright).


PITFALL 3: Abstract method in ABC not being truly abstract
───────────────────────────────────────────────────────────────────────────
    class Base(ABC):
        @abstractmethod
        def process(self):
            print("default behavior")  # This code CAN be called via super()
    
    class Child(Base):
        def process(self):
            super().process()  # ← Calls the "abstract" method's body!
            print("child behavior")
    
    This is by design — ABCs in Python CAN have body code.
    The @abstractmethod just means "must be overridden", not "has no body".
    
    GOTCHA: If you forget @abstractmethod, the method becomes concrete
    and subclasses don't need to override it — silent bug!
"""


# ─────────────────────────────────────────────────────────────────────────────
# SECTION 4: BROKEN CODE CHALLENGES — Fix These!
# ─────────────────────────────────────────────────────────────────────────────

# ── Challenge 1: Missing abstract methods not caught ────────────────────────
"""
PROBLEM: The PaymentProcessor ABC should enforce that subclasses implement
         process_payment(), refund(), and get_balance().  But the
         StripeProcessor below doesn't implement refund() and NO error
         is raised!

HINT:    - Check if @abstractmethod is applied to ALL required methods
         - One method might be missing the decorator
         - Also: ABC needs to be the base class (or use ABCMeta)
"""


class BrokenPaymentProcessor(ABC):
    @abstractmethod
    def process_payment(self, amount: float) -> bool:
        ...

    def refund(self, transaction_id: str) -> bool:
        # BUG: Missing @abstractmethod! This is a CONCRETE method
        # Subclasses aren't required to override it!
        return False

    @abstractmethod
    def get_balance(self) -> float:
        ...


class BrokenStripeProcessor(BrokenPaymentProcessor):
    def process_payment(self, amount: float) -> bool:
        return True

    def get_balance(self) -> float:
        return 1000.0

    # Missing refund() but no error because it's not abstract!


# ── Challenge 2: Protocol not checking properly at runtime ─────────────────
"""
PROBLEM: The code uses isinstance() with a Protocol but it gives False
         for objects that clearly satisfy the interface.

HINT:    - Protocol needs @runtime_checkable decorator for isinstance()
         - Without it, isinstance() always returns False
         - Also check that method names match exactly
"""


class BrokenLoggable(Protocol):
    # BUG: Missing @runtime_checkable!
    def log(self, message: str) -> None: ...
    def get_logs(self) -> list: ...


class FileLogger:
    def log(self, message: str) -> None:
        print(f"LOG: {message}")

    def get_logs(self) -> list:
        return ["log1", "log2"]


# isinstance(FileLogger(), BrokenLoggable)  # False ← should be True!


# ── Challenge 3: Diamond inheritance with ABC ──────────────────────────────
"""
PROBLEM: Multiple inheritance creates a diamond and __init__ is called
         multiple times or not at all for some parents.

HINT:    - Use super().__init__() consistently (cooperative inheritance)
         - Each __init__ should accept **kwargs and pass them through
         - Don't call parent __init__ directly (Parent.__init__(self, ...))
"""


class BrokenReader(ABC):
    def __init__(self, source: str):
        # BUG: Not using **kwargs for cooperative inheritance
        self.source = source

    @abstractmethod
    def read(self) -> str: ...


class BrokenWriter(ABC):
    def __init__(self, destination: str):
        # BUG: Not using **kwargs for cooperative inheritance
        self.destination = destination

    @abstractmethod
    def write(self, data: str) -> None: ...


class BrokenReadWriter(BrokenReader, BrokenWriter):
    def __init__(self, source: str, destination: str):
        # BUG: Which parent's __init__ runs?
        # BUG: With MRO, only BrokenReader.__init__ would be called via super()
        BrokenReader.__init__(self, source)
        BrokenWriter.__init__(self, destination)

    def read(self) -> str:
        return f"Reading from {self.source}"

    def write(self, data: str) -> None:
        print(f"Writing to {self.destination}: {data}")


# ─────────────────────────────────────────────────────────────────────────────
# SECTION 5: REFACTORING CHALLENGE
# ─────────────────────────────────────────────────────────────────────────────
"""
REFACTORING CHALLENGE: Messy Payment System
─────────────────────────────────────────────

Refactor to use:
    1. An ABC for PaymentGateway with enforced interface
    2. A Protocol for Auditable (anything with audit_trail())
    3. Proper separation — no if/elif chains for gateway type
    4. Each gateway as a separate class
    5. Easy to add a new gateway without modifying existing code
"""


class MessyPaymentSystem:
    """Refactor me using ABCs and Protocols!"""

    def process(self, gateway_type: str, amount: float,
                currency: str = "USD") -> dict:
        if gateway_type == "stripe":
            # Stripe-specific logic
            fee = amount * 0.029 + 0.30
            net = amount - fee
            return {
                "gateway": "stripe",
                "amount": amount,
                "fee": round(fee, 2),
                "net": round(net, 2),
                "currency": currency,
            }
        elif gateway_type == "paypal":
            # PayPal-specific logic
            fee = amount * 0.0349 + 0.49
            net = amount - fee
            return {
                "gateway": "paypal",
                "amount": amount,
                "fee": round(fee, 2),
                "net": round(net, 2),
                "currency": currency,
            }
        elif gateway_type == "razorpay":
            # Razorpay-specific logic
            fee = amount * 0.02
            net = amount - fee
            return {
                "gateway": "razorpay",
                "amount": amount,
                "fee": round(fee, 2),
                "net": round(net, 2),
                "currency": currency,
            }
        else:
            raise ValueError(f"Unknown gateway: {gateway_type}")

    def refund(self, gateway_type: str, transaction_id: str,
               amount: float) -> dict:
        if gateway_type == "stripe":
            return {"refunded": True, "gateway": "stripe", "amount": amount}
        elif gateway_type == "paypal":
            return {"refunded": True, "gateway": "paypal", "amount": amount}
        elif gateway_type == "razorpay":
            return {"refunded": True, "gateway": "razorpay", "amount": amount}
        else:
            raise ValueError(f"Unknown gateway: {gateway_type}")


# ─────────────────────────────────────────────────────────────────────────────
# QUICK SELF-TEST
# ─────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("=" * 60)
    print("  11_abc_protocols.py — Self Test")
    print("=" * 60)

    # Test ABC enforcement
    print("\n[Test] ABC enforcement:")
    try:
        Shape()
    except TypeError as e:
        print(f"  Shape() → TypeError: {e}")
    c = Circle(5.0)
    print(f"  Circle(5): {c.describe()}")

    # Test Protocol with runtime_checkable
    print("\n[Test] Protocol (runtime_checkable):")
    assert isinstance(HTMLWidget(), Renderable)
    assert not isinstance(JSONSerializer(), Renderable)
    print(f"  HTMLWidget is Renderable: {isinstance(HTMLWidget(), Renderable)}")
    print(f"  JSONSerializer is Renderable: {isinstance(JSONSerializer(), Renderable)}")

    # Test plugin system
    print("\n[Test] NotificationChannel plugin system:")
    channels = NotificationChannel._registry
    print(f"  Registered: {list(channels.keys())}")
    email = NotificationChannel.get_channel("email")
    assert email is not None
    assert email.validate_config()
    print(f"  Email send: {email.send('test@test.com', 'Hello')}")

    # Test Repository pattern
    print("\n[Test] Repository Pattern (Protocol):")
    repo = InMemoryUserRepo()
    service = UserService(repo)
    user = service.register("Sanket", "sanket@test.com")
    assert user.id == 1
    assert user.name == "Sanket"
    found = service.get_user(1)
    assert found.email == "sanket@test.com"
    print(f"  Registered: {user}")
    print(f"  Retrieved: {found}")

    # Test duplicate check
    try:
        service.register("Other", "sanket@test.com")
    except ValueError as e:
        print(f"  Duplicate caught: {e}")

    # Test DataSource (abstract property + classmethod)
    print("\n[Test] DataSource (abstract property):")
    csv_src = CSVDataSource.from_config({"filepath": "data.csv"})
    assert csv_src.source_type == "csv"
    data = csv_src.read()
    young = csv_src.read_filtered(lambda r: r["age"] < 30)
    print(f"  Source type: {csv_src.source_type}")
    print(f"  All data: {len(data)} rows, filtered: {len(young)} rows")

    print("\n✓ All ABC/Protocol tests passed!")
    print("=" * 60)
