"""
================================================================================
  MAGIC METHODS (DUNDER METHODS) — Deep Dive for Production Mastery
================================================================================
  Author: Senior Software Engineer Practice Guide
  Goal:   Master __hash__, __eq__, __repr__, operator overloading, and make
          custom objects behave like built-in Python types.
================================================================================
"""

# ─────────────────────────────────────────────────────────────────────────────
# SECTION 1: UNDER THE HOOD — The Dunder Method Dispatch System
# ─────────────────────────────────────────────────────────────────────────────
"""
Magic methods (dunder methods) are Python's operator overloading system.
When you write `a + b`, Python ACTUALLY calls `a.__add__(b)`.

The dispatch order for binary operations:

    a + b  →  type(a).__add__(a, b)
               if returns NotImplemented →  type(b).__radd__(b, a)
               if also NotImplemented   →  TypeError

    This is why __radd__ exists — it lets the RIGHT operand handle the op.


CRITICAL RELATIONSHIPS:

    ┌──────────────────────────────────────────────────────────────────┐
    │  __eq__ and __hash__                                             │
    │                                                                  │
    │  RULE: If you override __eq__, Python sets __hash__ = None       │
    │        (makes instances unhashable: can't be in sets/dict keys!) │
    │                                                                  │
    │  FIX: If a == b, then hash(a) MUST equal hash(b)                │
    │       (but hash(a) == hash(b) does NOT mean a == b)             │
    │                                                                  │
    │  If you override __eq__, you MUST also override __hash__        │
    │  (unless you intentionally want unhashable objects)              │
    └──────────────────────────────────────────────────────────────────┘

    ┌──────────────────────────────────────────────────────────────────┐
    │  __repr__ vs __str__                                             │
    │                                                                  │
    │  __repr__: For developers. Should ideally be eval-able:          │
    │            eval(repr(obj)) == obj                                │
    │            Used in: debugger, REPL, containers (lists, dicts)    │
    │                                                                  │
    │  __str__:  For end users. Human-readable.                        │
    │            Used in: print(), str(), f-strings                    │
    │                                                                  │
    │  If only __repr__ is defined, str() falls back to __repr__      │
    │  If only __str__ is defined, repr() does NOT fall back to __str__│
    │                                                                  │
    │  RULE: Always implement __repr__. Implement __str__ only if      │
    │        you need a different user-facing representation.          │
    └──────────────────────────────────────────────────────────────────┘


FULL DUNDER METHOD CHEAT SHEET:

    Object lifecycle:    __new__, __init__, __del__
    String:              __repr__, __str__, __format__, __bytes__
    Comparison:          __eq__, __ne__, __lt__, __le__, __gt__, __ge__
    Hashing:             __hash__
    Boolean:             __bool__, __len__
    Arithmetic:          __add__, __sub__, __mul__, __truediv__, __mod__,
                         __pow__, __floordiv__
    Reflected:           __radd__, __rsub__, etc.
    In-place:            __iadd__, __isub__, etc.
    Unary:               __neg__, __pos__, __abs__, __invert__
    Container:           __len__, __getitem__, __setitem__, __delitem__,
                         __contains__, __iter__, __reversed__
    Attribute:           __getattr__, __setattr__, __delattr__, __getattribute__
    Callable:            __call__
    Context manager:     __enter__, __exit__
    Descriptor:          __get__, __set__, __delete__, __set_name__
"""


# ─────────────────────────────────────────────────────────────────────────────
# SECTION 2: PRODUCTION-READY EXAMPLES
# ─────────────────────────────────────────────────────────────────────────────

# ── Example 1: Money Type (correct equality, hashing, arithmetic) ──────────

from functools import total_ordering


