from typing import Optional

from common.nodes import Node as ListNode


class Solution:
    def removeElements(self, head: Optional[ListNode], val: int) -> Optional[ListNode]:

        # Add dummy node at start
        pre_dummy = ListNode(0)
        pre_dummy.next = head

        # Set the curr to the dummy node
        curr = pre_dummy

        # We work on curr on next as we get the next value and well as curr value
        while curr.next:

            if curr.next.val == val:
                curr.next = curr.next.next
            else:
                curr = curr.next

        return pre_dummy.next
