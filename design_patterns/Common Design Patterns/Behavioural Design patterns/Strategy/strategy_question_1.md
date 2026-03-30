# Strategy Pattern — Question 1 (Easy)

## Problem: Payment Method Selector

An e-commerce checkout supports multiple payment methods. The strategy is selected at runtime.

### Requirements

- `PaymentStrategy(ABC)`: `pay(amount: float) -> str`
- Strategies: `CreditCardPayment(card_number)`, `PayPalPayment(email)`, `CryptoPayment(wallet_address)`
- `Checkout`: accepts a strategy and calls `pay()`.

### Expected Usage

```python
checkout = Checkout()

checkout.set_strategy(CreditCardPayment("4242-4242-4242-4242"))
print(checkout.process(99.99))
# → "Paid $99.99 via Credit Card ending in 4242"

checkout.set_strategy(PayPalPayment("alice@test.com"))
print(checkout.process(49.50))
# → "Paid $49.50 via PayPal (alice@test.com)"
```

### Constraints

- Strategy can be swapped at runtime via `set_strategy()`.
- `Checkout` doesn't know the details of any specific payment method.
