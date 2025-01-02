"""FIFO singly list list"""

from typing import Union

from dsa_book.common.exceptions import EmptyException, InvalidNodeException
from dsa_book.common.nodes import Node


class LinkedQueue:
    """Fifo"""

    def __init__(self) -> None:
        self._head: Union[Node, None] = None
        self._tail: Union[Node, None] = None
        self._size = 0

    def __len__(self):
        return self._size

    def is_empty(self):
        """Returns empty if the queues is empty"""

        return self._size == 0

    def first(self):
        """Return first element but does not remove it"""
        if self.is_empty():
            raise EmptyException

        if self._head is not None:
            return self._head.value

        raise InvalidNodeException

    def deque(self):
        """Remove and return the first element in the queue"""

        if self.is_empty():
            raise EmptyException

        if self._head is None:
            raise InvalidNodeException

        first_node = self._head.value
        self._head = self._head.next
        self._size -= 1

        # if the stack is empty clear the tail
        if self.is_empty():
            self._tail = None

        return first_node

    def enqueue(self, new_node: Node):

        # if empty this will also be the head
        if self.is_empty():
            self._head = new_node
            self._tail = new_node
        else:
            if self._tail is None:
                raise InvalidNodeException

            self._tail.next = new_node
        self._tail = new_node
        self._size += 1


if __name__ == "__main__":
    lq = LinkedQueue()
    n1 = Node(10)
    n2 = Node(2)
    n3 = Node(3)
    lq.enqueue(n1)
    lq.enqueue(n2)
    lq.enqueue(n3)
    print(lq.deque())
    print(lq.deque())
    print(lq.deque())
