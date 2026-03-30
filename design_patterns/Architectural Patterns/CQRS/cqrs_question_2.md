# CQRS Pattern — Question 2 (Medium)

## Problem: E-Commerce with Separate Read & Write Stores + Event Sync

An e-commerce system uses CQRS with separate write (normalized) and read (denormalized) stores, synced via events.

### Requirements

#### Write Model (Command Side)
```python
# Normalized — clean domain model
class Product:
    id: str
    name: str
    price: float
    stock: int

class Order:
    id: str
    customer_id: str
    items: list[OrderItem]  # product_id + quantity
    status: str
```

#### Read Model (Query Side)
```python
# Denormalized — optimized for display
class OrderView:
    id: str
    customer_name: str          # joined from customer
    items: list[OrderItemView]  # product name + price snapshot
    total: float                # pre-calculated
    status: str
```

#### Event Sync
```python
class DomainEvent(ABC): ...

class OrderPlacedEvent(DomainEvent):
    order_id: str
    customer_id: str
    items: list[OrderItem]

class OrderStatusChangedEvent(DomainEvent):
    order_id: str
    new_status: str

class EventBus:
    def publish(self, event: DomainEvent): ...
    def subscribe(self, event_type: type, handler: Callable): ...
```

### Expected Usage

```python
# Write side
cmd = PlaceOrderCommand(customer_id="C1", items=[("P1", 2), ("P2", 1)])
order_id = command_handler.handle(cmd)
# → Publishes OrderPlacedEvent

# Read model projection handles the event and builds the view
views = query_handler.get_orders_for_customer("C1")
# → [OrderView(id="O1", customer_name="Alice", items=[...], total=149.97, status="placed")]

# Status change
cmd = UpdateOrderStatusCommand(order_id, "shipped")
command_handler.handle(cmd)
# → Publishes OrderStatusChangedEvent → Read model updates
```

### Constraints

- Write and read stores are SEPARATE dictionaries (simulating separate DBs).
- Events sync the read model — the read store is a **projection** of events.
- Read model pre-calculates fields (total, names) for fast queries.
- If event sync fails, read model may be stale — this is acceptable (eventual consistency).

### Think About

- Why have separate stores if they hold the same data? (Read optimization, different schemas.)
- What is "eventual consistency" and how does it apply here?
