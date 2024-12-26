"""
Implement array queue
"""

import unittest

from dsa_book.dsa_wiley.array_stack import EmptyException


class ArrayQueue:
    """
    FIFO Queues using lists
    """

    def __init__(self, max_capacity: int = 5, empty_err_msg="Queue is empty") -> None:

        self._data = [None] * max_capacity
        self._size = 0
        self._front = 0
        self._empty_err_msg = empty_err_msg

    def __len__(self):
        return self._size

    def is_empty(self):
        """Return True if queue is empty"""
        return True if self._size == 0 else False

    def first(self):
        """Returns first element on the queue (does not remove it)"""

        if self.is_empty():
            raise EmptyException("Queue is empty")
        return self._data[self._front]

    def dequeue(self):
        """Remove and return first element of the queue"""

        if self.is_empty():
            raise EmptyException(self._empty_err_msg)

        front = self._data[self._front]
        self._front = (self._front + 1) % len(self._data)  # makes index always
        self._size -= 1
        return front

    def _resize(self, new_cap):
        """Resize to new capacity"""
        old = self._data
        self._data = [None] * new_cap
        walk = self._front

        for k in range(self._size):
            self._data[k] = old[walk]
            walk = (walk + 1) % len(old)
        self._front = 0

    def enqueue(self, ele):
        if self._size == len(self._data):
            self._resize(2 * len(self._data))

        avail = (self._front + self._size) % len(self._data)
        self._data[avail] = ele
        self._size += 1

    def __eq__(self, value: object) -> bool:
        """
        Checks for equality
        """
        if not isinstance(value, ArrayQueue):
            raise ValueError("Object should be a valid Array queue to compare")

        if self._size != value._size:
            return False

        for i in range(self._size):
            if self._data[i] != value._data[i]:
                return False

        return True


if __name__ == "__main__":

    class TestArrayQueue(unittest.TestCase):

        def test_is_empty(self):
            aq = ArrayQueue()

            self.assertEqual(aq.is_empty(), True, "is_empty method is failing")

        def test_first(self):
            aq = ArrayQueue()
            aq.enqueue(1)
            self.assertEqual(aq.first(), 1, "Queue first is incorrect")

        def test_enqueu_one(self):
            aq = ArrayQueue()
            aq.enqueue(100)
            self.assertEqual(aq._data, [100, None, None, None, None])

        def test_enqueue_full(self):

            aq = ArrayQueue(10)
            for i in range(10):
                aq.enqueue(i)

            self.assertEqual(
                aq._data, [0, 1, 2, 3, 4, 5, 6, 7, 8, 9], "Enqueue method failure"
            )

        def test_dequeue(self):

            aq = ArrayQueue(10)
            for i in range(10):
                aq.enqueue(i)

            aq.dequeue()

            self.assertEqual(
                aq._data, [0, 1, 2, 3, 4, 5, 6, 7, 8, 9], "Enqueue method failure"
            )

    unittest.main()
