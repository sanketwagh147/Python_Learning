"""
Swap nodes in pairs for linked list
"""

from typing import Optional

from icecream import ic

from dsa_book.common.builders import linked_list_builder
from dsa_book.common.nodes import ListNode


class Solution:
    def swapPairs(self, head: Optional[ListNode]) -> Optional[ListNode]:

        dummy = ListNode(0)
        dummy.next = head
        prev = dummy

        while head and head.next:

            # set first and second
            first = head
            second = head.next

            # Swap
            prev.next = (
                second  # point previous second as we have to swap second to first
            )
            first.next = second.next
            second.next = first

            # next iteration
            prev = first  # make prev the first node
            head = first.next

        return dummy.next


if __name__ == "__main__":
    l1 = linked_list_builder([1, 2, 3, 4])
    s = Solution()
    print(s.swapPairs(l1))
