"""
Orchestrator Pattern — Real-World Example
==========================================
Order Fulfillment Orchestrator

A central OrderOrchestrator coordinates the entire order workflow:
  1. Validate inventory
  2. Process payment
  3. Send confirmation email
  4. Schedule shipping

The orchestrator controls the flow, handles failures, and
rolls back completed steps on failure — unlike CoR where each
handler only knows about itself.
"""

from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum, auto


# ── Data Model ──────────────────────────────────────────────

class StepStatus(Enum):
    SUCCESS = auto()
    FAILED = auto()
    SKIPPED = auto()


@dataclass
class StepResult:
    step_name: str
    status: StepStatus
    message: str


@dataclass
class OrderContext:
    """Shared context that flows through the orchestrator."""
    order_id: str
    item: str
    quantity: int
    amount: float
    customer_email: str
    results: list[StepResult] = field(default_factory=list)
    failed: bool = False


# ── Step Abstraction ────────────────────────────────────────

class WorkflowStep(ABC):
    @abstractmethod
    def execute(self, ctx: OrderContext) -> StepResult: ...

    @abstractmethod
    def rollback(self, ctx: OrderContext) -> None: ...


# ── Concrete Steps ──────────────────────────────────────────

class InventoryStep(WorkflowStep):
    _stock = {"laptop": 5, "keyboard": 50, "monitor": 0}

    def execute(self, ctx: OrderContext) -> StepResult:
        available = self._stock.get(ctx.item, 0)
        if ctx.quantity > available:
            return StepResult("Inventory", StepStatus.FAILED,
                              f"Only {available} '{ctx.item}' in stock")
        self._stock[ctx.item] -= ctx.quantity  # reserve
        return StepResult("Inventory", StepStatus.SUCCESS,
                          f"Reserved {ctx.quantity} '{ctx.item}'")

    def rollback(self, ctx: OrderContext) -> None:
        self._stock[ctx.item] = self._stock.get(ctx.item, 0) + ctx.quantity
        print(f"  ↩ Inventory: released {ctx.quantity} '{ctx.item}'")


class PaymentStep(WorkflowStep):
    def execute(self, ctx: OrderContext) -> StepResult:
        if ctx.amount > 10_000:
            return StepResult("Payment", StepStatus.FAILED,
                              f"${ctx.amount:.2f} exceeds limit")
        return StepResult("Payment", StepStatus.SUCCESS,
                          f"Charged ${ctx.amount:.2f}")

    def rollback(self, ctx: OrderContext) -> None:
        print(f"  ↩ Payment: refunded ${ctx.amount:.2f}")


class EmailStep(WorkflowStep):
    def execute(self, ctx: OrderContext) -> StepResult:
        return StepResult("Email", StepStatus.SUCCESS,
                          f"Confirmation sent to {ctx.customer_email}")

    def rollback(self, ctx: OrderContext) -> None:
        print(f"  ↩ Email: sent cancellation to {ctx.customer_email}")


class ShippingStep(WorkflowStep):
    def execute(self, ctx: OrderContext) -> StepResult:
        return StepResult("Shipping", StepStatus.SUCCESS,
                          f"Shipping scheduled for order {ctx.order_id}")

    def rollback(self, ctx: OrderContext) -> None:
        print(f"  ↩ Shipping: cancelled shipment for {ctx.order_id}")


# ── Orchestrator ────────────────────────────────────────────

class OrderOrchestrator:
    """Central coordinator. Knows all steps, controls flow,
    and rolls back completed steps on failure."""

    def __init__(self, steps: list[WorkflowStep]):
        self._steps = steps

    def execute(self, ctx: OrderContext) -> OrderContext:
        completed: list[WorkflowStep] = []

        for step in self._steps:
            result = step.execute(ctx)
            ctx.results.append(result)

            if result.status == StepStatus.FAILED:
                ctx.failed = True
                print(f"  ❌ {result.step_name}: {result.message}")
                self._rollback(completed, ctx)
                break
            else:
                print(f"  ✔ {result.step_name}: {result.message}")
                completed.append(step)

        return ctx

    def _rollback(self, completed: list[WorkflowStep], ctx: OrderContext) -> None:
        if completed:
            print("  --- Rolling back ---")
            for step in reversed(completed):
                step.rollback(ctx)


# ── Demo ────────────────────────────────────────────────────

def run_order(ctx: OrderContext) -> None:
    orchestrator = OrderOrchestrator([
        InventoryStep(),
        PaymentStep(),
        EmailStep(),
        ShippingStep(),
    ])
    orchestrator.execute(ctx)
    status = "FAILED" if ctx.failed else "COMPLETED"
    print(f"\n--- Order {ctx.order_id} [{status}] ---\n")


if __name__ == "__main__":
    # 1) Happy path — all steps succeed
    run_order(OrderContext("ORD-001", "laptop", 1, 999.99, "alice@example.com"))

    # 2) Fails at Payment → rolls back Inventory
    run_order(OrderContext("ORD-002", "keyboard", 2, 25_000.00, "bob@example.com"))

    # 3) Fails at Inventory → nothing to roll back
    run_order(OrderContext("ORD-003", "monitor", 5, 499.00, "carol@example.com"))
