"""
Reorder list 
Leetcode 143
"""

from typing import Optional

from dsa_book.common.nodes import ListNode


class Solution:
    def reorderList(self, head: Optional[ListNode]) -> None:
        """
        Do not return anything, modify head in-place instead.
        """
        # curr = head
        slow, fast = head, head

        # 1️⃣ find the mid point
        while fast and fast.next:

            slow = slow.next
            fast = fast.next.next

        # 2️⃣ Rev the second half
        prev = None
        current = slow.next

        # 2️⃣ Rev the second half
        slow.next = None  #! Cut the list into half

        while current:
            next_node = current.next

            current.next = prev

            prev = current
            current = next_node

        # REVIEW : Merge two lists by alternating nodes?
        # 3️⃣ Merge first half and reversed second half
        # print(slow)

        first, second = head, prev

        while second:
            # 3️⃣🅰️  Save next of both in temp variables
            first_next = first.next
            second_next = second.next

            # 3️⃣🅱️ point next to alternate lists
            first.next = second
            second.next = first_next

            # 3️⃣🅱️  move to next node
            first = first_next
            second = second_next


if __name__ == "__main__":
    from dsa_book.common.builders import linked_list_builder

    l1 = linked_list_builder([1, 2, 3, 4, 5])
    s = Solution()
    s.reorderList(l1)
    op = linked_list_builder([1, 5, 2, 4, 3])
    l1.print_list()
    op.print_list()
