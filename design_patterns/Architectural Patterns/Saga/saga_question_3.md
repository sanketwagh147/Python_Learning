# Saga Pattern — Question 3 (Hard)

## Problem: Saga with Persistent State, Timeouts, and Retry Policies

Build a saga coordinator that persists saga state, handles step timeouts, supports configurable retry policies, and can resume from failures.

### Requirements

#### Saga Definition
```python
class SagaStep:
    name: str
    execute: Callable[[SagaContext], StepResult]
    compensate: Callable[[SagaContext], None]
    timeout_seconds: float
    retry_policy: RetryPolicy

class RetryPolicy:
    max_retries: int
    backoff_strategy: str  # "fixed", "exponential"
    base_delay: float

class SagaDefinition:
    name: str
    steps: list[SagaStep]
```

#### Saga Coordinator
```python
class SagaCoordinator:
    def __init__(self, definition: SagaDefinition, state_store: SagaStateStore): ...
    def execute(self, initial_data: dict) -> SagaResult: ...
    def resume(self, saga_id: str) -> SagaResult: ...  # resume from last checkpoint
```

#### State Store
```python
class SagaStateStore:
    def save(self, saga_id: str, state: SagaState): ...
    def load(self, saga_id: str) -> SagaState: ...

class SagaState:
    saga_id: str
    status: str  # "running", "completed", "compensating", "failed"
    current_step: int
    completed_steps: list[str]
    step_results: dict[str, Any]
    retry_counts: dict[str, int]
    started_at: datetime
    updated_at: datetime
```

### Expected Usage

```python
saga = SagaDefinition("order_fulfillment", [
    SagaStep(
        name="reserve_inventory",
        execute=reserve_inventory,
        compensate=release_inventory,
        timeout_seconds=5.0,
        retry_policy=RetryPolicy(max_retries=3, backoff_strategy="exponential", base_delay=1.0),
    ),
    SagaStep(
        name="process_payment",
        execute=process_payment,
        compensate=refund_payment,
        timeout_seconds=10.0,
        retry_policy=RetryPolicy(max_retries=2, backoff_strategy="fixed", base_delay=2.0),
    ),
    SagaStep(
        name="create_shipment",
        execute=create_shipment,
        compensate=cancel_shipment,
        timeout_seconds=15.0,
        retry_policy=RetryPolicy(max_retries=1, backoff_strategy="fixed", base_delay=0),
    ),
])

coordinator = SagaCoordinator(saga, InMemorySagaStateStore())

# Execute
result = coordinator.execute({"order_id": "O-1", "items": [...], "amount": 99.99})
# → [reserve_inventory] Attempt 1... ✓
# → [process_payment] Attempt 1... ✗ (timeout)
# → [process_payment] Attempt 2 (backoff 2s)... ✓
# → [create_shipment] Attempt 1... ✓
# → Saga completed: order_fulfillment (saga_id: S-001)

# Simulate crash after step 1 — resume from checkpoint
coordinator2 = SagaCoordinator(saga, same_state_store)
result = coordinator2.resume("S-001")
# → Resuming saga S-001 from step 2 (process_payment)...
```

### Constraints

- State is persisted AFTER each step completes (for crash recovery).
- Timeout: if a step exceeds `timeout_seconds`, treat as failure → retry or compensate.
- Retry: follow the retry policy. Exponential backoff = `base_delay * 2^attempt`.
- Compensation: if all retries exhausted, compensate completed steps in reverse.
- Resume: load state from store, skip completed steps, continue from `current_step`.
- Logging: every attempt, success, failure, compensation, and state save is logged.

### Think About

- How do real saga implementations (Temporal, NServiceBus) handle state persistence?
- What if compensation itself needs retries?
- How would you add saga timeouts (the entire saga, not just steps)?
- Idempotency: if `resume` re-executes a step that partially completed, what could go wrong?
