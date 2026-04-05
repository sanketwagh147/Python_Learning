
from __future__ import annotations

from dataclasses import dataclass
from abc import ABC

from enum import auto, StrEnum


class Severity(StrEnum):
    LOW = auto()
    MEDIUM = auto()
    HIGH = auto()
    CRITICAL = auto()

class Status(StrEnum):
    OPEN = auto()
    IN_PROGRESS = auto()
    RESOLVED = auto()
    CLOSED = auto()

@dataclass
class Ticket:
    id: str
    severity: Severity
    issue: str
    status: Status = Status.OPEN


class SupportHandler(ABC):
    def __init__(self, next_handler: SupportHandler | None = None) -> None:
        self.next_handler = next_handler

    def handle(self, ticket: Ticket):
        if self.next_handler:
            return self.next_handler.handle(ticket)
        return "Ticket escalated to management"

    def set_next(self, handler : SupportHandler):
        self.next_handler = handler
        return handler

class BasicSupport(SupportHandler):
    def handle(self, ticket: Ticket):
        if ticket.severity == Severity.LOW:
            ticket.status = Status.RESOLVED
            return f"[Basic Support] Resolved {ticket.id}: {ticket.issue}"

        return super().handle(ticket)

class TechnicalSupport(SupportHandler):
    def handle(self, ticket: Ticket):
        if ticket.severity == Severity.MEDIUM:
            ticket.status = Status.RESOLVED
            return f"[Technical Support] Resolved {ticket.id}: {ticket.issue}"

        return super().handle(ticket)

class ManagerSupport(SupportHandler):
    def handle(self, ticket: Ticket):
        if ticket.severity == Severity.HIGH:
            ticket.status = Status.RESOLVED
            return f"[Manager] Resolved {ticket.id}: {ticket.issue}"

        return super().handle(ticket)

class CEOSupport(SupportHandler):
    def handle(self, ticket: Ticket):
        if ticket.severity == Severity.CRITICAL:
            ticket.status = Status.RESOLVED
            return f"[CEO] Resolved {ticket.id}: {ticket.issue}"

        return super().handle(ticket)

if __name__ == "__main__": 
    
    sample_tickets = [
        Ticket(id="T1", severity=Severity.LOW, issue="Password reset"),
        Ticket(id="T2", severity=Severity.MEDIUM, issue="Software installation"),
        Ticket(id="T3", severity=Severity.HIGH, issue="System outage"),
        Ticket(id="T4", severity=Severity.CRITICAL, issue="Data breach"),]

    basic_handler = BasicSupport()
    technical_handler = TechnicalSupport()
    manager_handler = ManagerSupport()

    basic_handler.set_next(technical_handler).set_next(manager_handler)
    for ticket in sample_tickets:
        result = basic_handler.handle(ticket)
        print(result)
    
    if len(sample_tickets) > 0:
        print("\nEscalating unresolved tickets to CEO...\n")

    print("Reopening ticket T1 for further investigation...")
    sample_tickets[3].status = Status.IN_PROGRESS

    for ticket in sample_tickets:
        ceo_handler = CEOSupport()
        if ticket.status == Status.IN_PROGRESS:
            ticket.severity = Severity.LOW
            basic_handler.set_next(basic_handler)
            basic_handler.handle(ticket)

            print(f"Ticket {ticket.id} is in progress,  back to Basic Support for resolution.")

        if ticket.status != Status.RESOLVED :
            result = ceo_handler.handle(ticket)
            print(result)

    for ticket in sample_tickets:
        print(f"Ticket {ticket.id} - Status: {ticket.status}")
