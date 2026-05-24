# Magic Methods Practice Solutions

## Solution 1 - Money Value Object

Implement only the dunder methods that match the domain cleanly.

```python
from dataclasses import dataclass
from decimal import Decimal
from functools import total_ordering


@total_ordering
@dataclass(frozen=True)
class Money:
    amount: Decimal
    currency: str

    def _assert_same_currency(self, other):
        if self.currency != other.currency:
            raise ValueError("currencies must match")

    def __add__(self, other):
        self._assert_same_currency(other)
        return Money(self.amount + other.amount, self.currency)

    def __sub__(self, other):
        self._assert_same_currency(other)
        return Money(self.amount - other.amount, self.currency)

    def __lt__(self, other):
        self._assert_same_currency(other)
        return self.amount < other.amount

    def __str__(self):
        return f"{self.currency} {self.amount:.2f}"
```

## Solution 2 - Inventory Batch Container

Container dunder methods make a small domain object natural to use.

```python
class InventoryBatch:
    def __init__(self, sku, serial_numbers):
        self.sku = sku
        self.serial_numbers = list(serial_numbers)

    def __len__(self):
        return len(self.serial_numbers)

    def __contains__(self, item):
        return item in self.serial_numbers

    def __bool__(self):
        return bool(self.serial_numbers)

    def __repr__(self):
        return f"InventoryBatch(sku={self.sku!r}, count={len(self)})"
```

## Solution 3 - Time Window Membership

`__contains__` is perfect for repeated `timestamp in window` checks.

```python
class TimeWindow:
    def __init__(self, start_hour, end_hour):
        self.start_hour = start_hour
        self.end_hour = end_hour

    def __contains__(self, hour):
        if self.start_hour <= self.end_hour:
            return self.start_hour <= hour < self.end_hour
        return hour >= self.start_hour or hour < self.end_hour

    def __repr__(self):
        return f"TimeWindow({self.start_hour}, {self.end_hour})"
```

## Solution 4 - Query Filter Composition

Overload operators only when the meaning is obvious and immutable.

```python
class QueryFilter:
    def __init__(self, expression):
        self.expression = expression

    def __and__(self, other):
        return QueryFilter(f"({self.expression}) AND ({other.expression})")

    def __or__(self, other):
        return QueryFilter(f"({self.expression}) OR ({other.expression})")

    def __repr__(self):
        return f"QueryFilter({self.expression!r})"
```

## Solution 5 - Weighted Scorecard Object

Expose iteration and ordering deliberately instead of trying to mimic every numeric type.

```python
from functools import total_ordering


@total_ordering
class Scorecard:
    def __init__(self, **components):
        self.components = components

    def total(self):
        return sum(self.components.values())

    def __iter__(self):
        return iter(self.components.items())

    def __add__(self, other):
        merged = {key: self.components.get(key, 0) + other.components.get(key, 0) for key in set(self.components) | set(other.components)}
        return Scorecard(**merged)

    def __eq__(self, other):
        return self.total() == other.total()

    def __lt__(self, other):
        return self.total() < other.total()
```