@total_ordering
class Money:
    """
    Production-ready Money type with:
    - Currency-safe arithmetic (can't add USD + EUR)
    - Proper equality and hashing (usable in sets and as dict keys)
    - Operator overloading (+, -, *, comparison)
    - Human-readable AND developer-readable representations
    """

    __slots__ = ('_amount', '_currency')

    def __init__(self, amount: float, currency: str = "USD"):
        # Store as integer cents to avoid floating point issues
        self._amount = round(amount * 100)
        self._currency = currency.upper()

    @property
    def amount(self) -> float:
        return self._amount / 100

    @property
    def currency(self) -> str:
        return self._currency

    # ── String representation ──

    def __repr__(self) -> str:
        """Developer representation — should be eval-able."""
        return f"Money({self.amount}, '{self._currency}')"

    def __str__(self) -> str:
        """User-facing representation."""
        symbols = {"USD": "$", "EUR": "€", "GBP": "£", "INR": "₹", "JPY": "¥"}
        sym = symbols.get(self._currency, self._currency + " ")
        return f"{sym}{self.amount:,.2f}"

    def __format__(self, spec: str) -> str:
        """Support f-string formatting: f'{money:.0f}' or f'{money:>15}'."""
        if spec:
            formatted = format(self.amount, spec)
            return f"{self._currency} {formatted}"
        return str(self)

    # ── Equality and Hashing ──

    def __eq__(self, other) -> bool:
        if not isinstance(other, Money):
            return NotImplemented
        return self._amount == other._amount and self._currency == other._currency

    def __hash__(self) -> int:
        """Must be consistent with __eq__: a == b → hash(a) == hash(b)."""
        return hash((self._amount, self._currency))

    def __lt__(self, other) -> bool:
        """Only compare same currency."""
        if not isinstance(other, Money):
            return NotImplemented
        if self._currency != other._currency:
            raise ValueError(f"Cannot compare {self._currency} with {other._currency}")
        return self._amount < other._amount

    # ── Arithmetic ──

    def _check_currency(self, other: 'Money'):
        if self._currency != other._currency:
            raise ValueError(f"Cannot mix {self._currency} and {other._currency}")

    def __add__(self, other):
        if isinstance(other, Money):
            self._check_currency(other)
            return Money((self._amount + other._amount) / 100, self._currency)
        return NotImplemented

    def __radd__(self, other):
        """Allows sum() to work: sum(money_list) starts with 0 + first_item."""
        if other == 0:
            return self
        return self.__add__(other)

    def __sub__(self, other):
        if isinstance(other, Money):
            self._check_currency(other)
            return Money((self._amount - other._amount) / 100, self._currency)
        return NotImplemented

    def __mul__(self, other):
        if isinstance(other, (int, float)):
            return Money((self._amount * other) / 100, self._currency)
        return NotImplemented

    def __rmul__(self, other):
        return self.__mul__(other)

    def __neg__(self):
        return Money(-self._amount / 100, self._currency)

    def __abs__(self):
        return Money(abs(self._amount) / 100, self._currency)

    def __bool__(self) -> bool:
        """Money is truthy if non-zero."""
        return self._amount != 0


# ── Example 2: Custom Container (dict-like with dot access) ────────────────

class AttrDict:
    """
    Dictionary that supports dot-notation access.
    Demonstrates __getattr__, __setattr__, __getitem__, __setitem__,
    __contains__, __len__, __iter__, __repr__.
    
    Used in: configuration objects, API response wrappers, template engines.
    """

    def __init__(self, data: dict = None, **kwargs):
        # Use object.__setattr__ to avoid triggering our custom __setattr__
        object.__setattr__(self, '_data', {})
        if data:
            self._data.update(data)
        self._data.update(kwargs)

    # ── Dict-style access ──

    def __getitem__(self, key):
        try:
            value = self._data[key]
        except KeyError:
            raise KeyError(key)
        return AttrDict(value) if isinstance(value, dict) else value

    def __setitem__(self, key, value):
        self._data[key] = value

    def __delitem__(self, key):
        del self._data[key]

    def __contains__(self, key):
        return key in self._data

    def __len__(self):
        return len(self._data)

    def __iter__(self):
        return iter(self._data)

    # ── Dot-notation access ──

    def __getattr__(self, name):
        """Called when normal attribute lookup fails."""
        if name.startswith('_'):
            raise AttributeError(name)
        try:
            return self[name]
        except KeyError:
            raise AttributeError(f"No attribute '{name}'")

    def __setattr__(self, name, value):
        """Route dot-notation assignments to the internal dict."""
        if name.startswith('_'):
            object.__setattr__(self, name, value)
        else:
            self._data[name] = value

    # ── String representation ──

    def __repr__(self):
        return f"AttrDict({self._data!r})"

    def __str__(self):
        return str(self._data)

    # ── Equality ──

    def __eq__(self, other):
        if isinstance(other, AttrDict):
            return self._data == other._data
        if isinstance(other, dict):
            return self._data == other
        return NotImplemented

    def to_dict(self) -> dict:
        return dict(self._data)


