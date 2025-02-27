"""
Module which generates Linked list from list of values for testing purposes
"""

from dataclasses import dataclass
from typing import Any, NamedTuple, Optional

from dsa_book.common.nodes import ListNode


def linked_list_builder(values: list) -> Optional[ListNode]:
    """
    Function to build a linked list from list of values
    """
    if not values:
        return None

    # Create head from first element

    head = ListNode(values[0])
    current = head

    # Iterate from the second element
    for value in values[1:]:
        current.next = ListNode(value)
        current = current.next

    return head


@dataclass
class TestCase_:
    name: str
    inp: dict[str, Any]
    op: Any
    details: str | None = ""


class TestCase(NamedTuple):
    """Named tuple  for test cases"""

    name: str
    params: dict[str, Any]
    expected: Any
    description: str = ""
