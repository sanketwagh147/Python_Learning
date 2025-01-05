"""Base class for doubly linked list with header and tailer"""

from dsa_book.common.exceptions import InvalidNodeException
from dsa_book.common.nodes import DNode, Node


class _DoublyLinkedListBase:

    def __init__(self) -> None:

        # Initialize H 0 1 2 3 T
        self._header = DNode(None, None, None)
        self._trailer = DNode(None, None, None)

        # H <-> T when the list has no elements
        self._header.next = self._trailer
        self._trailer.prev = self._header
        self._size = 0

    def __len__(self):
        return self._size

    def is_empty(self):
        return self._size == 0

    def _insert_between(self, value, before, after):
        """Insert between 2 existing node and return new Node"""

        new_node = DNode(value, after, before)

        before.next = new_node
        after.prev = new_node
        self._size += 1

    def _delete_node(self, node: DNode):
        """Deletes and returns the value"""

        before = node.prev
        after = node.next

        # if not isinstance(before, DNode) or isinstance(after, DNode):
        #     raise InvalidNodeException("Bade Node")

        before.next = after
        after.prev = before
        self._size -= 1
        value = node.value
        node.prev = node.next = node.value = None
        return value

    def __str__(self):
        """Returns a string representation of the doubly linked list."""
        values = []
        current = (
            self._header.next
        )  # Start with the first actual node (after the header)
        while current is not self._trailer:  # Stop at the trailer
            values.append(str(current.value))
            current = current.next
        return " <-> ".join(values)

    def extend(self, ll):
        if ll is None or ll.is_empty():  # Handle empty or None `ll`
            return

        if self.is_empty():  # Handle if `self` is empty
            self._header = ll._header
            self._trailer = ll._trailer
            self._size = ll._size
            return

        # Connect `self`'s trailer to `ll`'s header
        self._trailer.next = ll._header
        ll._header.prev = self._trailer

        # Update `self`'s trailer to `ll`'s trailer
        self._trailer = ll._trailer

        # Update _size
        self._size += ll._size

        # Optionally clear `ll`
        ll._header = ll._trailer = None
        ll._size = 0
