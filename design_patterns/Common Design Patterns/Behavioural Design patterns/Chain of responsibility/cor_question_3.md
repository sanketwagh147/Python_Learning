# Chain of Responsibility — Question 3 (Hard)

## Problem: Dynamic Discount Engine with Priority and Stacking Rules

An e-commerce platform calculates discounts using a chain of handlers. Handlers have **priorities**, can **stack** (multiple discounts apply), and can **block** further discounts.

### Requirements

#### Discount Handler
```python
class DiscountHandler(ABC):
    priority: int  # lower = runs first
    stackable: bool  # can other discounts apply after this?
    
    @abstractmethod
    def calculate(self, order: Order) -> DiscountResult: ...
```

`DiscountResult`: `discount_amount: float`, `reason: str`, `blocks_further: bool`

#### Handlers (ordered by priority)
1. **CouponDiscount** (priority=1, stackable=True): applies coupon code percentage
2. **LoyaltyDiscount** (priority=2, stackable=True): +5% off for loyalty members
3. **BulkDiscount** (priority=3, stackable=True): 10% off if quantity > 10
4. **FlashSaleDiscount** (priority=4, stackable=False, blocks_further=True): 30% off — NO other discounts after this
5. **EmployeeDiscount** (priority=5, stackable=True): 25% off for employees
6. **MaxCapHandler** (priority=99): ensures total discount never exceeds 50%

#### Order
```python
@dataclass
class Order:
    items: list[OrderItem]
    customer_type: str  # "regular", "loyalty", "employee"
    coupon_code: str | None
    is_flash_sale: bool
```

### Expected Usage

```python
engine = DiscountEngine()
engine.register(CouponDiscount())
engine.register(LoyaltyDiscount())
engine.register(BulkDiscount())
engine.register(FlashSaleDiscount())
engine.register(EmployeeDiscount())
engine.register(MaxCapHandler())

# Case 1: Loyalty + Coupon stack
order1 = Order(items=[...], customer_type="loyalty", coupon_code="SAVE10", is_flash_sale=False)
result = engine.apply(order1)
# → Coupon: -10%, Loyalty: -5% → Total: 15% off

# Case 2: Flash sale blocks everything after it
order2 = Order(items=[...], customer_type="employee", coupon_code="SAVE10", is_flash_sale=True)
result = engine.apply(order2)
# → Coupon: -10% (priority 1, runs first), Flash Sale: -30% (blocks further) → Total: 40% off
# → Employee discount NOT applied (blocked by flash sale)

# Case 3: Cap at 50%
order3 = Order(items=[...], customer_type="employee", coupon_code="SAVE40")
result = engine.apply(order3)
# → Coupon: -40%, Employee: -25% → 65% → capped to 50%
```

### Constraints

- Handlers auto-sort by priority when registered.
- When a handler returns `blocks_further=True`, the chain stops (except MaxCapHandler which always runs).
- Each handler independently decides if it applies (e.g., CouponDiscount skips if no coupon code).
- Engine returns a `DiscountSummary` with: applied discounts list, total percentage, final amount.
- Write at least 5 test cases covering: stacking, blocking, cap, no discounts, single discount.

### Think About

- How does the dynamic priority + stacking differ from a simple linear chain?
- Could you use the Strategy pattern for individual discount calculations and CoR for the flow?
- How would you make this configurable via a database instead of hardcoded rules?
