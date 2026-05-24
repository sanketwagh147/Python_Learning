# Descriptors Practice Solutions

## Solution 1 - Positive Money Fields
Descriptors centralize validation across many related fields.

```python
from decimal import Decimal


class PositiveDecimal:
    def __set_name__(self, owner, name):
        self.storage_name = f"_{name}"

    def __get__(self, instance, owner):
        if instance is None:
            return self
        return getattr(instance, self.storage_name, Decimal("0"))

    def __set__(self, instance, value):
        amount = Decimal(str(value))
        if amount < 0:
            raise ValueError("value must be non-negative")
        setattr(instance, self.storage_name, amount)
```

## Solution 2 - Normalized Contact Fields
The descriptor keeps normalization rules out of every model method.

```python
class EmailField:
    def __set_name__(self, owner, name):
        self.storage_name = f"_{name}"

    def __get__(self, instance, owner):
        return getattr(instance, self.storage_name, None) if instance else self

    def __set__(self, instance, value):
        normalized = value.strip().lower()
        if "@" not in normalized:
            raise ValueError("invalid email")
        setattr(instance, self.storage_name, normalized)
```

## Solution 3 - Lazy Secret Lookup
Fetch once, cache per instance, and let the owner decide when to invalidate.

```python
class LazySecret:
    def __init__(self, secret_name):
        self.secret_name = secret_name

    def __set_name__(self, owner, name):
        self.storage_name = f"_{name}"

    def __get__(self, instance, owner):
        if instance is None:
            return self
        if not hasattr(instance, self.storage_name):
            value = instance.secret_manager.fetch(self.secret_name)
            setattr(instance, self.storage_name, value)
        return getattr(instance, self.storage_name)
```

## Solution 4 - Unit-Aware Measurement Field
Normalize internally and expose helper methods for alternative units.

```python
class WeightKg:
    conversion = {"kg": 1.0, "g": 0.001, "lb": 0.453592}

    def __set_name__(self, owner, name):
        self.storage_name = f"_{name}"

    def __get__(self, instance, owner):
        return getattr(instance, self.storage_name, None) if instance else self

    def __set__(self, instance, value):
        amount, unit = value
        kg = float(amount) * self.conversion[unit]
        if kg < 0:
            raise ValueError("weight cannot be negative")
        setattr(instance, self.storage_name, kg)
```

## Solution 5 - Permissioned Attribute Access with Audit
Descriptors can guard both reads and writes if the actor lives on the instance.

```python
class ProtectedNote:
    def __set_name__(self, owner, name):
        self.storage_name = f"_{name}"

    def __get__(self, instance, owner):
        if instance is None:
            return self
        instance.audit_log.append((instance.actor.role, "read", self.storage_name))
        if not instance.actor.can_read_notes:
            raise PermissionError("read denied")
        return getattr(instance, self.storage_name)

    def __set__(self, instance, value):
        instance.audit_log.append((instance.actor.role, "write", self.storage_name))
        if not instance.actor.can_write_notes:
            raise PermissionError("write denied")
        setattr(instance, self.storage_name, value)
```