# ── Example 3: Callable objects with __call__ ──────────────────────────────

class Validator:
    """
    Callable validator — use like a function but with configuration.
    
    v = Validator(min_val=0, max_val=100)
    v(42)    # True
    v(-1)    # raises ValueError
    """

    def __init__(self, *, min_val=None, max_val=None,
                 expected_type=None, predicate=None, error_msg=None):
        self.min_val = min_val
        self.max_val = max_val
        self.expected_type = expected_type
        self.predicate = predicate
        self.error_msg = error_msg or "Validation failed"

    def __call__(self, value) -> bool:
        """Makes instances callable: validator(value)."""
        if self.expected_type and not isinstance(value, self.expected_type):
            raise TypeError(f"Expected {self.expected_type.__name__}, got {type(value).__name__}")
        if self.min_val is not None and value < self.min_val:
            raise ValueError(f"{self.error_msg}: {value} < {self.min_val}")
        if self.max_val is not None and value > self.max_val:
            raise ValueError(f"{self.error_msg}: {value} > {self.max_val}")
        if self.predicate and not self.predicate(value):
            raise ValueError(f"{self.error_msg}: predicate failed for {value}")
        return True

    def __repr__(self):
        parts = []
        if self.expected_type:
            parts.append(f"type={self.expected_type.__name__}")
        if self.min_val is not None:
            parts.append(f"min={self.min_val}")
        if self.max_val is not None:
            parts.append(f"max={self.max_val}")
        return f"Validator({', '.join(parts)})"

    def __and__(self, other: 'Validator') -> 'Validator':
        """Compose validators: combined = v1 & v2."""
        def combined_predicate(value):
            self(value)
            other(value)
            return True
        return Validator(predicate=combined_predicate,
                        error_msg=f"({self.error_msg}) AND ({other.error_msg})")


# Usage:
# validate_age = Validator(min_val=0, max_val=150, expected_type=int,
#                          error_msg="Invalid age")
# validate_age(25)    # True
# validate_age(-1)    # ValueError: Invalid age: -1 < 0


# ── Example 4: Context-aware __getattr__ for API clients ───────────────────

class APIClient:
    """
    Fluent API client using __getattr__ for URL building.
    
    client = APIClient("https://api.example.com")
    client.users.list()        → GET /users
    client.users[42].get()     → GET /users/42
    client.posts.create(data)  → POST /posts
    """

    def __init__(self, base_url: str, path_parts: list = None):
        self._base_url = base_url.rstrip('/')
        self._parts = path_parts or []

    def __getattr__(self, name):
        """Build URL incrementally: client.users → client with /users."""
        if name.startswith('_'):
            raise AttributeError(name)
        return APIClient(self._base_url, self._parts + [name])

    def __getitem__(self, key):
        """Support subscript: client.users[42] → /users/42."""
        return APIClient(self._base_url, self._parts + [str(key)])

    @property
    def url(self) -> str:
        return f"{self._base_url}/{'/'.join(self._parts)}"

    def get(self, **params) -> dict:
        return {"method": "GET", "url": self.url, "params": params}

    def post(self, data: dict = None) -> dict:
        return {"method": "POST", "url": self.url, "data": data}

    def __repr__(self):
        return f"APIClient(url='{self.url}')"


