"""
Chain of Responsibility — Real-World Example
=============================================
E-commerce Order Processing Pipeline

When a customer places an order on an e-commerce site, the order
passes through a chain of validation / processing steps:

  1. Inventory Check   → Is the item in stock?
  2. Payment Validation → Is the payment method valid and charged?
  3. Fraud Detection    → Does the order look suspicious?
  4. Shipping Setup     → Can we ship to the customer's address?

Each handler either rejects the order (stops the chain) or
forwards it to the next handler. If every handler approves,
the order is confirmed.
"""

from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass, field

from inventory_repository import (
    InventoryRepository,
    DBInventoryRepository,
    InMemoryInventoryRepository,
    get_session,
)


# ── Data Model ──────────────────────────────────────────────

@dataclass
class Order:
    order_id: str
    item: str
    quantity: int
    payment_method: str
    amount: float
    shipping_address: str
    is_flagged: bool = False          # pre-flagged by external system
    status: str = "pending"
    messages: list[str] = field(default_factory=list)


# ── Abstract Handler ────────────────────────────────────────

class OrderHandler(ABC):
    """Base handler that holds a reference to the next handler."""

    def __init__(self, next_handler: OrderHandler | None = None):
        self._next = next_handler

    def set_next(self, handler: OrderHandler) -> OrderHandler:
        self._next = handler
        return handler                # allows chaining: a.set_next(b).set_next(c)

    def handle(self, order: Order) -> Order:
        """Pass to the next handler, or finalize if chain is done."""
        if self._next:
            return self._next.handle(order)
        # End of chain — order passed every check
        order.status = "confirmed"
        order.messages.append("✅ Order confirmed!")
        return order


# ── Concrete Handlers ───────────────────────────────────────

class InventoryHandler(OrderHandler):
    """Check whether the requested quantity is in stock.

    Follows DIP — depends on InventoryRepository abstraction,
    not a hard-coded dict or direct DB call.
    """

    def __init__(
        self,
        repo: InventoryRepository,
        next_handler: OrderHandler | None = None,
    ):
        super().__init__(next_handler)
        self._repo = repo

    def handle(self, order: Order) -> Order:
        available = self._repo.get_stock(order.item)
        if order.quantity > available:
            order.status = "rejected"
            order.messages.append(
                f"❌ Inventory: '{order.item}' — requested {order.quantity}, "
                f"only {available} in stock."
            )
            return order
        order.messages.append(f"✔ Inventory: '{order.item}' is in stock.")
        return super().handle(order)


class PaymentHandler(OrderHandler):
    """Validate the payment method and amount."""

    _accepted_methods = {"credit_card", "debit_card", "paypal"}

    def handle(self, order: Order) -> Order:
        if order.payment_method not in self._accepted_methods:
            order.status = "rejected"
            order.messages.append(
                f"❌ Payment: '{order.payment_method}' is not accepted."
            )
            return order
        if order.amount <= 0:
            order.status = "rejected"
            order.messages.append("❌ Payment: invalid amount.")
            return order
        order.messages.append(
            f"✔ Payment: ${order.amount:.2f} via {order.payment_method} approved."
        )
        return super().handle(order)


class FraudDetectionHandler(OrderHandler):
    """Flag suspicious orders."""

    _max_safe_amount = 10_000

    def handle(self, order: Order) -> Order:
        if order.is_flagged:
            order.status = "rejected"
            order.messages.append("❌ Fraud: order was pre-flagged for review.")
            return order
        if order.amount > self._max_safe_amount:
            order.status = "rejected"
            order.messages.append(
                f"❌ Fraud: amount ${order.amount:.2f} exceeds "
                f"${self._max_safe_amount} limit."
            )
            return order
        order.messages.append("✔ Fraud check: order looks legitimate.")
        return super().handle(order)


class ShippingHandler(OrderHandler):
    """Verify we can ship to the destination."""

    _blocked_regions = {"antarctica", "mars"}

    def handle(self, order: Order) -> Order:
        if order.shipping_address.lower() in self._blocked_regions:
            order.status = "rejected"
            order.messages.append(
                f"❌ Shipping: cannot deliver to '{order.shipping_address}'."
            )
            return order
        order.messages.append(
            f"✔ Shipping: delivery to '{order.shipping_address}' is available."
        )
        return super().handle(order)


# ── Build the chain & run demo ──────────────────────────────

def build_order_pipeline(
    inventory_repo: InventoryRepository | None = None,
) -> OrderHandler:
    """Assemble the processing chain.

    Pass an InventoryRepository to control where stock data comes from.
    Defaults to DBInventoryRepository with a fresh session.
    """
    if inventory_repo is None:
        # Standalone usage — create session here.
        # In FastAPI you'd pass the repo from the route handler instead.
        session = get_session()
        inventory_repo = DBInventoryRepository(session)

    inventory = InventoryHandler(repo=inventory_repo)
    payment = PaymentHandler()
    fraud = FraudDetectionHandler()
    shipping = ShippingHandler()

    # Link: Inventory → Payment → Fraud → Shipping
    inventory.set_next(payment).set_next(fraud).set_next(shipping)
    return inventory


def process_order(
    order: Order,
    inventory_repo: InventoryRepository | None = None,
) -> None:
    pipeline = build_order_pipeline(inventory_repo)
    pipeline.handle(order)
    print(f"\n--- Order {order.order_id} [{order.status.upper()}] ---")
    for msg in order.messages:
        print(f"  {msg}")


# ── Test Cases ──────────────────────────────────────────────

if __name__ == "__main__":

    # 1) Happy path — passes every handler
    process_order(Order(
        order_id="ORD-001",
        item="laptop",
        quantity=1,
        payment_method="credit_card",
        amount=999.99,
        shipping_address="New York",
    ))

    # 2) Fails at Inventory — item out of stock
    process_order(Order(
        order_id="ORD-002",
        item="monitor",
        quantity=2,
        payment_method="credit_card",
        amount=499.00,
        shipping_address="London",
    ))

    # 3) Fails at Payment — unsupported method
    process_order(Order(
        order_id="ORD-003",
        item="keyboard",
        quantity=3,
        payment_method="bitcoin",
        amount=150.00,
        shipping_address="Tokyo",
    ))

    # 4) Fails at Fraud Detection — amount too high
    process_order(Order(
        order_id="ORD-004",
        item="laptop",
        quantity=2,
        payment_method="paypal",
        amount=25_000.00,
        shipping_address="Berlin",
    ))

    # 5) Fails at Shipping — blocked region
    process_order(Order(
        order_id="ORD-005",
        item="keyboard",
        quantity=1,
        payment_method="debit_card",
        amount=75.00,
        shipping_address="Antarctica",
    ))
