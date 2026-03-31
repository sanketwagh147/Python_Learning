"""
================================================================================
  DATACLASSES, __slots__, & MEMORY — From Fundamentals to Production Mastery
================================================================================
  Author: Senior Software Engineer Practice Guide
  Goal:   Master dataclasses, __slots__, memory optimization, frozen instances,
          __post_init__, and when to use each approach.
================================================================================
"""

# ─────────────────────────────────────────────────────────────────────────────
# SECTION 1: UNDER THE HOOD — How Dataclasses & __slots__ Work
# ─────────────────────────────────────────────────────────────────────────────
"""
DATACLASSES (Python 3.7+):

    @dataclass is a CLASS DECORATOR that auto-generates boilerplate methods
    based on class-level type annotations.

    @dataclass
    class Point:
        x: float
        y: float

    Python generates:
        __init__(self, x: float, y: float)
        __repr__(self)  → "Point(x=1.0, y=2.0)"
        __eq__(self, other) → compares all fields

    Optional generation (via decorator args):
        @dataclass(order=True)    → __lt__, __le__, __gt__, __ge__
        @dataclass(frozen=True)   → __setattr__, __delattr__ raise FrozenError
        @dataclass(slots=True)    → auto __slots__ (Python 3.10+)
        @dataclass(kw_only=True)  → all fields keyword-only (Python 3.10+)

    KEY INSIGHT: dataclass does NOT change how Python creates instances.
    It's purely a code generator — inspect the generated __init__:
        import inspect
        print(inspect.getsource(Point.__init__))  # auto-generated code!


__slots__:

    By default, Python objects store attributes in a DICT (self.__dict__).
    Dicts are flexible but memory-heavy (~100-200 bytes overhead per instance).

    __slots__ tells Python to use a FIXED STRUCT instead of a dict:
    
    class Point:
        __slots__ = ('x', 'y')
        def __init__(self, x, y):
            self.x = x
            self.y = y

    Effects:
    ┌──────────────────────────┬──────────────┬──────────────┐
    │  Feature                 │  __dict__    │  __slots__   │
    ├──────────────────────────┼──────────────┼──────────────┤
    │  Memory per instance     │  ~200 bytes  │  ~56 bytes   │
    │  Attribute access speed  │  dict lookup │  direct offset│
    │  Dynamic attribute add   │  ✓ Yes       │  ✗ No        │
    │  __dict__ available      │  ✓ Yes       │  ✗ No        │
    │  Can be pickled          │  ✓ Yes       │  ✓ (careful) │
    │  Can use __weakref__     │  ✓ Yes       │  Only if listed│
    └──────────────────────────┴──────────────┴──────────────┘

    Under the hood: __slots__ creates DESCRIPTORS on the class for each name.
    These descriptors use a fixed offset into the instance's memory layout.

    When to use __slots__:
    - Creating millions of instances (huge memory savings)
    - Performance-critical inner loops
    - When you want to prevent typos (no accidental new attributes)
    
    When NOT to use __slots__:
    - Need dynamic attributes
    - Multiple inheritance with conflicting slots
    - Prototyping / scripts
"""

from dataclasses import dataclass, field, asdict, astuple, replace, fields
from dataclasses import FrozenInstanceError
import sys


# ── Proof: Memory comparison ────────────────────────────────────────────────

class PointDict:
    """Regular class — uses __dict__."""
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y


class PointSlots:
    """Slots class — fixed memory layout."""
    __slots__ = ('x', 'y')
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y


@dataclass
class PointDataclass:
    """Dataclass — uses __dict__ by default."""
    x: float
    y: float


@dataclass(slots=True)  # Python 3.10+
class PointDataclassSlots:
    """Dataclass with slots — best of both worlds."""
    x: float
    y: float


def compare_memory():
    """Compare memory usage of different approaches."""
    dict_obj = PointDict(1.0, 2.0)
    slots_obj = PointSlots(1.0, 2.0)
    dc_obj = PointDataclass(1.0, 2.0)
    dc_slots_obj = PointDataclassSlots(1.0, 2.0)

    return {
        "PointDict": sys.getsizeof(dict_obj) + sys.getsizeof(dict_obj.__dict__),
        "PointSlots": sys.getsizeof(slots_obj),
        "PointDataclass": sys.getsizeof(dc_obj) + sys.getsizeof(dc_obj.__dict__),
        "PointDataclassSlots": sys.getsizeof(dc_slots_obj),
    }


