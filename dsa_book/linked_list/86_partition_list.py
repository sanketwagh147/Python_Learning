"""
Leet code 86

Partition list by value x 

ex 1:
ll = [1 4 3 2 5 2]
x = 3
op => [1,2,2,3,5]

"""

from typing import Optional

from decorators.disable_print_decorator import disable_print
from dsa_book.common.nodes import ListNode


class Solution:
    def partition(self, head: Optional[ListNode], x: int) -> Optional[ListNode]:

        sm_dummy = ListNode(0)
        lg_dummy = ListNode(0)
        small = sm_dummy
        large = lg_dummy

        while head:
            # print(f"{curr=}")

            # Compare the values with x
            if head.val < x:
                small.next = head
                small = small.next
            else:
                print(f"{head=}({head.val=}) has value greater than 3")
                large.next = head
                large = large.next
            head = head.next

        # Clear the end
        large.next = None

        # connecting small and large
        small.next = lg_dummy.next

        return sm_dummy.next


if __name__ == "__main__":
    from dsa_book.common.builders import linked_list_builder

    l1 = linked_list_builder([1, 4, 3, 2, 5, 2])
    s = Solution()
    s.partition(l1, 3).print_list()
