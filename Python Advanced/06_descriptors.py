"""
================================================================================
  DESCRIPTORS — From Fundamentals to Production-Ready Mastery
================================================================================
  Author: Senior Software Engineer Practice Guide
  Goal:   Understand __get__/__set__/__delete__ — the mechanism that powers
          @property, @classmethod, @staticmethod, ORMs, and validated attrs.
================================================================================
"""

# ─────────────────────────────────────────────────────────────────────────────
# SECTION 1: UNDER THE HOOD — The Descriptor Protocol
# ─────────────────────────────────────────────────────────────────────────────
"""
A descriptor is any object that defines __get__, __set__, or __delete__.

When you access an attribute on an object (obj.x), Python's lookup order is:

    1. data descriptor on the CLASS  (defines __set__ or __delete__)
    2. instance __dict__
    3. non-data descriptor on the CLASS  (defines only __get__)
    4. __getattr__  (if defined, as a fallback)

This is called the DESCRIPTOR PROTOCOL and it's the backbone of Python's
attribute access system.

The three dunder methods:

    class MyDescriptor:
        def __get__(self, obj, objtype=None):
            '''
            Called when the attribute is ACCESSED.
            - obj:      the instance (None if accessed on the class)
            - objtype:  the class itself
            '''
            ...

        def __set__(self, obj, value):
            '''
            Called when the attribute is ASSIGNED.
            - obj:      the instance
            - value:    the value being assigned
            '''
            ...

        def __delete__(self, obj):
            '''
            Called when the attribute is DELETED (del obj.x).
            - obj:      the instance
            '''
            ...

    DATA DESCRIPTOR:     defines __set__ and/or __delete__
                         → takes PRIORITY over instance __dict__
    NON-DATA DESCRIPTOR: defines only __get__
                         → instance __dict__ can shadow it

WHY THIS MATTERS:
    - @property is a data descriptor (has __get__, __set__, __delete__)
    - Regular methods are non-data descriptors (have only __get__)
    - @classmethod, @staticmethod are descriptors
    - Django's models.CharField, SQLAlchemy's Column — all descriptors
    - Understanding this explains WHY property can't be overridden by
      instance attributes, but methods can
"""


# ── Proof: Watching descriptor access ───────────────────────────────────────

class VerboseDescriptor:
    """Descriptor that prints every access, assignment, and deletion."""

    def __set_name__(self, owner, name):
        """Called at class creation time — gives us the attribute name."""
        self.public_name = name
        self.private_name = f'_desc_{name}'
        print(f"  [__set_name__] Descriptor bound to '{owner.__name__}.{name}'")

    def __get__(self, obj, objtype=None):
        if obj is None:
            # Accessed on the class (e.g., MyClass.attr)
            print(f"  [__get__] Class-level access for '{self.public_name}'")
            return self
        value = getattr(obj, self.private_name, 'NOT SET')
        print(f"  [__get__] Getting '{self.public_name}' → {value}")
        return value

    def __set__(self, obj, value):
        print(f"  [__set__] Setting '{self.public_name}' = {value}")
        setattr(obj, self.private_name, value)

    def __delete__(self, obj):
        print(f"  [__delete__] Deleting '{self.public_name}'")
        delattr(obj, self.private_name)


class DemoModel:
    name = VerboseDescriptor()
    age = VerboseDescriptor()

# Uncomment to test:
# m = DemoModel()
# m.name = "Sanket"     # [__set__] Setting 'name' = Sanket
# print(m.name)          # [__get__] Getting 'name' → Sanket
# del m.name             # [__delete__] Deleting 'name'
# DemoModel.name         # [__get__] Class-level access for 'name'


# ─────────────────────────────────────────────────────────────────────────────
# SECTION 2: PRODUCTION-READY EXAMPLES
# ─────────────────────────────────────────────────────────────────────────────

# ── Example 1: Validated Attribute (like Django/Pydantic fields) ────────────

