# Open-Closed Principle — Question 2 (Medium)

## Problem: Discount Engine that's Open for Extension

An e-commerce system applies discounts. New discount types are added frequently. The system must be extendable without modifying existing discount logic.

### The Violating Code

```python
class DiscountCalculator:
    def calculate(self, order, discount_code):
        if discount_code == "SUMMER20":
            return order.total * 0.20
        elif discount_code == "VIP":
            return order.total * 0.15 if order.customer.is_vip else 0
        elif discount_code == "BULK":
            return order.total * 0.10 if order.item_count > 10 else 0
        elif discount_code == "FIRST_ORDER":
            return order.total * 0.25 if order.customer.order_count == 0 else 0
        else:
            return 0
```

### Requirements

Refactor using OCP:

```python
class DiscountRule(ABC):
    def is_applicable(self, order: Order) -> bool: ...
    def calculate(self, order: Order) -> float: ...

class DiscountEngine:
    def __init__(self, rules: list[DiscountRule]): ...
    def best_discount(self, order: Order) -> float: ...
    def all_applicable(self, order: Order) -> list[tuple[str, float]]: ...
```

#### Concrete Rules
- `PercentageDiscount(code, percent, condition)`: generic percentage off
- `BulkDiscount(min_items, percent)`: discount when buying many items
- `VIPDiscount(percent)`: only for VIP customers
- `FirstOrderDiscount(percent)`: only for first-time customers
- `SeasonalDiscount(code, percent, start_date, end_date)`: time-limited

### Expected Usage

```python
engine = DiscountEngine([
    PercentageDiscount("SUMMER20", 0.20, condition=lambda o: True),
    BulkDiscount(min_items=10, percent=0.10),
    VIPDiscount(percent=0.15),
    FirstOrderDiscount(percent=0.25),
    SeasonalDiscount("HOLIDAY", 0.30, date(2024, 12, 20), date(2024, 12, 31)),
])

order = Order(total=200, item_count=12, customer=Customer(is_vip=True, order_count=5))

# Get best discount
best = engine.best_discount(order)
print(best)  # → ("BulkDiscount", 20.0) or ("SUMMER20", 40.0)

# List all applicable
all_discounts = engine.all_applicable(order)
# → [("SUMMER20", 40.0), ("BulkDiscount", 20.0), ("VIPDiscount", 30.0)]
```

### Constraints

- Adding a new discount: create ONE new class. `DiscountEngine` is NEVER modified.
- Rules are loaded at startup (could come from config/DB).
- `best_discount` returns the highest applicable discount.

### Think About

- How would you load discount rules from a JSON config file?
- This is OCP + Strategy. How do the two principles complement each other?
