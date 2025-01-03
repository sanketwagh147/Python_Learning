"""Implementation of a stack using LL"""

from dsa_book.common.nodes import Node


class Stack:
    def __init__(self, value) -> None:
        new_node = Node(value)
        self.top = new_node
        self.height = 1

    def print_stack(self):
        temp = self.top
        while temp is not None:
            print(temp.value)
            temp = temp.next

    def push(self, value):
        new_node = Node(value)

        if self.height == 0:
            self.top = new_node
        else:
            new_node.next = self.top
            self.top = new_node
        self.height += 1

    def pop(self):
        if self.height == 0:
            return None
        else:
            temp = self.top
            self.top = self.top.next  # type: ignore
            temp.next = None  # type: ignore
        self.height -= 1
        return temp


if __name__ == "__main__":
    stack = Stack(1)
    stack.push(2)
    stack.push(3)
    print(stack.pop())
    stack.push(4)
    stack.print_stack()
