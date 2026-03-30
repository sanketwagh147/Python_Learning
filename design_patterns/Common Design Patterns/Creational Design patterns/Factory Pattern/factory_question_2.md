# Factory Pattern — Question 2 (Medium)

## Problem: Payment Gateway Factory (Factory Method)

An e-commerce platform supports multiple payment gateways. Each gateway has different initialization logic and API calls.

### Requirements

- Abstract base: `PaymentGateway` with:
  - `authorize(amount: float) -> bool`
  - `capture(transaction_id: str) -> bool`
  - `refund(transaction_id: str, amount: float) -> bool`

- Concrete gateways: `StripeGateway`, `PayPalGateway`, `RazorpayGateway`

- Abstract creator: `PaymentProcessor` with a **factory method** `create_gateway() -> PaymentGateway`

- Concrete creators: `StripeProcessor`, `PayPalProcessor`, `RazorpayProcessor` — each overrides `create_gateway()`.

- `PaymentProcessor` has a `process_payment(amount)` template method:
  1. Creates gateway via `create_gateway()`
  2. Calls `authorize(amount)`
  3. If authorized, calls `capture(txn_id)`
  4. Returns success/failure

### Expected Usage

```python
processor = StripeProcessor()
result = processor.process_payment(99.99)
# → [Stripe] Authorizing $99.99... ✓
# → [Stripe] Capturing TXN-001... ✓
# → Payment successful

processor = RazorpayProcessor()
result = processor.process_payment(500.00)
# → [Razorpay] Authorizing ₹500.00... ✓
# → [Razorpay] Capturing TXN-002... ✓
# → Payment successful
```

### Constraints

- The `process_payment()` logic lives in the **base** `PaymentProcessor` — subclasses only override `create_gateway()`.
- This is the **Factory Method** variant (not Simple Factory).

### Think About

- Why is this better than passing a gateway type string to a single processor?
- How does this pattern help when adding a new gateway (e.g., `SquareGateway`)?
