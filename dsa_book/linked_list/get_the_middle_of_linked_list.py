from typing import Optional

from dsa_book.common.builders import linked_list_builder
from dsa_book.common.nodes import ListNode


class Solution:
    def middleNode(self, head: Optional[ListNode[int]]) -> ListNode:

        slow = fast = head

        while fast and fast.next:
            slow = slow.next
            fast = fast.next.next

        return slow


if __name__ == "__main__":
    l1 = linked_list_builder([1, 2])
    l2 = linked_list_builder([1, 2, 2, 1])
    l3 = linked_list_builder([3, 1, 3, 3, 1, 3])
    l3 = linked_list_builder([1, 2, 3, 4, 5, 6, 7])
    so = Solution()
    print(so.middleNode(l1))
    print(so.middleNode(l2))
    print(so.middleNode(l3))