# ─────────────────────────────────────────────────────────────────────────────
# SECTION 2: PRODUCTION-READY EXAMPLES
# ─────────────────────────────────────────────────────────────────────────────

# ── Example 1: Immutable Configuration (frozen dataclass) ──────────────────

from typing import Optional
from datetime import datetime


@dataclass(frozen=True)
class AppConfig:
    """
    Immutable configuration object.
    
    frozen=True means:
    - Cannot modify fields after creation → no accidental mutation
    - Hashable → can be used as dict key or in sets
    - Thread-safe by default (no shared mutable state)
    """
    database_url: str
    redis_url: str = "redis://localhost:6379"
    max_connections: int = 10
    debug: bool = False
    api_keys: tuple = ()  # use tuple, not list (must be hashable for frozen)

    def with_overrides(self, **kwargs) -> 'AppConfig':
        """Create a new config with some fields overridden (immutable update)."""
        return replace(self, **kwargs)


# Usage:
# config = AppConfig(database_url="postgresql://localhost/mydb", debug=True)
# prod_config = config.with_overrides(debug=False, max_connections=50)
# config.debug = True   # FrozenInstanceError!


# ── Example 2: Domain Model with validation (__post_init__) ────────────────

@dataclass
class Order:
    """
    Production domain model with validation, computed fields, and factories.
    
    __post_init__ runs AFTER __init__ — perfect for:
    - Validation
    - Computed/derived fields
    - Transformations (e.g., normalizing strings)
    """
    order_id: str
    customer_email: str
    items: list = field(default_factory=list)
    status: str = "pending"
    created_at: datetime = field(default_factory=datetime.now)
    total: float = field(init=False)  # computed, not in __init__
    _validated: bool = field(init=False, repr=False, compare=False)

    def __post_init__(self):
        # Normalize
        self.customer_email = self.customer_email.strip().lower()

        # Validate
        if not self.order_id:
            raise ValueError("order_id is required")
        if '@' not in self.customer_email:
            raise ValueError(f"Invalid email: {self.customer_email}")
        if self.status not in ("pending", "confirmed", "shipped", "delivered", "cancelled"):
            raise ValueError(f"Invalid status: {self.status}")

        # Compute
        self.total = sum(item.get("price", 0) * item.get("qty", 1) for item in self.items)
        self._validated = True

    @classmethod
    def from_dict(cls, data: dict) -> 'Order':
        """Factory method — create from API response or DB row."""
        return cls(
            order_id=data["id"],
            customer_email=data["email"],
            items=data.get("items", []),
            status=data.get("status", "pending"),
        )

    def to_dict(self) -> dict:
        """Serialize to dict (e.g., for JSON response)."""
        d = asdict(self)
        d.pop('_validated', None)
        d['created_at'] = self.created_at.isoformat()
        return d


# ── Example 3: High-Performance Data Container with __slots__ ──────────────

@dataclass(slots=True, frozen=True)
class StockTick:
    """
    Represents a single stock price tick.  Millions of these in memory.
    
    slots=True + frozen=True:
    - Minimal memory (~56 bytes per instance)
    - Immutable → safe for concurrent reads
    - Hashable → can be in sets, used as dict keys
    """
    symbol: str
    price: float
    volume: int
    timestamp: float  # Unix timestamp

    @property
    def value(self) -> float:
        """Dollar volume of this tick."""
        return self.price * self.volume


# ── Example 4: Field customization patterns ────────────────────────────────

@dataclass
class APIResponse:
    """Shows all field() options in action."""
    status_code: int
    data: dict = field(default_factory=dict)              # mutable default
    headers: dict = field(default_factory=dict, repr=False)  # hidden from repr
    _raw_bytes: bytes = field(default=b'', compare=False)    # excluded from ==
    request_id: str = field(default='', hash=False)          # excluded from hash
    metadata: dict = field(
        default_factory=dict,
        metadata={"description": "Extra context", "max_size": 1024}
    )

    # Access metadata at runtime:
    # fields(APIResponse)[5].metadata  → {"description": "Extra context", ...}


# ── Example 5: Inheritance with dataclasses ─────────────────────────────────

@dataclass
class BaseEvent:
    event_type: str
    timestamp: datetime = field(default_factory=datetime.now)
    source: str = "system"


@dataclass
class UserEvent(BaseEvent):
    user_id: int = 0
    action: str = ""


@dataclass
class PaymentEvent(BaseEvent):
    amount: float = 0.0
    currency: str = "USD"
    user_id: int = 0


