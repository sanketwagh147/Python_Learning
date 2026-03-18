"""
Liskov Substitution Principle (LSP) — Practical Example

Scenario: An order-notification system that broadcasts through multiple channels
(email, SMS, push, fax). Each channel has its own recipients configured at
construction time (emails, phone numbers, device tokens, fax numbers), while the
Notification object carries only the MESSAGE CONTENT.

This cleanly separates WHO receives from WHAT is sent, so broadcast() just
calls sender.send(notification) on every sender — true Liskov substitution.

Key LSP idea:
    broadcast() accepts list[NotificationSender].
    ANY subclass can be dropped in — or swapped out — without touching
    the broadcast logic.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field


# ── Notification — pure message content ────────────────────────────
# No recipient info here. Each SENDER knows its own recipients.


@dataclass
class Notification:
    body: str  # plain-text body (all channels use this)
    subject: str = ""  # used by email, fax
    html_body: str = ""  # email-specific rich body
    title: str = ""  # push-specific title
    image_url: str = ""  # push-specific image


# ── Base class (the contract) ─────────────────────────────────────


class NotificationSender(ABC):
    """
    Contract every subclass must honour:
        send(notification) -> bool
        - Accept any Notification without adding stricter preconditions.
        - Return True on success, False on failure.
        - Never raise for input that the base class would accept.

        can_send(notification) -> bool
        - Override to declare channel-specific requirements.
        - Base implementation returns True (no extra requirements).
    """

    def can_send(self, notification: Notification) -> bool:
        """Override to declare channel-specific requirements."""
        return True

    @abstractmethod
    def send(self, notification: Notification) -> bool: ...


# ── Subtypes that HONOUR the contract (LSP ✔) ────────────────────


class EmailSender(NotificationSender):
    """Configured with its own to/cc/bcc email addresses."""

    def __init__(
        self,
        to: list[str],
        cc: list[str] | None = None,
        bcc: list[str] | None = None,
    ):
        self.to = to
        self.cc = cc or []
        self.bcc = bcc or []

    def send(self, notification: Notification) -> bool:
        print(f"[Email]  To: {', '.join(self.to)}")
        if self.cc:
            print(f"         Cc: {', '.join(self.cc)}")
        if self.bcc:
            print(f"         Bcc: {', '.join(self.bcc)}")
        content = notification.html_body or notification.body
        print(f"         Subject: {notification.subject}")
        print(f"         Body: {content}")
        return True


class SmsSender(NotificationSender):
    """Configured with phone numbers. Uses only the plain-text body."""

    def __init__(self, phone_numbers: list[str]):
        self.phone_numbers = phone_numbers

    def send(self, notification: Notification) -> bool:
        for phone in self.phone_numbers:
            print(f"[SMS]    To: {phone} | {notification.body}")
        return True


class PushNotificationSender(NotificationSender):
    """Configured with device tokens. Uses title, body, and optional image."""

    def __init__(self, device_tokens: list[str]):
        self.device_tokens = device_tokens

    def send(self, notification: Notification) -> bool:
        for token in self.device_tokens:
            print(f"[Push]   Device: {token}")
            print(f"         Title: {notification.title or notification.subject}")
            print(f"         Body: {notification.body}")
            if notification.image_url:
                print(f"         Image: {notification.image_url}")
        return True


class FaxSender(NotificationSender):
    """
    Correct Fax implementation that respects LSP:
    - Configured with fax numbers at construction time.
    - Declares its requirement (subject) via can_send() — caller decides what to do.
    - send() returns False if requirement isn't met (no exception).
    - Returns bool as promised.
    """

    def __init__(self, fax_numbers: list[str]):
        self.fax_numbers = fax_numbers

    def can_send(self, notification: Notification) -> bool:
        return bool(notification.subject)

    def send(self, notification: Notification) -> bool:
        if not notification.subject:
            print("[Fax]    ⚠ Skipped — fax requires a subject")
            return False
        for fax_number in self.fax_numbers:
            print(f"[Fax]    To: {fax_number}")
            print(f"         Subject: {notification.subject}")
            print(f"         Body: {notification.body}")
        return True


# ── Client code — relies ONLY on the base type ────────────────────


def broadcast(senders: list[NotificationSender], notification: Notification):
    """
    Works with ANY NotificationSender — that's LSP in action.
    Uses can_send() to check requirements before attempting delivery.
    Add a new channel tomorrow (Slack, WhatsApp, …) and this function
    doesn't change at all.
    """
    for sender in senders:
        if not sender.can_send(notification):
            print(f"  ⚠ {sender.__class__.__name__} skipped (missing required fields)")
            print()
            continue
        success = sender.send(notification)
        if not success:
            print(f"  ⚠ Failed via {sender.__class__.__name__}")
        print()


# ── BAD subtype that VIOLATES LSP ─────────────────────────────────


class BrokenFaxSender(NotificationSender):
    """
    Violates LSP because:
    1. Strengthens preconditions — demands subject AND rejects short bodies.
       (The base class accepts any valid Notification.)
    2. Returns a string instead of bool, breaking the caller's 'if not success' check.
    """

    def __init__(self, fax_numbers: list[str]):
        self.fax_numbers = fax_numbers

    def send(self, notification: Notification):
        if not notification.subject:
            raise ValueError("Fax requires a subject")  # stricter precondition
        if len(notification.body) < 50:
            raise ValueError(
                "Fax body must be ≥ 50 characters"
            )  # stricter precondition
        for fax_number in self.fax_numbers:
            print(f"[Fax]    To: {fax_number} | {notification.body}")
        return "sent"  # wrong return type — caller expects bool


# ── Demo ───────────────────────────────────────────────────────────

if __name__ == "__main__":
    # Each sender is configured with its OWN recipients
    email = EmailSender(
        to=["alice@example.com", "bob@example.com"],
        cc=["manager@example.com"],
        bcc=["audit-log@example.com"],
    )
    sms = SmsSender(phone_numbers=["+1-555-0101", "+1-555-0202"])
    push = PushNotificationSender(device_tokens=["device-token-abc123"])
    fax = FaxSender(fax_numbers=["+1-555-9000"])

    # The Notification is JUST the content — no recipients here
    order_shipped = Notification(
        subject="Your order #1042 has shipped!",
        body="Your package is on its way.",
        html_body="<h1>Shipped!</h1><p>Your package is on its way.</p>",
        title="Order Shipped 📦",
        image_url="https://img.example.com/shipped.png",
    )

    print("=" * 60)
    print("  GOOD EXAMPLE — LSP respected")
    print("  broadcast() sends the SAME notification to ALL channels")
    print("=" * 60, "\n")

    # All four channels in one broadcast — each sender uses its own
    # recipients and picks the notification fields relevant to it.
    broadcast([email, sms, push, fax], order_shipped)

    # ── Minimal notification (no subject, short body) ──────────────
    # Every good sender handles this gracefully (LSP ✔).
    # BrokenFaxSender would crash here (LSP ✘).
    print("-" * 60)
    print("  Minimal notification — all good senders still work fine")
    print("-" * 60, "\n")

    minimal = Notification(body="Hi!")
    broadcast([email, sms, push, fax], minimal)

    # ── BAD example ────────────────────────────────────────────────
    print("=" * 60)
    print("  BAD EXAMPLE — LSP violated by BrokenFaxSender")
    print("=" * 60, "\n")

    try:
        broken_fax = BrokenFaxSender(fax_numbers=["+1-555-9000"])
        broadcast([email, broken_fax], minimal)
    except ValueError as e:
        print(f"  💥 LSP violation: {e}")
        print(
            "     BrokenFaxSender imposed stricter preconditions than the base class."
        )
        print(
            "     Compare with FaxSender above — it handled the same notification fine."
        )
