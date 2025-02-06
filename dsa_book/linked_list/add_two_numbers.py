from typing import Optional


class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


class Solution:
    def addTwoNumbers(
        self, l1: Optional[ListNode], l2: Optional[ListNode]
    ) -> Optional[ListNode]:

        res = ListNode()
        curr = res

        # Iterate only when any one is not None
        carry = 0
        while l1 or l2 or carry:
            print("looping")

            v1 = l1.val if l1 else 0
            v2 = l2.val if l2 else 0
            total = v1 + v2 + carry
            carry = total // 10
            # 11 // 10 = 1
            curr.next = ListNode(total % 10)
            # 15 % 10 = 5
            curr = curr.next

            if l1:
                l1 = l1.next
            if l2:
                l2 = l2.next
        return res.next


# @lc code=end


if __name__ == "__main__":
    l1 = ListNode(2, ListNode(4, ListNode(3)))
    l2 = ListNode(5, ListNode(6, ListNode(4, ListNode(9))))
    s = Solution()
    s.addTwoNumbers(l1, l2)
