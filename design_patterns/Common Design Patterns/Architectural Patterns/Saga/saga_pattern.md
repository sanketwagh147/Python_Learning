# Saga Pattern

Manages distributed transactions across multiple services. Each step has a **compensating action** (undo). If any step fails, all previously completed steps are rolled back in reverse order to maintain consistency.

## Key Concepts

- **Saga**: A sequence of local transactions, each with a compensation.
- **Compensating Action**: The "undo" for a completed step (e.g., refund after charge).
- **Orchestration-based Saga**: A central orchestrator drives the saga (shown here).
- **Choreography-based Saga**: Each service emits events and the next service reacts (no central coordinator).

## Saga vs Orchestrator

| | Orchestrator | Saga |
|---|---|---|
| **Focus** | General workflow coordination | Distributed transaction consistency |
| **Compensation** | Optional | Required — every step MUST have an undo |
| **Use case** | Any multi-step workflow | Cross-service transactions that must be atomic |

## Structure

```
SagaOrchestrator
   │
   ├── Step 1: execute() ←→ compensate()
   ├── Step 2: execute() ←→ compensate()
   └── Step 3: execute() ←→ compensate()

On failure at Step 3:
   compensate(Step 2) → compensate(Step 1)
```

## Example — Travel Booking

```python
class BookFlightStep(SagaStep):
    def execute(self, ctx):    # book the flight
    def compensate(self, ctx):  # cancel the flight

class BookHotelStep(SagaStep):
    def execute(self, ctx):    # reserve the room
    def compensate(self, ctx):  # cancel the reservation

# If hotel fails → flight is compensated (cancelled)
```

## When to Use

✅ Distributed transactions across microservices  
✅ Each step must be reversible (payment → refund, reserve → release)  
✅ You need eventual consistency without distributed locks  

## When NOT to Use

❌ Single-database transactions (just use DB transactions)  
❌ Steps that can't be compensated / undone  
❌ Simple workflows that don't span multiple services
