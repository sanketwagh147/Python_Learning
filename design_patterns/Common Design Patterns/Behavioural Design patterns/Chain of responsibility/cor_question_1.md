# Chain of Responsibility — Question 1 (Easy)

## Problem: Customer Support Ticket Router

Tickets arrive with a severity level. Route each ticket to the appropriate support tier.

### Requirements

- `SupportHandler(ABC)`: `handle(ticket: dict)`, `set_next(handler) -> handler`
- **Tier 1 (Basic Support)**: handles severity "low" — password resets, FAQ questions
- **Tier 2 (Technical Support)**: handles severity "medium" — bugs, integration issues
- **Tier 3 (Engineering)**: handles severity "high" — outages, data loss
- **Fallback**: if no handler matches, print "Ticket escalated to management"

### Expected Usage

```python
tier1 = BasicSupport()
tier2 = TechnicalSupport()
tier3 = Engineering()
tier1.set_next(tier2).set_next(tier3)

tier1.handle({"id": "T001", "severity": "low", "issue": "Reset password"})
# → [Basic Support] Resolved T001: Reset password

tier1.handle({"id": "T002", "severity": "high", "issue": "Database outage"})
# → [Engineering] Resolved T002: Database outage

tier1.handle({"id": "T003", "severity": "critical", "issue": "Unknown"})
# → Ticket T003 escalated to management
```

### Constraints

- Use `set_next()` with method chaining (return the next handler for fluent API).
- Each handler ONLY handles its severity — everything else passes to next.
