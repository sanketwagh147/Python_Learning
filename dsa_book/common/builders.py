"""
Module which generates Linked list from list of values for testing purposes
"""

from collections import namedtuple
from dataclasses import dataclass
from typing import Any, Optional

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


TestCase = namedtuple("TestCase", ["name", "params", "expected", "description"])
TestCase.__doc__ = """Represents a test case.

Fields:
- name (str): The identifier of the test case.
- params (dict): The input parameters.
- expected (Any): The expected output.
- description (str): A short description of the test case.
"""
