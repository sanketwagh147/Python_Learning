# Facade Pattern — Question 2 (Medium)

## Problem: E-Commerce Checkout Facade

A checkout process involves multiple complex subsystems. Create a facade that the controller/API layer calls with a single `checkout()` method.

### Requirements

- Subsystems:
  - `InventoryService`: `check_stock(items) -> bool`, `reserve(items)`, `release(items)`
  - `PricingService`: `calculate_total(items, coupon=None) -> float`, `apply_tax(total, state) -> float`
  - `PaymentService`: `charge(card_token, amount) -> PaymentResult`
  - `ShippingService`: `estimate_delivery(address) -> date`, `create_shipment(order_id, address) -> str`
  - `NotificationService`: `send_confirmation(email, order_id)`, `send_shipping_update(email, tracking)`

- `CheckoutFacade.checkout(cart, customer, payment_info) -> OrderResult`:
  1. Check inventory
  2. Calculate pricing (with optional coupon)
  3. Charge payment
  4. Reserve inventory
  5. Create shipment
  6. Send confirmation email
  7. Return `OrderResult` with order_id, total, estimated_delivery, tracking

### Expected Usage

```python
facade = CheckoutFacade(
    InventoryService(), PricingService(), PaymentService(),
    ShippingService(), NotificationService()
)

result = facade.checkout(
    cart={"items": [{"sku": "LAPTOP-1", "qty": 1}], "coupon": "SAVE10"},
    customer={"email": "alice@test.com", "address": "123 Main St", "state": "CA"},
    payment={"card_token": "tok_visa_4242"}
)
print(result)
# OrderResult(order_id="ORD-001", total=1079.99, tracking="TRK-ABC", delivery="2024-02-15")
```

### Constraints

- If payment fails, release reserved inventory (rollback logic inside facade).
- If inventory is unavailable, return error before attempting payment.
- Each subsystem is independently testable with its own interface.

### Think About

- How does this differ from the Orchestrator pattern?
- Should the facade handle retries, or should that be in each subsystem?