# ─────────────────────────────────────────────────────────────────────────────
# SECTION 3: COMMON PITFALLS — Top 3 Bugs Juniors Introduce
# ─────────────────────────────────────────────────────────────────────────────
"""
PITFALL 1: Overriding __eq__ without __hash__
───────────────────────────────────────────────────────────────────────────
    class Point:
        def __init__(self, x, y):
            self.x, self.y = x, y
        def __eq__(self, other):
            return self.x == other.x and self.y == other.y
    
    {Point(1,2)}           # TypeError: unhashable type: 'Point'
    {Point(1,2): "value"}  # TypeError!
    
    WHY: Python sets __hash__ = None when you define __eq__.
    
    FIX: Implement __hash__:
        def __hash__(self):
            return hash((self.x, self.y))
    
    RULE: If a == b, then hash(a) MUST == hash(b).
          Hash the same fields used in __eq__.


PITFALL 2: __repr__ that crashes on edge cases
───────────────────────────────────────────────────────────────────────────
    class TreeNode:
        def __init__(self, value, children=None):
            self.value = value
            self.children = children or []
        def __repr__(self):
            return f"TreeNode({self.value}, {self.children})"
    
    # Self-referencing: node.children.append(node) → infinite recursion!
    
    FIX: Limit recursion depth or use id() for cycles:
        def __repr__(self):
            child_ids = [id(c) for c in self.children]
            return f"TreeNode({self.value}, children={child_ids})"


PITFALL 3: Forgetting NotImplemented in operator overloading
───────────────────────────────────────────────────────────────────────────
    class Vector:
        def __add__(self, other):
            if not isinstance(other, Vector):
                raise TypeError("Can only add Vectors")  # TOO AGGRESSIVE!
    
    PROBLEM: This prevents other types from handling the operation.
    
    FIX: Return NotImplemented (NOT raise NotImplementedError):
        def __add__(self, other):
            if not isinstance(other, Vector):
                return NotImplemented  # Python will try other.__radd__(self)
            return Vector(self.x + other.x, self.y + other.y)
    
    NotImplemented vs NotImplementedError:
    - NotImplemented: a SENTINEL VALUE returned from __add__ etc.
      → tells Python "try the other operand's reflected method"
    - NotImplementedError: an EXCEPTION raised in abstract methods
      → means "this method isn't implemented yet"
"""


# ─────────────────────────────────────────────────────────────────────────────
# SECTION 4: BROKEN CODE CHALLENGES — Fix These!
# ─────────────────────────────────────────────────────────────────────────────

# ── Challenge 1: Broken equality and hashing ────────────────────────────────
"""
PROBLEM: This Point class can't be used in sets or as dict keys, and
         two Points with same coordinates aren't equal.

HINT:    - __eq__ is defined but uses wrong comparison
         - __hash__ is missing entirely
         - Also: __eq__ should handle non-Point comparisons gracefully
"""


class BrokenPoint:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def __eq__(self, other):
        # BUG 1: No type check → crashes if other is not a Point
        # BUG 2: Using `is` instead of `==` (identity vs equality)
        return self.x is other.x and self.y is other.y

    # BUG 3: Missing __hash__!  Can't use in sets/dicts.

    def __repr__(self):
        return f"Point({self.x}, {self.y})"


# p1 = BrokenPoint(1.0, 2.0)
# p2 = BrokenPoint(1.0, 2.0)
# print(p1 == p2)        # Might be False (identity check, not value)
# {p1, p2}               # TypeError: unhashable type


# ── Challenge 2: Operator overloading without reflected methods ─────────────
"""
PROBLEM: The Vector class works for Vector + Vector but fails for:
         - 3 * vector  (int * Vector)
         - sum([v1, v2, v3])  (starts with 0 + v1)

HINT:    - __rmul__ handles: 3 * vector (when int.__mul__ fails)
         - __radd__ handles: 0 + vector (for sum() to work)
         - Return NotImplemented for unsupported types
"""