class Validated:
    """
    Reusable, type-checked, range-validated descriptor.
    
    Usage:
        class User:
            age = Validated(int, min_val=0, max_val=150)
            name = Validated(str, min_length=1, max_length=100)
    """

    def __init__(self, expected_type, *, min_val=None, max_val=None,
                 min_length=None, max_length=None):
        self.expected_type = expected_type
        self.min_val = min_val
        self.max_val = max_val
        self.min_length = min_length
        self.max_length = max_length

    def __set_name__(self, owner, name):
        self.public_name = name
        self.private_name = f'_validated_{name}'

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        return getattr(obj, self.private_name, None)

    def __set__(self, obj, value):
        # Type check
        if not isinstance(value, self.expected_type):
            raise TypeError(
                f"'{self.public_name}' must be {self.expected_type.__name__}, "
                f"got {type(value).__name__}"
            )
        # Range check (for numbers)
        if self.min_val is not None and value < self.min_val:
            raise ValueError(f"'{self.public_name}' must be >= {self.min_val}")
        if self.max_val is not None and value > self.max_val:
            raise ValueError(f"'{self.public_name}' must be <= {self.max_val}")
        # Length check (for strings/sequences)
        if self.min_length is not None and len(value) < self.min_length:
            raise ValueError(f"'{self.public_name}' must have length >= {self.min_length}")
        if self.max_length is not None and len(value) > self.max_length:
            raise ValueError(f"'{self.public_name}' must have length <= {self.max_length}")

        setattr(obj, self.private_name, value)

    def __delete__(self, obj):
        delattr(obj, self.private_name)


class Employee:
    name = Validated(str, min_length=1, max_length=100)
    age = Validated(int, min_val=18, max_val=120)
    salary = Validated(float, min_val=0.0)

    def __init__(self, name: str, age: int, salary: float):
        self.name = name
        self.age = age
        self.salary = salary

    def __repr__(self):
        return f"Employee(name={self.name!r}, age={self.age}, salary={self.salary})"


# ── Example 2: Lazy/Cached Property (non-data descriptor) ──────────────────

class LazyProperty:
    """
    Descriptor that computes a value on first access and caches it
    in the instance __dict__.  Since this is a NON-DATA descriptor
    (no __set__), the cached value in __dict__ takes priority on 
    subsequent accesses → zero overhead after first call.

    This is exactly how functools.cached_property works.
    """

    def __init__(self, func):
        self.func = func
        self.attrname = None
        self.__doc__ = func.__doc__

    def __set_name__(self, owner, name):
        self.attrname = name

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        # Compute and cache in instance __dict__
        value = self.func(obj)
        obj.__dict__[self.attrname] = value  # shadows the descriptor
        return value


