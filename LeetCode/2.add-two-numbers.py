# # @lc app=leetcode id=2 lang=python3
#
# [2] Add Two Numbers
#

# @lc code=start
# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next
from typing import DefaultDict


class Solution:
    def addTwoNumbers(self, l1: Optional[ListNode], l2: Optional[ListNode]) -> Optional[ListNode]:
        result = ListNode()
        pointer = result
        quotient = 0
    # ! This is shitty
    # * This is importtant
    # Todo: This must be don
    # ? IDK whtf is this
        while l1 or l2:
            if l1 and l2:
                curSum = l1.val + l2.val + quotient
                l1 = l1.next
                l2 = l2.next

            elif l1 and not l2:
                curSum = l1.val + quotient
                l1 = l1.next

            elif not l1 and l2:
                curSum = l2.val + quotient
                l2 = l2.next

            if curSum >= 10: # if there is overflow the sum
                remainder = curSum % 10
                quotient = 1 # quotient is always 1 because the max sum is 9+9 only
                pointer.next = ListNode(remainder)

            else:
                pointer.next = ListNode(curSum)
                quotient = 0 # reset the quotient

            pointer = pointer.next

        if quotient != 0: # if there is overflow on the length of our linked list
            pointer.next = ListNode(quotient)

        return result.next

# @lc code=end