class BrokenVector:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def __add__(self, other):
        if isinstance(other, BrokenVector):
            return BrokenVector(self.x + other.x, self.y + other.y)
        raise TypeError(f"Cannot add Vector and {type(other)}")  # BUG: too aggressive

    def __mul__(self, scalar):
        if isinstance(scalar, (int, float)):
            return BrokenVector(self.x * scalar, self.y * scalar)
        raise TypeError(f"Cannot multiply Vector by {type(scalar)}")  # BUG

    # Missing __radd__ → sum() fails
    # Missing __rmul__ → 3 * vector fails

    def __repr__(self):
        return f"Vector({self.x}, {self.y})"


# v1 = BrokenVector(1, 2)
# v2 = BrokenVector(3, 4)
# v1 + v2      # Works
# 3 * v1       # TypeError! (int doesn't know how to multiply by Vector)
# sum([v1, v2]) # TypeError! (0 + v1 fails because int.__add__ returns NotImplemented)


# ── Challenge 3: __getattr__ infinite recursion ─────────────────────────────
"""
PROBLEM: This LazyRecord crashes with infinite recursion when you
         access any attribute.

HINT:    - __getattr__ calls self._data which triggers __getattr__ again
         - The issue is in __init__: self._data = {} triggers __setattr__
           which tries to access self._data before it exists
         - Use object.__setattr__ in __init__ to bootstrap
"""


class BrokenLazyRecord:
    def __init__(self, data: dict):
        # BUG: self._data = data triggers __setattr__
        # which might trigger __getattr__ for self._data → infinite loop
        self._data = data  # This MIGHT work but is fragile

    def __getattr__(self, name):
        # BUG: accessing self._data here could trigger __getattr__ recursively
        # if _data hasn't been set yet
        if name in self._data:
            return self._data[name]
        raise AttributeError(f"No attribute '{name}'")

    def __setattr__(self, name, value):
        if name.startswith('_'):
            # Try to set normally, but _data might not exist yet
            object.__setattr__(self, name, value)
        else:
            # BUG: self._data might not exist during __init__
            self._data[name] = value


# ─────────────────────────────────────────────────────────────────────────────
# SECTION 5: REFACTORING CHALLENGE
# ─────────────────────────────────────────────────────────────────────────────
"""
REFACTORING CHALLENGE: Messy Matrix Class
───────────────────────────────────────────

Refactor to properly use magic methods:
    1. __repr__ and __str__ for display
    2. __eq__ and __hash__ for comparisons
    3. __add__, __mul__, __rmul__ for arithmetic
    4. __getitem__ and __setitem__ for element access: m[1, 2]
    5. __len__ and __iter__ for container behavior
    6. __bool__ for truthiness (non-zero matrix)
    7. __neg__ for negation
"""


class MessyMatrix:
    """Refactor me to use proper magic methods!"""

    def __init__(self, rows):
        self.rows = [list(row) for row in rows]
        self.nrows = len(rows)
        self.ncols = len(rows[0]) if rows else 0

    def get_element(self, row, col):
        return self.rows[row][col]

    def set_element(self, row, col, value):
        self.rows[row][col] = value

    def add_matrix(self, other):
        if self.nrows != other.nrows or self.ncols != other.ncols:
            raise ValueError("Matrix dimensions must match")
        result = []
        for i in range(self.nrows):
            row = []
            for j in range(self.ncols):
                row.append(self.rows[i][j] + other.rows[i][j])
            result.append(row)
        return MessyMatrix(result)

    def scale(self, factor):
        result = []
        for i in range(self.nrows):
            row = []
            for j in range(self.ncols):
                row.append(self.rows[i][j] * factor)
            result.append(row)
        return MessyMatrix(result)

    def is_equal(self, other):
        if self.nrows != other.nrows or self.ncols != other.ncols:
            return False
        for i in range(self.nrows):
            for j in range(self.ncols):
                if self.rows[i][j] != other.rows[i][j]:
                    return False
        return True

    def display(self):
        for row in self.rows:
            print(" ".join(f"{x:6.2f}" for x in row))

    def to_flat_list(self):
        result = []
        for row in self.rows:
            for val in row:
                result.append(val)
        return result

    def is_zero(self):
        for row in self.rows:
            for val in row:
                if val != 0:
                    return False
        return True

    def negate(self):
        return self.scale(-1)


