# Orchestrator Pattern — Question 2 (Medium)

## Problem: Order Fulfillment Orchestrator with Error Handling and Compensation

Coordinate an order fulfillment workflow with multiple services, retries, and compensation logic.

### Requirements

#### Services
```python
class InventoryService:
    def reserve_items(self, items: list) -> ReservationId: ...
    def release_items(self, reservation_id: ReservationId): ...  # compensation

class PaymentService:
    def charge(self, customer_id: str, amount: float) -> PaymentId: ...
    def refund(self, payment_id: PaymentId): ...  # compensation

class ShippingService:
    def create_shipment(self, order_id: str, items: list) -> TrackingId: ...
    def cancel_shipment(self, tracking_id: TrackingId): ...  # compensation

class NotificationService:
    def notify(self, customer_id: str, message: str): ...
```

#### Orchestrator
```python
class OrderOrchestrator:
    def fulfill_order(self, order: Order) -> FulfillmentResult:
        """
        Steps:
        1. Reserve inventory
        2. Charge payment
        3. Create shipment
        4. Notify customer
        
        If step 2 fails → release inventory
        If step 3 fails → refund payment + release inventory
        """
```

### Expected Usage

```python
# Happy path
result = orchestrator.fulfill_order(order)
# → Reserving items... ✓ (RES-001)
# → Charging $99.99... ✓ (PAY-001)
# → Creating shipment... ✓ (TRK-001)
# → Notifying customer... ✓
# → FulfillmentResult(status="completed", tracking="TRK-001")

# Payment failure
result = orchestrator.fulfill_order(bad_order)
# → Reserving items... ✓ (RES-002)
# → Charging $99.99... ✗ (InsufficientFunds)
# → Compensating: Releasing inventory RES-002... ✓
# → FulfillmentResult(status="failed", error="Payment failed")
```

### Constraints

- Compensation runs in reverse order of completed steps.
- Each step that completed gets its compensating action called on failure.
- The orchestrator tracks which steps completed for proper rollback.
- Retry up to 2 times before failing.
- `FulfillmentResult` includes: status, completed_steps, failed_step, error.

### Think About

- How is this different from the Saga pattern? (Orchestrator = centralized control; Saga = distributed/choreographed.)
- What if the compensation itself fails?
