"""
Leet code problem 82 : Remove duplicates from sorted linked list 2
"""

from typing import Optional

from dsa_book.common.builders import linked_list_builder
from dsa_book.common.nodes import ListNode


class Solution:
    def deleteDuplicates(self, head: Optional[ListNode[int]]) -> Optional[ListNode]:

        # create dummy and make next as head
        dummy = ListNode(0, head)

        # previous node becomes a dummy node
        prev = dummy

        while head:
            if head.next and head.val == head.next.val:

                # Skip all nodes with same val
                while head.next and head.val == head.next.val:
                    head = head.next

                prev.next = head.next
            else:
                prev = prev.next

            head = head.next

        return dummy.next


if __name__ == "__main__":
    l1 = linked_list_builder([1, 2, 3, 3, 4, 4, 5])
    l2 = linked_list_builder([1, 1, 1, 2, 3])
    s = Solution()
    s.deleteDuplicates(l1).print_list()
    s.deleteDuplicates(l2).print_list()
