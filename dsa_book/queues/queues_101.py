"""
Queue
"""

from dsa_book.common.nodes import Node


class Queue:
    def __init__(self, value) -> None:
        new_node = Node(value)
        self.first = new_node
        self.last = new_node
        self.length = 1

    def print_queue(self):
        temp = self.first
        while temp is not None:
            print(temp.value)
            temp = temp.next

    def enqueue(self, value):
        new_node = Node(value)

        if self.length == 0:
            self.first = self.last = new_node

        else:
            self.last.next = new_node
            self.last = new_node

        self.length += 1

    def deque(self):
        if self.length == 0:
            return None
        temp = self.first
        if self.length == 1:
            self.first = self.last = None
        else:
            self.first = self.first.next
            temp.next = None

        self.length -= 1

        return temp


if __name__ == "__main__":
    my_que = Queue(3)
    my_que.enqueue(2)
    my_que.enqueue(1)
    my_que.enqueue(1)
    print(my_que.deque())
    my_que.print_queue()
