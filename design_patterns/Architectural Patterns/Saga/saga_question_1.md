# Saga Pattern — Question 1 (Easy)

## Problem: Travel Booking Saga

A travel booking involves multiple steps. If any step fails, undo the completed steps.

### Requirements

- Steps: `BookFlight`, `BookHotel`, `BookRentalCar`
- Each step has `execute()` and `compensate()`.
- `BookingSaga` runs steps in order. On failure, compensates in reverse.

### Expected Usage

```python
saga = BookingSaga([
    BookFlight(flight="FL-100", date="2024-06-15"),
    BookHotel(hotel="Hilton", nights=3),
    BookRentalCar(car_type="sedan", days=3),
])

# Happy path
result = saga.execute()
# → Booking flight FL-100... ✓
# → Booking Hilton for 3 nights... ✓
# → Booking sedan rental for 3 days... ✓
# → SagaResult(status="completed")

# Failure scenario: rental car unavailable
result = saga.execute()
# → Booking flight FL-100... ✓
# → Booking Hilton for 3 nights... ✓
# → Booking sedan rental... ✗ (CarUnavailableError)
# → Compensating: Cancelling hotel booking... ✓
# → Compensating: Cancelling flight... ✓
# → SagaResult(status="failed", failed_step="BookRentalCar")
```

### Constraints

- Compensation runs in REVERSE order of successful steps.
- If a step hasn't executed, its compensation is NOT called.
- `SagaResult` includes: status, completed steps, failed step, error.
