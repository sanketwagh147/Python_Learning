"""
Implements a hash set using Linked List
"""

from dsa_book.common.nodes import ListNode


class MyHashSet:

    def __init__(self) -> None:
        self.size = 1000  # bucket size
        self.buckets = [None] * self.size

    def _hash(self, key: int) -> int:
        """Mod the key for int"""
        return key % self.size

    def add(self, key: int) -> None:
        """Add key to hash set"""

        index = self._hash(key)

        if self.buckets[index] is None:
            self.buckets[index] = ListNode(key)
        else:
            curr = self.buckets[index]

            while curr:
                if curr.key == key:

                    return

                if curr.next is None:
                    break

                curr = curr.next

            curr.next = ListNode(key)

    def remove(self, key: int) -> None:
        """Remove key from hash set"""

        index = self._hash(key)
        curr = self.buckets[index]

        if curr is None:
            return

        if curr.key == key:
            self.buckets[index] = curr.next
            return

        prev = None

        while curr:
            if curr.key == key:
                prev.next = curr.next
                return

            prev, curr = curr, curr.next

    def contains(self, key: int) -> bool:
        index = self._hash(key)

        curr = self.buckets[index]

        while curr:

            if curr.key == key:
                return True
            curr = curr.next

        return False
