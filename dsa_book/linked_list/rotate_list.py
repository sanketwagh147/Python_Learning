"""
Rotate linked list
"""

from typing import Optional

from dsa_book.common.builders import linked_list_builder
from dsa_book.common.nodes import ListNode


class Solution:

    def rotateRight(self, head: Optional[ListNode], k: int) -> Optional[ListNode]:

        if not head or not head.next or k == 0:
            return head

        # finding len of list
        len_list = 1
        tail = head

        while tail.next:
            tail = tail.next
            len_list += 1

        # makes list circular
        tail.next = head

        # handles if k is larger than the list
        k = k % len_list
        print(len_list)
        print(k)

        new_tail = head

        for _ in range(len_list - k - 1):
            new_tail = new_tail.next

        new_head = new_tail.next
        new_tail.next = None
        return new_head


if __name__ == "__main__":
    l1 = linked_list_builder([1, 2, 3, 4, 5])
    s = Solution()
    print(s.rotateRight(l1, 2))