# ─────────────────────────────────────────────────────────────────────────────
# QUICK SELF-TEST
# ─────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("=" * 60)
    print("  12_magic_methods.py — Self Test")
    print("=" * 60)

    # Test Money type
    print("\n[Test] Money type:")
    usd_10 = Money(10.00, "USD")
    usd_20 = Money(20.00, "USD")
    inr = Money(500, "INR")

    # Arithmetic
    total = usd_10 + usd_20
    assert total == Money(30.00, "USD")
    doubled = usd_10 * 2
    assert doubled == Money(20.00, "USD")
    assert 3 * usd_10 == Money(30.00, "USD")
    print(f"  {usd_10} + {usd_20} = {total}")
    print(f"  {usd_10} * 2 = {doubled}")

    # Currency safety
    try:
        usd_10 + inr
    except ValueError as e:
        print(f"  Currency mismatch caught: {e}")

    # Hashing (usable in sets)
    money_set = {usd_10, usd_20, Money(10.00, "USD")}
    assert len(money_set) == 2  # deduplication works!
    print(f"  Set dedup: {len(money_set)} unique values from 3 inputs")

    # sum() works via __radd__
    prices = [Money(9.99), Money(24.99), Money(4.99)]
    total = sum(prices)
    print(f"  sum({[str(p) for p in prices]}) = {total}")

    # repr vs str
    print(f"  repr: {repr(usd_10)}")
    print(f"  str:  {str(usd_10)}")
    print(f"  INR:  {inr}")

    # Test AttrDict
    print("\n[Test] AttrDict (custom container):")
    config = AttrDict({"host": "localhost", "port": 5432, "db": {"name": "mydb"}})
    assert config.host == "localhost"
    assert config["port"] == 5432
    assert config.db.name == "mydb"  # nested dict → nested AttrDict
    assert "host" in config
    assert len(config) == 3
    config.new_key = "new_value"
    assert config.new_key == "new_value"
    print(f"  config.host = {config.host}")
    print(f"  config.db.name = {config.db.name}")
    print(f"  len(config) = {len(config)}")

    # Test Validator (__call__)
    print("\n[Test] Validator (__call__):")
    validate_age = Validator(min_val=0, max_val=150, expected_type=int,
                            error_msg="Invalid age")
    assert validate_age(25) is True
    try:
        validate_age(-1)
    except ValueError as e:
        print(f"  Caught: {e}")
    try:
        validate_age("not a number")
    except TypeError as e:
        print(f"  Caught: {e}")

    # Test APIClient (__getattr__ + __getitem__)
    print("\n[Test] APIClient (fluent interface):")
    client = APIClient("https://api.example.com")
    result = client.users[42].get()
    assert result["url"] == "https://api.example.com/users/42"
    print(f"  client.users[42].get() → {result['url']}")
    result = client.posts.create.post(data={"title": "Hello"})
    print(f"  client.posts.create.post() → {result['url']}")

    # Test comparison (total_ordering)
    print("\n[Test] Money comparisons (total_ordering):")
    assert Money(10) < Money(20)
    assert Money(20) > Money(10)
    assert Money(10) <= Money(10)
    assert Money(10) >= Money(10)
    assert Money(0).__bool__() is False
    assert Money(1).__bool__() is True
    sorted_prices = sorted([Money(30), Money(10), Money(20)])
    print(f"  Sorted: {[str(p) for p in sorted_prices]}")

    print("\n✓ All magic methods tests passed!")
    print("=" * 60)
