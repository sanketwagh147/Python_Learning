"""
LIFO stack implementation using a singly linked list for storage
"""

from dataclasses import dataclass
from enum import Enum
from typing import Generic, TypeVar, Union


class ExceptionMsgEnum(str, Enum):
    EMPTY_STACK = "The Stack is empty"


class StackException(Exception): ...


class EmptyStackException(StackException):
    _EMPTY_STACK_MSG = ExceptionMsgEnum.EMPTY_STACK

    def __init__(self, msg: str = _EMPTY_STACK_MSG, *args) -> None:
        super().__init__(msg, *args)


# This
GenericNode = TypeVar("GenericNode")


@dataclass
class Node(Generic[GenericNode]):
    value: GenericNode
    next: Union["Node[GenericNode]", None] = None

    def __str__(self) -> str:
        return f"<Node : {self.value} {'-> ' if self.next else ''} {self.next if self.next else ''}>"


class LinkedStack:

    def __init__(self) -> None:
        self._head = None
        self._size = 0

    def __len__(self):
        "Return num elements in the stack"
        return self._size

    def is_empty(self):
        """Returns true if stack size is 0"""
        return self._size == 0

    def push(self, node: Node[int]):
        """push element to the top of a stack"""

        # 1 Create a new Node
        new_node = Node(node, self._head)

        # 2 Now the head is the new node

        self._head = new_node
        self._size += 1

    def top(self):
        """Only returns the top element and doesn't remove it"""

        if self.is_empty():
            raise EmptyStackException()

        # top is head of stack
        return self._head.value  # type: ignore

    def pop(self):
        """Removes from top of  stack LIFO"""

        if self.is_empty():
            raise EmptyStackException()

        # Item to be popped is the head
        top_element = self._head.value  # type: ignore

        # new head is the next of current head which will be popped
        self._head = self._head.next  # type: ignore
        self._size -= 1
        return top_element


if __name__ == "__main__":
    ls = LinkedStack()
    nn1: Node[int] = Node(20, None)
    nn2: Node[int] = Node(30, None)
    nn3: Node[int] = Node(40, None)
    nn4: Node[int] = Node(50, None)
    nn5: Node[int] = Node(60, None)
    nn6: Node[int] = Node(70, None)

    ls.push(nn1)
    ls.push(nn2)
    ls.push(nn3)
    ls.push(nn4)
    ls.push(nn5)
    ls.push(nn6)
    print(ls.pop())
    print(ls.pop())
    print(ls.pop())
    print(ls.pop())
    print(ls.pop())
    print(ls.pop())
