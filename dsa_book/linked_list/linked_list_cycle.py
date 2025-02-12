"""
Leet code 141. Linked List Cycle : https://leetcode.com/problems/linked-list-cycle/
"""

import sys
from typing import Optional

from icecream import ic

from dsa_book.common import builders
from dsa_book.common.nodes import Node as ListNode

print(sys.path)


class Solution:
    def hasCycle(self, head: Optional[ListNode]) -> bool:

        # Two nodes one fast and one slow
        fast = head

        while fast and fast.next:

            head = head.next
            fast = fast.next.next

            # If they meet there is a cycle
            if head is fast:
                ic("Linked List has a cycle")

                return True

        ic("Linked List does not have a cycle")
        return False


if __name__ == "__main__":

    l1 = builders.linked_list_builder([3, 2, 0, -4])
    sol = Solution()
    sol.hasCycle(l1)

    # Generate some linked list with cycle
    l1.next.next.next.next = l1.next
    sol.hasCycle(l1)