# ─────────────────────────────────────────────────────────────────────────────
# SECTION 3: COMMON PITFALLS — Top 3 Bugs Juniors Introduce
# ─────────────────────────────────────────────────────────────────────────────
"""
PITFALL 1: Mutable default arguments
───────────────────────────────────────────────────────────────────────────
    @dataclass
    class Bad:
        items: list = []   # ValueError! Python catches this for dataclasses!
    
    BUT not in regular classes:
    class AlsoBad:
        def __init__(self, items=[]):  # ← shared mutable default!
            self.items = items
    
    FIX FOR DATACLASSES: field(default_factory=list)
    FIX FOR CLASSES: def __init__(self, items=None): self.items = items or []


PITFALL 2: __slots__ + inheritance gotchas
───────────────────────────────────────────────────────────────────────────
    class Parent:
        __slots__ = ('x',)
    
    class Child(Parent):
        __slots__ = ('x', 'y')  # BUG: 'x' in both → no error, but wastes memory
    
    FIX: Only add NEW slots in the child:
        class Child(Parent):
            __slots__ = ('y',)  # 'x' inherited from Parent


PITFALL 3: frozen dataclass with mutable fields
───────────────────────────────────────────────────────────────────────────
    @dataclass(frozen=True)
    class Config:
        values: list = field(default_factory=list)
    
    c = Config(values=[1, 2, 3])
    c.values.append(4)   # Works! Frozen only prevents REBINDING, not mutation!
    
    FIX: Use immutable types (tuple, frozenset) for frozen dataclasses:
        values: tuple = ()
    
    OR: Deep-freeze in __post_init__ (use object.__setattr__ for frozen):
        def __post_init__(self):
            object.__setattr__(self, 'values', tuple(self.values))
"""


# ─────────────────────────────────────────────────────────────────────────────
# SECTION 4: BROKEN CODE CHALLENGES — Fix These!
# ─────────────────────────────────────────────────────────────────────────────

# ── Challenge 1: Mutable default shared between instances ───────────────────
"""
PROBLEM: All instances share the same tags list!
         Adding a tag to one user adds it to ALL users.

HINT:    - The default list is shared (regular class, not dataclass)
         - Dataclass would catch this, but regular class doesn't
         - Fix with None default + create new list in __init__
"""


class BrokenUser:
    def __init__(self, name: str, tags: list = []):
        self.name = name
        self.tags = tags  # BUG: shared mutable default!

    def add_tag(self, tag: str):
        self.tags.append(tag)


# u1 = BrokenUser("Alice")
# u2 = BrokenUser("Bob")
# u1.add_tag("admin")
# print(u2.tags)  # ["admin"] ← WRONG! Bob shouldn't be admin!


# ── Challenge 2: Frozen dataclass with mutable internals ───────────────────
"""
PROBLEM: This "frozen" config can still be mutated through its list/dict fields.
         Someone can do config.allowed_hosts.append("evil.com").

HINT:    - frozen=True only prevents attribute REBINDING, not internal mutation
         - Convert mutable types to immutable in __post_init__
         - Must use object.__setattr__ since it's frozen
"""


@dataclass(frozen=True)
class BrokenFrozenConfig:
    name: str
    allowed_hosts: list = field(default_factory=list)
    settings: dict = field(default_factory=dict)

    # BUG: No __post_init__ to freeze mutable fields!
    # c = BrokenFrozenConfig("prod", ["safe.com"], {"debug": False})
    # c.allowed_hosts.append("evil.com")  # Works! Not truly frozen!


# ── Challenge 3: __slots__ breaking pickle/copy ────────────────────────────
"""
PROBLEM: This slots class can't be pickled or deep-copied because
         it's missing __getstate__ and __setstate__.

HINT:    - Slots classes don't have __dict__ by default
         - pickle needs to know how to serialize/deserialize
         - Implement __getstate__ returning a dict of slot values
         - Implement __setstate__ restoring them
"""

import pickle
import copy


class BrokenSerializablePoint:
    __slots__ = ('x', 'y', 'label')

    def __init__(self, x: float, y: float, label: str = ""):
        self.x = x
        self.y = y
        self.label = label

    # BUG: Missing __getstate__ and __setstate__ for pickle support
    # p = BrokenSerializablePoint(1.0, 2.0, "origin")
    # pickled = pickle.dumps(p)    # May fail or lose data
    # copied = copy.deepcopy(p)    # May fail


