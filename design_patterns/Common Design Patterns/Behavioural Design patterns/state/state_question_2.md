# State Pattern — Question 2 (Medium)

## Problem: Order Lifecycle Management

An e-commerce order goes through multiple states with different allowed transitions and behaviors.

### Requirements

#### States
```
Created → Paid → Shipped → Delivered
    ↓        ↓       ↓
  Cancelled  Refunded (from Paid or Shipped)
```

#### State Behaviors
| State | Can Pay? | Can Ship? | Can Cancel? | Can Refund? | Can Deliver? |
|---|---|---|---|---|---|
| Created | ✅ | ❌ | ✅ | ❌ | ❌ |
| Paid | ❌ | ✅ | ❌ | ✅ | ❌ |
| Shipped | ❌ | ❌ | ❌ | ✅ | ✅ |
| Delivered | ❌ | ❌ | ❌ | ❌ | ❌ |
| Cancelled | ❌ | ❌ | ❌ | ❌ | ❌ |
| Refunded | ❌ | ❌ | ❌ | ❌ | ❌ |

### Expected Usage

```python
order = Order("ORD-001", items=["Laptop"])

order.pay(amount=999.99)
print(order.status)  # → "Paid"

order.ship(tracking="TRK-123")
print(order.status)  # → "Shipped"

order.deliver()
print(order.status)  # → "Delivered"

order.cancel()  # → InvalidTransitionError: Cannot cancel a Delivered order

# Refund from Shipped state
order2 = Order("ORD-002", items=["Mouse"])
order2.pay(50.0)
order2.ship("TRK-456")
order2.refund(reason="Damaged in transit")
print(order2.status)  # → "Refunded"
```

### Constraints

- Each state class handles ALL possible actions — invalid ones raise `InvalidTransitionError`.
- State transitions are handled by the state objects themselves.
- The `Order` class has NO `if/elif` for state checks.
- Track a `history: list` of state transitions with timestamps.

### Think About

- What if you need to add a "Processing" state between Paid and Shipped?
- How does this compare to using an enum + if/elif chain?
