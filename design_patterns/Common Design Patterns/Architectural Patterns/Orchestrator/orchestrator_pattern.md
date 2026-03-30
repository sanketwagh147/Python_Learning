# Orchestrator Pattern

A central coordinator that drives a multi-step workflow. Unlike Chain of Responsibility (where each handler decides the next step), the Orchestrator **knows** the full workflow and controls execution order, error handling, and retries.

## Key Concepts

- **Orchestrator**: Central class that owns the workflow steps and their execution order.
- **Steps / Services**: Independent units of work invoked by the orchestrator.
- **Workflow Result**: The orchestrator collects results and decides the overall outcome.

## Orchestrator vs Chain of Responsibility

| | Chain of Responsibility | Orchestrator |
|---|---|---|
| **Control** | Decentralized — each handler passes to the next | Centralized — orchestrator controls everything |
| **Knowledge** | Handlers don't know about each other | Orchestrator knows all steps |
| **Error handling** | Handler rejects and chain stops | Orchestrator can retry, skip, or compensate |
| **Adding steps** | Add a new handler to the chain | Add a step in the orchestrator's list |

## Structure

```
          Orchestrator
         /    |    \
        ▼     ▼     ▼
    Step A  Step B  Step C
```

The orchestrator calls each step in order, inspects the result,
and decides whether to proceed, retry, skip, or rollback.

## Example

```python
class OrderOrchestrator:
    def __init__(self, steps: list[WorkflowStep]):
        self._steps = steps

    def execute(self, ctx: OrderContext) -> OrderContext:
        completed = []
        for step in self._steps:
            result = step.execute(ctx)
            if result.status == StepStatus.FAILED:
                self._rollback(completed, ctx)
                break
            completed.append(step)
        return ctx

    def _rollback(self, completed, ctx):
        for step in reversed(completed):
            step.rollback(ctx)
```

## When to Use

✅ Multi-step workflows with conditional logic  
✅ Need retry, compensation, or rollback  
✅ Steps have dependencies (step 3 needs output of step 1)  
✅ Microservice coordination  

## When NOT to Use

❌ Simple linear validation (use Chain of Responsibility)  
❌ Fully independent steps with no coordination needed  
❌ Event-driven systems where choreography is more appropriate
