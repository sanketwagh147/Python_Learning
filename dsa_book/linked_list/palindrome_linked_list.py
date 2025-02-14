from typing import Optional

from icecream import ic

from dsa_book.common.builders import linked_list_builder


class Solution:
    def isPalindrome(self, head: Optional[ListNode]) -> bool:

        # empty list of list of single element will always be empty
        if not head or not head.next:
            return True

        # Get the middle of the linked list
        slow, fast = head, head
        while fast and fast.next:
            slow = slow.next
            fast = fast.next.next

        # Reverse the second half of the list
        prev, curr = None, slow

        while curr:

            next_node = curr.next
            curr.next = prev

            prev = curr
            curr = next_node

        # Compare first and second half
        fh, sh = head, prev

        while sh:
            if fh.val != sh.val:
                return False
            fh = fh.next
            sh = sh.next
        return True


if __name__ == "__main__":
    l1 = linked_list_builder([1, 2])
    l2 = linked_list_builder([1, 2, 2, 1])
    l3 = linked_list_builder([3, 1, 3, 3, 1, 3])
    so = Solution()
    print(so.isPalindrome(l1))
    print(so.isPalindrome(l2))
    print(so.isPalindrome(l3))
