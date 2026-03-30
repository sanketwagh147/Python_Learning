# Saga Pattern — Question 2 (Medium)

## Problem: Choreography-Based Saga with Event-Driven Steps

Convert the typical orchestrated saga into a choreography-based saga where each service listens for events and decides what to do next.

### Requirements

#### Events
```python
class OrderCreatedEvent: order_id, customer_id, items, total
class PaymentCompletedEvent: order_id, payment_id
class PaymentFailedEvent: order_id, reason
class InventoryReservedEvent: order_id, reservation_id
class InventoryFailedEvent: order_id, reason
class ShipmentCreatedEvent: order_id, tracking_id
class OrderCompletedEvent: order_id
class OrderCancelledEvent: order_id, reason
```

#### Services (each listens for events and publishes new ones)
```python
class PaymentService:
    # Listens for: OrderCreatedEvent
    # Publishes: PaymentCompletedEvent or PaymentFailedEvent

class InventoryService:
    # Listens for: PaymentCompletedEvent
    # Publishes: InventoryReservedEvent or InventoryFailedEvent
    # Also listens for: PaymentFailedEvent → release any holds

class ShippingService:
    # Listens for: InventoryReservedEvent
    # Publishes: ShipmentCreatedEvent

class OrderService:
    # Listens for: ShipmentCreatedEvent → mark order completed
    # Also: PaymentFailedEvent, InventoryFailedEvent → mark order cancelled
```

#### Event Bus
```python
class EventBus:
    def subscribe(self, event_type: type, handler: Callable): ...
    def publish(self, event): ...
```

### Expected Usage

```python
bus = EventBus()
payment = PaymentService(bus)
inventory = InventoryService(bus)
shipping = ShippingService(bus)
orders = OrderService(bus)

# Trigger the saga by publishing the first event
bus.publish(OrderCreatedEvent("O-1", "C-1", ["item1"], 99.99))

# Events flow automatically:
# OrderCreatedEvent → PaymentService charges → PaymentCompletedEvent
# PaymentCompletedEvent → InventoryService reserves → InventoryReservedEvent
# InventoryReservedEvent → ShippingService ships → ShipmentCreatedEvent
# ShipmentCreatedEvent → OrderService completes → OrderCompletedEvent

# Failure scenario:
# OrderCreatedEvent → PaymentService charges → PaymentFailedEvent
# PaymentFailedEvent → OrderService cancels order
```

### Constraints

- NO central orchestrator — each service acts independently based on events.
- Compensation happens via events (e.g., `PaymentFailedEvent` triggers inventory release).
- Each service only knows about the events it subscribes to.
- Services must be idempotent — processing the same event twice should be safe.

### Think About

- Orchestration vs Choreography: what are the trade-offs?
- How do you debug a failed choreography saga? (Event tracing/correlation IDs)
- What if events are delivered out of order?
