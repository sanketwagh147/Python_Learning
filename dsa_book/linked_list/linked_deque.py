"""Linked Deque"""

from dsa_book.common.exceptions import EmptyException, InvalidNodeException
from dsa_book.common.nodes import DNode
from dsa_book.linked_list.doubly_linked_list_base import _DoublyLinkedListBase


class LinkedDeque(_DoublyLinkedListBase):
    """Double end implementation of a queue based on Doubly linked list"""

    def first(self):
        """Returns first node without removing"""

        if self.is_empty():
            raise EmptyException(f"{self.__class__.__name__} is empty")

        if not isinstance(self._header.next, DNode):
            raise InvalidNodeException("Invalid Node")

        return self._header.next.value

    def last(self):
        """Returns last node without removing"""

        if self.is_empty():
            raise EmptyException(f"{self.__class__.__name__} is empty")

        if not isinstance(self._trailer.prev, DNode):
            raise InvalidNodeException("Invalid Node")

        return self._trailer.prev.value

    def insert_first(self, value):
        """Adds element to front of the deque"""
        self._insert_between(value, self._header, self._header.next)

    def insert_last(self, value):
        """Adds element to back of the deque"""
        self._insert_between(value, self._trailer.prev, self._trailer)

    def delete_first(self):
        if self.is_empty():
            raise EmptyException(f"{self.__class__.__name__} is empty")

        if not isinstance(self._header.next, DNode):
            raise InvalidNodeException("Invalid Node")
        return self._delete_node(self._header.next)

    def delete_last(self):
        if self.is_empty():
            raise EmptyException(f"{self.__class__.__name__} is empty")

        if not isinstance(self._trailer.prev, DNode):
            raise InvalidNodeException("Invalid Node")
        return self._delete_node(self._trailer.prev)


if __name__ == "__main__":
    ldq = LinkedDeque()
    ldq.insert_first(10)
    ldq.insert_first(9)
    ldq.insert_last(100)
    ldq.insert_last(101)
    print(ldq)
