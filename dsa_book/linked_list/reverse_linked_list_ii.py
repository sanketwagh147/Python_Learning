"""
Leet code 92 reverse linked list 2
"""

from typing import Optional

from dsa_book.common.nodes import ListNode


class Solution:
    def reverseBetween(
        self, head: Optional[ListNode], left: int, right: int
    ) -> Optional[ListNode]:

        # no need to reverse if empty and l and r are equal
        if not head or left == right:
            return head

        dummy = ListNode(0, head)
        dummy.next = head
        prev = dummy

        # move prev to left - 1
        for _ in range(left - 1):
            prev = prev.next

        curr = prev.next
        next_node = None

        for _ in range(right - left):
            next_node = curr.next

            curr.next = next_node.next

            next_node.next = prev.next

            prev.next = next_node

        return dummy.next

    def rev_list(self, head):

        prev = None
        curr = head

        while curr:
            next = curr.next
            curr.next = prev

            prev = curr

            curr = next

        return prev


if __name__ == "__main__":
    from dsa_book.common.builders import linked_list_builder

    l1 = linked_list_builder([1, 2, 3, 4, 5])
    s = Solution()
    s.reverseBetween(l1, 2, 4).print_list()
    # s.rev_list(l1).print_list()
