"""
FIFO queue
"""

from dsa_book.dsa_wiley.array_stack import EmptyException


class Queue:
    """
    FIFO
    add to right of the list and removes from left of the list
    """

    def __init__(self, capacity=10) -> None:

        self._queue = [None] * capacity

        self._fi = 0
        self._size = 0
        self._bi = -1  # states list is empty
        self._capacity = capacity

    @property
    def first(self):
        if self.is_empty:
            raise EmptyException("Queue is empty")
        return self._queue[self._fi]

    @property
    def get_size(self):
        return self._size

    @property
    def capacity(self):
        return self._capacity

    @property
    def is_empty(self):
        return self._size == 0

    def enqueue(self, data):
        """
        Adds to the back of the list
        """

        if self._size == self._capacity:
            print("Queue is full")
            return

        self._bi = (self._bi + 1) % self._capacity
        self._queue[self._bi] = data

        self._size += 1

    def deque(self):
        if self.is_empty:
            print("Empty queue")
            return

        data = self._queue[self._fi]
        self._queue[self._fi] = None  # Reset
        self._fi = (self._fi + 1) % self._capacity
        self._size -= 1
        return data

    def display_queue(self):
        print(self._queue)


if __name__ == "__main__":
    qu = Queue()
    qu.enqueue(1)
    qu.enqueue(2)
    qu.enqueue(3)
    qu.deque()
    # qu.deque()
    qu.display_queue()
    print(qu._fi)
    print(qu._bi)
