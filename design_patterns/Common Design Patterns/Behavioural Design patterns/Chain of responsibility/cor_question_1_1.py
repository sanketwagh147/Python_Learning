
from __future__ import annotations
from abc import ABC
from enum import StrEnum, auto
from functools import wraps


def log_escalation_level(fn):

    @wraps(fn)
    def wrapper(*args, **kwargs):
        escalation_level = args[1] if len(args) > 1 else kwargs.get("escalation_level")
        print(f"[{fn.__qualname__}] Handling escalation level: {escalation_level}")
        return fn(*args, **kwargs)

    return wrapper
    
class EscalationLevel(StrEnum):
    BASIC = auto()
    TECHNICAL = auto()
    MANAGERIAL = auto()


class Handler(ABC):
    def __init__(self, next_handler: Handler | None = None) -> None:
        self.next_process = next_handler

    @log_escalation_level
    def handle(self, escalation_level:EscalationLevel):

        if self.next_process:
            return self.next_process.handle(escalation_level)
        return "No Handler available"


class BasicSupport(Handler):
    @log_escalation_level
    def handle(self, escalation_level):
        if escalation_level == EscalationLevel.BASIC:
            return "Basic Support: Resolved the issue"

        return super().handle(escalation_level)

class TechnicalSupport(Handler):

    @log_escalation_level
    def handle(self, escalation_level):
        if escalation_level == EscalationLevel.TECHNICAL:
            return "Tech Support: Resolved the issue"

        return super().handle(escalation_level)

class ManagerSupport(Handler):
    @log_escalation_level
    def handle(self, escalation_level):
        if escalation_level == EscalationLevel.MANAGERIAL:
            return "Manager: Resolved the issue"

        return super().handle(escalation_level)



if __name__ == "__main__": 
    
    chain = BasicSupport(TechnicalSupport(ManagerSupport()))
    print(chain.handle(EscalationLevel.MANAGERIAL))
    print("---".center(50, "-"))
    print(chain.handle(EscalationLevel.BASIC))
    print("---".center(50, "-"))
    print(chain.handle(EscalationLevel.TECHNICAL))