class DataAnalyzer:
    def __init__(self, data: list):
        self.data = data

    @LazyProperty
    def statistics(self):
        """Expensive computation — only runs once."""
        print("  [Computing statistics...]")
        n = len(self.data)
        total = sum(self.data)
        mean = total / n if n else 0
        sorted_data = sorted(self.data)
        median = sorted_data[n // 2] if n else 0
        return {"count": n, "sum": total, "mean": mean, "median": median}


# Uncomment to test:
# analyzer = DataAnalyzer([3, 1, 4, 1, 5, 9, 2, 6])
# print(analyzer.statistics)   # [Computing statistics...] → shows dict
# print(analyzer.statistics)   # No computation message — cached!
# print('statistics' in analyzer.__dict__)  # True — it's in instance dict


# ── Example 3: Audited Field (tracks all changes) ──────────────────────────

from datetime import datetime


class AuditedField:
    """
    Descriptor that keeps a full change history.  Useful for compliance,
    debugging, or building undo/redo systems.
    """

    def __set_name__(self, owner, name):
        self.public_name = name
        self.value_attr = f'_audited_{name}_value'
        self.history_attr = f'_audited_{name}_history'

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        return getattr(obj, self.value_attr, None)

    def __set__(self, obj, value):
        old_value = getattr(obj, self.value_attr, '<UNSET>')
        # Initialize history list if needed
        if not hasattr(obj, self.history_attr):
            setattr(obj, self.history_attr, [])
        history = getattr(obj, self.history_attr)
        history.append({
            'timestamp': datetime.now().isoformat(),
            'old': old_value,
            'new': value,
        })
        setattr(obj, self.value_attr, value)

    def get_history(self, obj) -> list:
        """Get full change history for this field on an instance."""
        return getattr(obj, self.history_attr, [])


class Contract:
    status = AuditedField()
    price = AuditedField()

    def __init__(self, status: str, price: float):
        self.status = status
        self.price = price


# Uncomment to test:
# c = Contract("draft", 10000.0)
# c.status = "review"
# c.status = "approved"
# c.price = 12000.0
# print("Status history:", Contract.status.get_history(c))
# print("Price history:", Contract.price.get_history(c))


# ─────────────────────────────────────────────────────────────────────────────
# SECTION 3: COMMON PITFALLS — Top 3 Bugs Juniors Introduce
# ─────────────────────────────────────────────────────────────────────────────
"""
PITFALL 1: Storing descriptor state on the DESCRIPTOR, not the INSTANCE
───────────────────────────────────────────────────────────────────────────
    class Bad:
        def __set__(self, obj, value):
            self.value = value   # ← stored on descriptor, shared by ALL instances!
    
    FIX: Store on the instance:  obj.__dict__[self.private_name] = value
         or use setattr(obj, self.private_name, value)


PITFALL 2: Not implementing __set_name__
───────────────────────────────────────────────────────────────────────────
    Without __set_name__, you have to pass the attribute name manually:
    
        class Foo:
            x = MyDescriptor('x')  # ← annoying, error-prone duplication
    
    FIX: Implement __set_name__(self, owner, name) → Python 3.6+ calls
         it automatically during class creation.


PITFALL 3: Confusing data vs non-data descriptors
───────────────────────────────────────────────────────────────────────────
    Non-data descriptor (only __get__) is SHADOWED by instance __dict__:
    
        class Desc:
            def __get__(self, obj, cls): return 42
        class Foo:
            x = Desc()
        f = Foo()
        f.x = 99        # This shadows the descriptor!
        print(f.x)       # 99, NOT 42
    
    Data descriptor (has __set__) CANNOT be shadowed:
    
        class Desc:
            def __get__(self, obj, cls): return 42
            def __set__(self, obj, value): pass
        class Foo:
            x = Desc()
        f = Foo()
        f.x = 99        # Calls Desc.__set__
        print(f.x)       # 42, NOT 99
    
    FIX: Know the priority chain. If you want enforcement, make it a
         data descriptor. If you want caching (cached_property), make
         it non-data.
"""


# ─────────────────────────────────────────────────────────────────────────────
# SECTION 4: BROKEN CODE CHALLENGES — Fix These!
# ─────────────────────────────────────────────────────────────────────────────

# ── Challenge 1: Shared state bug ───────────────────────────────────────────
"""
PROBLEM: All instances share the same value!
         User("Alice").name returns "Bob" after User("Bob") is created.

HINT:    Where is the value being stored?  It should be per-instance,
         not per-descriptor.
"""

class BrokenTyped:
    def __init__(self, expected_type):
        self.expected_type = expected_type
        self.value = None  # BUG: stored on descriptor, shared!

    def __set_name__(self, owner, name):
        self.name = name

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        return self.value  # BUG: returns shared value

    def __set__(self, obj, value):
        if not isinstance(value, self.expected_type):
            raise TypeError(f"Expected {self.expected_type}")
        self.value = value  # BUG: stores on descriptor, not instance


class BrokenUser:
    name = BrokenTyped(str)
    age = BrokenTyped(int)

    def __init__(self, name, age):
        self.name = name
        self.age = age


# Uncomment to see the bug:
# u1 = BrokenUser("Alice", 30)
# u2 = BrokenUser("Bob", 25)
# print(u1.name)  # "Bob" ← WRONG! Should be "Alice"


# ── Challenge 2: Descriptor that doesn't work with inheritance ──────────────
"""
PROBLEM: The descriptor works for the base class but breaks when subclassed,
         because __set_name__ stores the owner class and the private name
         collides between parent and child.

HINT:    Use the instance's __dict__ directly or use a unique storage
         key per (descriptor_id, instance) pair.
"""

class BrokenCached:
    """Supposed to work like cached_property but has a subtle bug."""

    def __init__(self, func):
        self.func = func

    def __set_name__(self, owner, name):
        self.attrname = name

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        # BUG: If subclass OVERRIDES this descriptor with a new one,
        # but the attribute name is the same, they collide in __dict__
        if self.attrname in obj.__dict__:
            return obj.__dict__[self.attrname]
        value = self.func(obj)
        obj.__dict__[self.attrname] = value
        return value

    def __set__(self, obj, value):
        # BUG: This makes it a data descriptor, so __dict__ lookup
        # in __get__ is NEVER reached — obj.__dict__ can't shadow it!
        obj.__dict__[self.attrname] = value


# Uncomment to see the bug:
# class Base:
#     @BrokenCached
#     def config(self):
#         return {"base": True}
#
# b = Base()
# print(b.config)  # Calls func but __get__ always recomputes because
#                    # __set__ makes this a data descriptor, preventing shadowing


# ── Challenge 3: Thread-unsafe descriptor ───────────────────────────────────
"""
PROBLEM: Multiple threads writing to the same audited field cause
         lost updates in the history list.

HINT:    - list.append is atomic in CPython, so history might be okay
         - BUT the read-then-write of the value is NOT atomic
         - Use a per-instance lock or threading.local
"""

import threading


class BrokenThreadSafeField:
    def __set_name__(self, owner, name):
        self.name = name
        self.private = f'_tsf_{name}'

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        return getattr(obj, self.private, None)

    def __set__(self, obj, value):
        # BUG: Not thread-safe!  Two threads can interleave here.
        old = getattr(obj, self.private, None)
        # Simulate slow operation
        # import time; time.sleep(0.001)
        setattr(obj, self.private, value)
        # If we had a history, old could be wrong


class BrokenCounter:
    value = BrokenThreadSafeField()

    def __init__(self):
        self.value = 0


# ─────────────────────────────────────────────────────────────────────────────
# SECTION 5: REFACTORING CHALLENGE
# ─────────────────────────────────────────────────────────────────────────────
"""
REFACTORING CHALLENGE: Messy Form Validator
────────────────────────────────────────────

The class below has repetitive validation logic in the __init__.
Refactor it using descriptors so that:
    1. Each field validates itself (type, range, required)
    2. Adding a new field requires ONE line, not a new if-block
    3. Error messages are consistent and descriptive
"""


class MessyRegistrationForm:
    """Messy validator — refactor me using descriptors!"""

    def __init__(self, username, email, age, password, confirm_pass):
        # Validate username
        if not isinstance(username, str):
            raise TypeError("username must be a string")
        if len(username) < 3:
            raise ValueError("username must be at least 3 characters")
        if len(username) > 50:
            raise ValueError("username must be at most 50 characters")
        self.username = username

        # Validate email
        if not isinstance(email, str):
            raise TypeError("email must be a string")
        if '@' not in email:
            raise ValueError("email must contain @")
        if len(email) > 254:
            raise ValueError("email must be at most 254 characters")
        self.email = email

        # Validate age
        if not isinstance(age, int):
            raise TypeError("age must be an integer")
        if age < 13:
            raise ValueError("age must be at least 13")
        if age > 120:
            raise ValueError("age must be at most 120")
        self.age = age

        # Validate password
        if not isinstance(password, str):
            raise TypeError("password must be a string")
        if len(password) < 8:
            raise ValueError("password must be at least 8 characters")
        self.password = password

        # Validate confirm_pass
        if password != confirm_pass:
            raise ValueError("passwords do not match")
        self.confirm_pass = confirm_pass


# ─────────────────────────────────────────────────────────────────────────────
# QUICK SELF-TEST
# ─────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("=" * 60)
    print("  06_descriptors.py — Self Test")
    print("=" * 60)

    # Test Validated descriptor
    print("\n[Test] Validated descriptor:")
    emp = Employee("Sanket", 28, 85000.0)
    print(f"  Created: {emp}")
    try:
        emp.age = -5
    except ValueError as e:
        print(f"  Caught: {e}")
    try:
        emp.name = 123
    except TypeError as e:
        print(f"  Caught: {e}")

    # Test LazyProperty
    print("\n[Test] LazyProperty descriptor:")
    analyzer = DataAnalyzer([3, 1, 4, 1, 5, 9, 2, 6])
    print(f"  First access: {analyzer.statistics}")
    print(f"  Second access (cached): {analyzer.statistics}")
    assert 'statistics' in analyzer.__dict__

    # Test AuditedField
    print("\n[Test] AuditedField descriptor:")
    c = Contract("draft", 10000.0)
    c.status = "review"
    c.status = "approved"
    history = Contract.status.get_history(c)
    print(f"  Status changes: {len(history)}")
    assert len(history) == 3  # init + 2 changes

    print("\n✓ All descriptor tests passed!")
    print("=" * 60)
