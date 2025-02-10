"""
Module which generates Linked list from list of values for testing purposes
"""

from typing import Optional

from dsa_book.common.nodes import Node


def linked_list_builder(values: list) -> Optional[Node]:
    """
    Function to build a linked list from list of values
    """
    if not values:
        return None

    # Create head from first element

    head = Node(values[0])
    current = head

    # Iterate from the second element
    for value in values[1:]:
        current.next = Node(value)
        current = current.next

    return head
