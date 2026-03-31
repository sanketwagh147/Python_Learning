"""
================================================================================
  METACLASSES & __init_subclass__ — From Fundamentals to Production-Ready Mastery
================================================================================
  Author: Senior Software Engineer Practice Guide
  Goal:   Understand how classes are created, leverage metaclasses and
          __init_subclass__ for framework design, and avoid over-engineering.
================================================================================
"""

# ─────────────────────────────────────────────────────────────────────────────
# SECTION 1: UNDER THE HOOD — How Classes Are Actually Created
# ─────────────────────────────────────────────────────────────────────────────
"""
In Python, EVERYTHING is an object — including classes themselves.

    class Dog:
        pass

    type(Dog)   → <class 'type'>
    type(type)  → <class 'type'>   # type is its own metaclass!

The creation chain when Python sees `class Dog: ...`:

    1. Python collects the class body into a dict (namespace)
    2. Determines the metaclass (default: type)
    3. Calls: type('Dog', (object,), namespace_dict)
       This invokes:
         a) type.__new__(mcs, name, bases, namespace)  → creates the class obj
         b) type.__init__(cls, name, bases, namespace)  → initializes it

So when we write a custom metaclass, we intercept class CREATION itself.

    class Meta(type):
        def __new__(mcs, name, bases, namespace):
            # Runs BEFORE the class object exists
            # Can modify namespace, add methods, enforce rules
            cls = super().__new__(mcs, name, bases, namespace)
            return cls

        def __init__(cls, name, bases, namespace):
            # Runs AFTER the class object is created
            # cls is the newly created class
            super().__init__(name, bases, namespace)

        def __call__(cls, *args, **kwargs):
            # Runs when you instantiate: Dog()
            # Controls instance creation — this is how Singletons work
            instance = super().__call__(*args, **kwargs)
            return instance

MODERN ALTERNATIVE — __init_subclass__ (Python 3.6+):
    For MOST use cases, you don't need a metaclass.  __init_subclass__
    is a classmethod hook called on the PARENT when a new subclass is defined.

    class Base:
        def __init_subclass__(cls, **kwargs):
            super().__init_subclass__(**kwargs)
            # cls is the new subclass being created
            # runs at class definition time, not instantiation time
"""


# ── Proof: Watching the class creation lifecycle ────────────────────────────

class LifecycleMeta(type):
    """Metaclass that prints every step of class creation."""

    def __new__(mcs, name, bases, namespace):
        print(f"  [Meta.__new__] Creating class '{name}'")
        print(f"  [Meta.__new__] Bases: {bases}")
        print(f"  [Meta.__new__] Methods defined: {[k for k in namespace if not k.startswith('_')]}")
        cls = super().__new__(mcs, name, bases, namespace)
        return cls

    def __init__(cls, name, bases, namespace):
        print(f"  [Meta.__init__] Initializing class '{name}'")
        super().__init__(name, bases, namespace)

    def __call__(cls, *args, **kwargs):
        print(f"  [Meta.__call__] Instantiating '{cls.__name__}' with args={args}")
        instance = super().__call__(*args, **kwargs)
        return instance


# Uncomment to test:
# class Animal(metaclass=LifecycleMeta):
#     def speak(self):
#         return "..."
#
# a = Animal()  # See all three steps fire


# ─────────────────────────────────────────────────────────────────────────────
# SECTION 2: PRODUCTION-READY EXAMPLE — Auto-Registering Plugin System
# ─────────────────────────────────────────────────────────────────────────────
"""
Real-world scenario: You're building a plugin system (like Django admin,
Flask blueprints, or pytest fixtures).  Any class that subclasses BasePlugin
automatically registers itself.

Two implementations shown:
  1. Using a metaclass (classic approach)
  2. Using __init_subclass__ (modern, preferred)
"""

# ── Approach 1: Metaclass-based registry ────────────────────────────────────

class RegistryMeta(type):
    """Metaclass that auto-registers subclasses into a registry."""

    _registry: dict = {}

    def __new__(mcs, name, bases, namespace):
        cls = super().__new__(mcs, name, bases, namespace)
        # Don't register the base class itself
        if bases:  # has parent classes → it's a subclass
            if not hasattr(cls, 'name'):
                raise TypeError(f"Plugin '{name}' must define a 'name' class attribute")
            mcs._registry[cls.name] = cls
        return cls

    @classmethod
    def get_plugin(mcs, name: str):
        return mcs._registry.get(name)

    @classmethod
    def list_plugins(mcs):
        return dict(mcs._registry)


class BasePlugin(metaclass=RegistryMeta):
    """Base class — subclasses auto-register."""
    name: str  # must be overridden

    def execute(self):
        raise NotImplementedError


