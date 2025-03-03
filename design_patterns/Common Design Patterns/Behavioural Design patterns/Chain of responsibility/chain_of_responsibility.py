"""
Chain of responsibility Design pattern
"""

from typing import Any


class Event(list):
    """
    A list of functions to call
    """

    def __call__(self, *args: Any, **kwds: Any) -> Any:
        for item in self:
            item(*args, **kwds)
