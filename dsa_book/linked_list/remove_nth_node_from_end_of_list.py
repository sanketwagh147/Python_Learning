from typing import Optional


class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


class Solution:
    def removeNthFromEnd(self, head: Optional[ListNode], n: int) -> Optional[ListNode]:

        dummy = ListNode(0, head)
        p1 = p2 = dummy

        # p1 should be ahead by n + 1
        # This step is did so that when p1 is None ( or at end)
        # p2 (if both moved in same pace) will be at the previous pos of node which is to be deleted
        for _ in range(n + 1):
            p1 = p1.next

        # Once p1 is None this means p2 points to previous node which is to be deleted
        while p1:
            # Move both at same pace till p1 hits the end
            p1, p2 = p1.next, p2.next

        # point the previous node to the next node which is to be deleted
        temp = p2.next
        p2.next = p2.next.next
        temp.next = None

        return dummy.next