class CSVExporter(BasePlugin):
    name = "csv"
    def execute(self):
        return "Exporting to CSV..."


class JSONExporter(BasePlugin):
    name = "json"
    def execute(self):
        return "Exporting to JSON..."


# Uncomment to test:
# print(RegistryMeta.list_plugins())      # {'csv': <class 'CSVExporter'>, ...}
# plugin = RegistryMeta.get_plugin("csv")
# print(plugin().execute())               # "Exporting to CSV..."


# ── Approach 2: __init_subclass__ (PREFERRED — same result, less magic) ─────

class BaseHandler:
    """Modern plugin system using __init_subclass__ — no metaclass needed."""

    _handlers: dict = {}

    def __init_subclass__(cls, handler_name: str = None, **kwargs):
        super().__init_subclass__(**kwargs)
        name = handler_name or cls.__name__.lower()
        cls._handlers[name] = cls
        cls._handler_name = name  # tag each subclass

    @classmethod
    def get_handler(cls, name: str):
        return cls._handlers.get(name)

    def handle(self, data):
        raise NotImplementedError


class EmailHandler(BaseHandler, handler_name="email"):
    def handle(self, data):
        return f"Sending email: {data}"


class SlackHandler(BaseHandler, handler_name="slack"):
    def handle(self, data):
        return f"Posting to Slack: {data}"


# Uncomment to test:
# print(BaseHandler._handlers)   # {'email': <class 'EmailHandler'>, ...}
# h = BaseHandler.get_handler("slack")
# print(h().handle("Deploy done"))  # "Posting to Slack: Deploy done"


# ── Production Example: Singleton via Metaclass ─────────────────────────────

class SingletonMeta(type):
    """Thread-safe Singleton metaclass."""
    _instances: dict = {}
    _lock = __import__('threading').Lock()

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            with cls._lock:
                # Double-checked locking pattern
                if cls not in cls._instances:
                    instance = super().__call__(*args, **kwargs)
                    cls._instances[cls] = instance
        return cls._instances[cls]


class DatabaseConnection(metaclass=SingletonMeta):
    def __init__(self):
        self.connection_id = id(self)
        print(f"  [DB] New connection created: {self.connection_id}")


# Uncomment to test:
# db1 = DatabaseConnection()
# db2 = DatabaseConnection()
# assert db1 is db2  # Same instance!
# print(f"  db1.connection_id == db2.connection_id → {db1.connection_id == db2.connection_id}")


# ─────────────────────────────────────────────────────────────────────────────
# SECTION 3: COMMON PITFALLS — Top 3 Bugs Juniors Introduce
# ─────────────────────────────────────────────────────────────────────────────
"""
PITFALL 1: Mutable class-level registry shared across metaclass instances
───────────────────────────────────────────────────────────────────────────
    class Meta(type):
        registry = {}     # ← SHARED across ALL classes using this metaclass
        
    PROBLEM: If you have two separate plugin systems using the same metaclass,
    they pollute each other's registry.
    
    FIX: Use a per-base-class registry, or separate metaclass instances.


PITFALL 2: Forgetting to call super().__new__ / super().__init_subclass__
───────────────────────────────────────────────────────────────────────────
    class Base:
        def __init_subclass__(cls, **kwargs):
            # Missing: super().__init_subclass__(**kwargs)
            ...
    
    PROBLEM: Breaks cooperative multiple inheritance.  If another parent
    also defines __init_subclass__, it never fires.
    
    FIX: ALWAYS call super().__init_subclass__(**kwargs).


PITFALL 3: Using metaclasses when __init_subclass__ or a decorator suffices
───────────────────────────────────────────────────────────────────────────
    Juniors learn metaclasses and use them EVERYWHERE.  Metaclasses:
    - Can't be easily combined (class can only have ONE metaclass)
    - Make debugging harder (magic at class-definition time)
    - Confuse collaborators
    
    RULE OF THUMB:
        Need to modify class creation?    → __init_subclass__ first
        Need to control instantiation?    → __init_subclass__ + __new__
        Need to intercept attribute access on the CLASS itself? → metaclass
        Building a framework (Django ORM)? → maybe metaclass
"""


# ─────────────────────────────────────────────────────────────────────────────
# SECTION 4: BROKEN CODE CHALLENGES — Fix These!
# ─────────────────────────────────────────────────────────────────────────────

# ── Challenge 1: Broken Singleton (NOT thread-safe) ─────────────────────────
"""
PROBLEM: This singleton has a race condition.  Two threads can create
         two different instances.

HINT:    - Add a lock
         - Use double-checked locking pattern
         - Bonus: Make it work with __init__ arguments (first-call wins)
"""

class BrokenSingletonMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            # BUG: Race condition — another thread could be here too!
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


# ── Challenge 2: Broken Auto-Validator ──────────────────────────────────────
"""
PROBLEM: This metaclass should enforce that every method has a docstring.
         But it has two bugs:
         1. It crashes on dunder methods
         2. It doesn't handle @staticmethod / @classmethod correctly

HINT:    - Filter out dunder methods
         - Check for staticmethod/classmethod descriptors before callable()
"""

class DocstringEnforcerMeta(type):
    def __new__(mcs, name, bases, namespace):
        for attr_name, attr_value in namespace.items():
            if callable(attr_value):
                # BUG 1: This crashes on __init__ and other dunders
                # BUG 2: staticmethod objects aren't callable in namespace
                if not attr_value.__doc__:
                    raise TypeError(
                        f"Method '{attr_name}' in class '{name}' "
                        f"must have a docstring"
                    )
        return super().__new__(mcs, name, bases, namespace)


# ── Challenge 3: Broken init_subclass with kwargs ───────────────────────────
"""
PROBLEM: This plugin system crashes when using multiple inheritance.

HINT:    - The **kwargs aren't being passed through to super()
         - handler_name leaks into kwargs for other parents
"""

class BrokenHandlerBase:
    _registry = {}

    def __init_subclass__(cls, handler_name=None):
        # BUG: Missing super().__init_subclass__() and **kwargs
        if handler_name:
            cls._registry[handler_name] = cls


class LoggingMixin:
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        print(f"  LoggingMixin sees new subclass: {cls.__name__}")


# This will crash: TypeError about unexpected keyword arguments
# class MyHandler(BrokenHandlerBase, LoggingMixin, handler_name="my"):
#     pass


# ─────────────────────────────────────────────────────────────────────────────
# SECTION 5: REFACTORING CHALLENGE
# ─────────────────────────────────────────────────────────────────────────────
"""
REFACTORING CHALLENGE: Messy Plugin Loader
───────────────────────────────────────────

The function below manually manages a plugin registry with repetitive
if/elif chains.  Refactor it to use __init_subclass__ so adding a new
format requires ZERO changes to existing code.

REQUIREMENTS:
    1. Use __init_subclass__ for auto-registration
    2. Each format should be a separate class
    3. The load_and_export() function should just do: registry[fmt]().export(data)
    4. Adding "xml" support should only require writing a new class
"""


def messy_export(data: dict, fmt: str, output_path: str) -> str:
    """Messy monolithic exporter — refactor me!"""
    if fmt == "csv":
        import csv
        import io
        output = io.StringIO()
        writer = csv.DictWriter(output, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)
        result = output.getvalue()
        with open(output_path, 'w') as f:
            f.write(result)
        return f"CSV exported to {output_path}"
    elif fmt == "json":
        import json
        result = json.dumps(data, indent=2)
        with open(output_path, 'w') as f:
            f.write(result)
        return f"JSON exported to {output_path}"
    elif fmt == "yaml":
        # Pretend yaml is available
        lines = []
        for item in data:
            lines.append("- " + ", ".join(f"{k}: {v}" for k, v in item.items()))
        result = "\n".join(lines)
        with open(output_path, 'w') as f:
            f.write(result)
        return f"YAML exported to {output_path}"
    else:
        raise ValueError(f"Unknown format: {fmt}")


# ─────────────────────────────────────────────────────────────────────────────
# QUICK SELF-TEST (run this file to verify nothing crashes)
# ─────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("=" * 60)
    print("  05_metaclasses.py — Self Test")
    print("=" * 60)

    # Test registry metaclass
    print("\n[Test] RegistryMeta plugin system:")
    plugins = RegistryMeta.list_plugins()
    assert "csv" in plugins
    assert "json" in plugins
    print(f"  Registered plugins: {list(plugins.keys())}")
    print(f"  CSV execute: {plugins['csv']().execute()}")

    # Test __init_subclass__ handlers
    print("\n[Test] __init_subclass__ handler system:")
    print(f"  Registered: {list(BaseHandler._handlers.keys())}")
    assert "email" in BaseHandler._handlers
    assert "slack" in BaseHandler._handlers
    h = BaseHandler.get_handler("email")
    print(f"  Email handle: {h().handle('Test message')}")

    # Test Singleton metaclass
    print("\n[Test] Singleton metaclass:")
    db1 = DatabaseConnection()
    db2 = DatabaseConnection()
    assert db1 is db2
    print(f"  db1 is db2 → {db1 is db2}")

    print("\n✓ All metaclass tests passed!")
    print("=" * 60)
