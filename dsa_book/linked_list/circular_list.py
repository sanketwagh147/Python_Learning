"""Circular linked list"""

from graphviz import Digraph

from dsa_book.common.nodes import Node


class CircularList:

    def __init__(self) -> None:
        """Constructs circular linked list"""
        self.head = None
        self.length = 0

    def _insert(self, index, value):
        """Insert value at a given index"""

        if index < 0 or index > self.length:
            raise IndexError("Bad Index")

        # Case 1: List is empty first item insersion
        if self.head is None:
            if index != 0:
                raise IndexError("Bad Index")

            new_node = Node(value)
            self.head = new_node
            self.head.next = self.head  # Circular link

        # Case 2: Insert at the end
        elif index == self.length:
            temp = self.head

            # if the temp.next item and end are same it means we are at the end
            while temp.next != self.head:
                temp = temp.next

            # append the new node to last temp and make its next as the head
            temp.next = Node(value, self.head)

        # Case 3: Insert at a specific position
        else:
            temp = self.head
            for _ in range(index - 1):
                # modify the next to point to the next iemp
                temp = temp.next

            temp.next = Node(value, temp.next)

        self.length += 1

    def append(self, value):
        self._insert(self.length, value)

    def print_list(self):
        print(self.head.value, end=" ")
        temp = self.head.next
        while temp != self.head:
            print(temp.value, end=" ")
            temp = temp.next


if __name__ == "__main__":
    cl = CircularList()
    cl.append(1)
    cl.append(2)
    cl.append(5)
    cl.append(5)
    cl.print_list()

    # dot = Digraph()
    # dot.node("A", "1")
    # dot.node("B", "2")
    # dot.node("C", "3")
    # dot.edges(["AB", "BC"])
    # dot.render("linked_list", format="png", view=True)
