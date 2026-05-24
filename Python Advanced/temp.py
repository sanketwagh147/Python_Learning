from typing import Callable

from attr import dataclass
from enum import StrEnum, auto


class Status(StrEnum):
    STARTED = auto()
    FIRST_INNINGS = auto()
    LUNCH = auto()
    SECOND_INNINGS = auto()
    TEA = auto()
    ENDED = auto()


class StatusStore:
    def __init__(self, fn: Callable) -> None:
        self.current_status: Status = Status.STARTED
