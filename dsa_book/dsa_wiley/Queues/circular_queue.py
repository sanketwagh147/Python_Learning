"""Circular Queue Implementation"""


class CircularQueue:
    def __init__(self, max_size: int = 5) -> None:

        self.queue = [None] * max_size
        # increase max size by 1
        max_size += 1
        self.max_size: int = max_size
        self.first = self.last = 0

    def enqueue(self, new_item):
        # checks if queue is full

        if (self.last + 1) % self.max_size == self.first:
            print("Queue is full")
        else:
            self.queue[self.last] = new_item
            self.last = (self.last + 1) % self.max_size

    def deque(self):
        # Check if empty

        if self.find_size() == 0:
            print("Queue is empty")
        else:
            element = self.queue[self.first]
            self.queue[self.first] = None
            self.first = (self.first + 1) % self.max_size
            return element

    def find_size(self):
        """
        Gets no of elements in circular queue
        """
        if self.last >= self.first:
            size = self.last - self.first
        else:
            size = self.max_size - (self.first - self.last)
        return size

    def display_queue(self):
        print(self.first, self.last)
        print(self.queue)


if __name__ == "__main__":
    cq = CircularQueue()
    cq.enqueue(1)
    cq.enqueue(2)
    cq.enqueue(3)
    cq.enqueue(4)
    cq.enqueue(5)
    cq.display_queue()
