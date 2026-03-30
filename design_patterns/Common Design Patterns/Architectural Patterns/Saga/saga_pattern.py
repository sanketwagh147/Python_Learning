"""
Saga Pattern — Real-World Example
===================================
Travel Booking Saga

Book a trip that spans 3 independent services:
  1. Flight booking
  2. Hotel reservation
  3. Car rental

If any step fails, all previous bookings are cancelled (compensated).
Each step is a SagaStep with execute() and compensate().
"""

from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass, field


# ── Data Model ──────────────────────────────────────────────

@dataclass
class TripContext:
    trip_id: str
    destination: str
    days: int
    budget: float
    log: list[str] = field(default_factory=list)
    failed: bool = False
    failure_reason: str = ""


# ── Saga Step Abstraction ───────────────────────────────────

class SagaStep(ABC):
    @property
    @abstractmethod
    def name(self) -> str: ...

    @abstractmethod
    def execute(self, ctx: TripContext) -> bool:
        """Run the step. Return True on success, False on failure."""

    @abstractmethod
    def compensate(self, ctx: TripContext) -> None:
        """Undo/rollback this step."""


# ── Concrete Steps ──────────────────────────────────────────

class BookFlightStep(SagaStep):
    name = "Flight"

    def execute(self, ctx: TripContext) -> bool:
        if ctx.destination.lower() == "mars":
            ctx.log.append("❌ Flight: no flights to Mars")
            return False
        ctx.log.append(f"✔ Flight: booked to {ctx.destination}")
        return True

    def compensate(self, ctx: TripContext) -> None:
        ctx.log.append(f"↩ Flight: cancelled flight to {ctx.destination}")


class BookHotelStep(SagaStep):
    name = "Hotel"

    def execute(self, ctx: TripContext) -> bool:
        if ctx.days > 30:
            ctx.log.append("❌ Hotel: max 30-day stay exceeded")
            return False
        ctx.log.append(f"✔ Hotel: reserved for {ctx.days} nights")
        return True

    def compensate(self, ctx: TripContext) -> None:
        ctx.log.append(f"↩ Hotel: cancelled {ctx.days}-night reservation")


class RentCarStep(SagaStep):
    name = "Car Rental"

    def execute(self, ctx: TripContext) -> bool:
        if ctx.budget < 500:
            ctx.log.append("❌ Car Rental: budget too low (min $500)")
            return False
        ctx.log.append(f"✔ Car Rental: rented for {ctx.days} days")
        return True

    def compensate(self, ctx: TripContext) -> None:
        ctx.log.append(f"↩ Car Rental: cancelled {ctx.days}-day rental")


# ── Saga Orchestrator ──────────────────────────────────────

class SagaOrchestrator:
    """Executes saga steps in order. On failure, compensates
    all completed steps in reverse."""

    def __init__(self, steps: list[SagaStep]):
        self._steps = steps

    def run(self, ctx: TripContext) -> TripContext:
        completed: list[SagaStep] = []

        for step in self._steps:
            success = step.execute(ctx)
            if not success:
                ctx.failed = True
                ctx.failure_reason = f"Failed at: {step.name}"
                # Compensate in reverse order
                for done in reversed(completed):
                    done.compensate(ctx)
                break
            completed.append(step)

        return ctx


# ── Demo ────────────────────────────────────────────────────

def book_trip(ctx: TripContext) -> None:
    saga = SagaOrchestrator([
        BookFlightStep(),
        BookHotelStep(),
        RentCarStep(),
    ])
    saga.run(ctx)
    status = "FAILED" if ctx.failed else "BOOKED"
    print(f"\n--- Trip {ctx.trip_id} [{status}] ---")
    if ctx.failed:
        print(f"  Reason: {ctx.failure_reason}")
    for msg in ctx.log:
        print(f"  {msg}")


if __name__ == "__main__":
    # 1) Happy path — everything succeeds
    book_trip(TripContext("TRIP-001", "Paris", 7, 2000.00))

    # 2) Fails at Car Rental → compensates Hotel and Flight
    book_trip(TripContext("TRIP-002", "Tokyo", 5, 200.00))

    # 3) Fails at Hotel → compensates Flight only
    book_trip(TripContext("TRIP-003", "London", 60, 5000.00))

    # 4) Fails at Flight → nothing to compensate
    book_trip(TripContext("TRIP-004", "Mars", 10, 99999.00))
