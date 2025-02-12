from typing import Optional

from dsa_book.common.builders import linked_list_builder
from dsa_book.common.nodes import Node as ListNode


class Solution:
    def reverseList(self, head: Optional[ListNode]) -> Optional[ListNode]:

        # set prev to None
        prev = None
        curr = head

        while curr:
            # Saves the next node
            next_node = curr.next

            curr.next = prev

            # next iteration
            prev = curr
            curr = next_node

        return prev


if __name__ == "__main__":
    l1 = linked_list_builder([1, 2, 3, 4, 5])
    s = Solution()
    print(s.reverseList(l1))
