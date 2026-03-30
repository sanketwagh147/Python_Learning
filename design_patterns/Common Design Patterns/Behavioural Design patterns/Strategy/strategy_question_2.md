# Strategy Pattern — Question 2 (Medium)

## Problem: Shipping Cost Calculator with Dynamic Strategy Selection

A logistics system calculates shipping costs. The strategy depends on package weight, destination, and customer tier.

### Requirements

#### Strategy
```python
class ShippingStrategy(ABC):
    def calculate(self, weight_kg: float, distance_km: float) -> float: ...
    def estimated_days(self, distance_km: float) -> int: ...
```

Strategies:
- `StandardShipping`: $0.50/kg + $0.01/km, 5-7 days
- `ExpressShipping`: $1.50/kg + $0.03/km, 2-3 days
- `OvernightShipping`: $5.00/kg + $0.10/km, 1 day
- `FreeShipping`: $0, 7-10 days (only for orders above threshold)

#### Context
```python
class ShippingCalculator:
    def __init__(self, strategy_selector: Callable): ...
    def calculate_for_order(self, order: Order) -> ShippingQuote: ...
```

#### Auto-Selection Rules
```python
def select_strategy(order: Order) -> ShippingStrategy:
    if order.total > 100 and order.customer_tier == "premium":
        return FreeShipping()
    if order.priority == "urgent":
        return OvernightShipping()
    if order.total > 50:
        return ExpressShipping()
    return StandardShipping()
```

### Expected Usage

```python
selector = select_strategy
calculator = ShippingCalculator(selector)

order1 = Order(items=[...], total=150, weight=3.5, distance=500, customer_tier="premium")
quote1 = calculator.calculate_for_order(order1)
print(quote1)  # → ShippingQuote(cost=0.00, days=8, method="Free Shipping")

order2 = Order(total=30, weight=1.0, distance=200, priority="urgent")
quote2 = calculator.calculate_for_order(order2)
print(quote2)  # → ShippingQuote(cost=25.00, days=1, method="Overnight")
```

### Constraints

- The `select_strategy` function is itself injectable (passed to the calculator).
- `ShippingQuote` is a dataclass with `cost`, `estimated_days`, `method_name`.
- Adding a new shipping method requires only: 1 new Strategy class + update `select_strategy`.

### Think About

- How is strategy selection different from Foundation pattern (abstract factory)?
- Could you replace the function with a dictionary or config-driven selector?