# ─────────────────────────────────────────────────────────────────────────────
# SECTION 5: REFACTORING CHALLENGE
# ─────────────────────────────────────────────────────────────────────────────
"""
REFACTORING CHALLENGE: Messy Product Catalog Class
────────────────────────────────────────────────────

Refactor this verbose class into:
    1. A @dataclass with proper field() definitions
    2. Validation in __post_init__
    3. frozen=True for immutability
    4. Computed fields (init=False)
    5. Factory class method for creating from API responses
    6. Proper comparison support (order=True based on price)
"""


class MessyProduct:
    """Refactor me into a clean dataclass!"""

    def __init__(self, product_id, name, price, category, stock=0,
                 discount=0.0, tags=None, created_at=None):
        if not product_id:
            raise ValueError("product_id required")
        self.product_id = product_id

        if not isinstance(name, str) or len(name) < 1:
            raise ValueError("name must be a non-empty string")
        self.name = name

        if not isinstance(price, (int, float)) or price < 0:
            raise ValueError("price must be a positive number")
        self.price = float(price)

        self.category = category
        self.stock = stock

        if not 0 <= discount <= 1:
            raise ValueError("discount must be between 0 and 1")
        self.discount = discount

        self.tags = tags if tags is not None else []

        if created_at is None:
            self.created_at = datetime.now()
        else:
            self.created_at = created_at

        self.final_price = self.price * (1 - self.discount)
        self.in_stock = self.stock > 0

    def __repr__(self):
        return (f"MessyProduct(id={self.product_id}, name={self.name!r}, "
                f"price={self.price}, final_price={self.final_price})")

    def __eq__(self, other):
        if not isinstance(other, MessyProduct):
            return NotImplemented
        return self.product_id == other.product_id

    def __lt__(self, other):
        if not isinstance(other, MessyProduct):
            return NotImplemented
        return self.final_price < other.final_price

    def __le__(self, other):
        if not isinstance(other, MessyProduct):
            return NotImplemented
        return self.final_price <= other.final_price

    def __gt__(self, other):
        if not isinstance(other, MessyProduct):
            return NotImplemented
        return self.final_price > other.final_price

    def __ge__(self, other):
        if not isinstance(other, MessyProduct):
            return NotImplemented
        return self.final_price >= other.final_price

    def __hash__(self):
        return hash(self.product_id)


# ─────────────────────────────────────────────────────────────────────────────
# QUICK SELF-TEST
# ─────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("=" * 60)
    print("  10_dataclasses_slots.py — Self Test")
    print("=" * 60)

    # Test memory comparison
    print("\n[Test] Memory comparison:")
    mem = compare_memory()
    for name, size in mem.items():
        print(f"  {name}: ~{size} bytes")

    # Test frozen config
    print("\n[Test] Frozen AppConfig:")
    config = AppConfig(database_url="postgresql://localhost/db", debug=True)
    prod = config.with_overrides(debug=False, max_connections=50)
    assert config.debug is True
    assert prod.debug is False
    try:
        config.debug = False
    except FrozenInstanceError:
        print(f"  FrozenInstanceError raised ✓")
    print(f"  Config: {config}")
    print(f"  Prod:   {prod}")

    # Test Order with __post_init__
    print("\n[Test] Order with __post_init__:")
    order = Order(
        order_id="ORD-001",
        customer_email="  Sanket@Test.COM  ",
        items=[{"name": "Widget", "price": 29.99, "qty": 2}],
    )
    assert order.customer_email == "sanket@test.com"  # normalized
    assert order.total == 59.98  # computed
    print(f"  Order: {order}")
    print(f"  Total (computed): {order.total}")

    # Test Order validation
    try:
        Order(order_id="", customer_email="bad")
    except ValueError as e:
        print(f"  Validation caught: {e}")

    # Test StockTick (slots + frozen)
    print("\n[Test] StockTick (slots + frozen):")
    tick = StockTick("AAPL", 150.0, 1000, 1648000000.0)
    assert tick.value == 150000.0
    print(f"  {tick}, value=${tick.value:,.0f}")

    # Test field metadata
    print("\n[Test] Field metadata:")
    meta = fields(APIResponse)[5].metadata
    assert meta["description"] == "Extra context"
    print(f"  APIResponse.metadata field info: {meta}")

    # Test inheritance
    print("\n[Test] Dataclass inheritance:")
    ue = UserEvent(event_type="login", user_id=42, action="login")
    pe = PaymentEvent(event_type="charge", amount=99.99, user_id=42)
    print(f"  UserEvent: {ue}")
    print(f"  PaymentEvent: {pe}")

    print("\n✓ All dataclass/slots tests passed!")
    print("=" * 60)
