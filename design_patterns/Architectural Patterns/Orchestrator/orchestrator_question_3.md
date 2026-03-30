# Orchestrator Pattern — Question 3 (Hard)

## Problem: Workflow Engine with Dynamic Steps, Branching, and Parallel Execution

Build a generic workflow orchestrator that supports sequential steps, conditional branches, parallel steps, and dynamic step composition.

### Requirements

#### Step Types
```python
class Step(ABC):
    def execute(self, context: WorkflowContext) -> StepResult: ...
    def compensate(self, context: WorkflowContext): ...

class SequentialStep(Step):
    """Run steps one after another."""
    def __init__(self, steps: list[Step]): ...

class ParallelStep(Step):
    """Run steps concurrently (simulated) and wait for all to complete."""
    def __init__(self, steps: list[Step]): ...

class ConditionalStep(Step):
    """Branch based on a condition evaluated from context."""
    def __init__(self, condition: Callable, if_true: Step, if_false: Step): ...

class RetryStep(Step):
    """Wrap a step with retry logic."""
    def __init__(self, step: Step, max_retries: int, backoff: float): ...
```

#### Orchestrator
```python
class WorkflowOrchestrator:
    def __init__(self, root_step: Step): ...
    def run(self, initial_context: dict) -> WorkflowResult: ...
```

#### WorkflowContext
```python
class WorkflowContext:
    data: dict              # shared data between steps
    completed_steps: list   # for compensation
    logs: list[str]         # execution log
```

### Expected Usage

```python
# Build a complex workflow
workflow = SequentialStep([
    ValidateOrderStep(),
    ConditionalStep(
        condition=lambda ctx: ctx.data["total"] > 1000,
        if_true=SequentialStep([
            FraudCheckStep(),
            ManualApprovalStep(),
        ]),
        if_false=AutoApproveStep(),
    ),
    ParallelStep([
        ReserveInventoryStep(),
        CalculateShippingStep(),
    ]),
    RetryStep(ChargepaymentStep(), max_retries=3, backoff=1.0),
    SendConfirmationStep(),
])

orchestrator = WorkflowOrchestrator(workflow)
result = orchestrator.run({"order_id": "O-1", "total": 1500, "items": [...]})

# Execution trace:
# → [SEQ] Starting workflow...
# → [STEP] ValidateOrderStep ✓
# → [COND] total > 1000 → TRUE
# →   [SEQ] Starting fraud check branch...
# →   [STEP] FraudCheckStep ✓
# →   [STEP] ManualApprovalStep ✓
# → [PARALLEL] Running 2 steps...
# →   [STEP] ReserveInventoryStep ✓
# →   [STEP] CalculateShippingStep ✓
# → [RETRY] ChargePaymentStep attempt 1... ✗
# → [RETRY] ChargePaymentStep attempt 2... ✓
# → [STEP] SendConfirmationStep ✓
# → Workflow completed in 5 steps
```

### Constraints

- Workflows are composable — any Step can contain other Steps.
- `WorkflowContext` is shared between all steps (read/write).
- Compensation: if step N fails, compensate steps N-1, N-2, ... in reverse.
- ParallelStep: if any sub-step fails, compensate all completed sub-steps.
- The orchestrator produces a full execution trace (log).
- Steps can write to context (e.g., `ctx.data["reservation_id"] = "..."`) for later steps.

### Think About

- How does this compare to Temporal.io or Apache Airflow workflows?
- What makes this pattern different from a simple chain of function calls?
- How would you persist workflow state for long-running processes?
