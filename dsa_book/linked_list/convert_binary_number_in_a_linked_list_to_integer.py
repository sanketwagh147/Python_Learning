from typing import Optional

from decorators.disable_print_decorator import disable_print
from dsa_book.common.builders import linked_list_builder
from dsa_book.common.nodes import ListNode


class Solution:

    @disable_print
    def getDecimalValue(self, head: Optional[ListNode[int]]) -> int:

        # 101
        # Reverse the list

        prev = None
        curr = head

        while curr:

            next_node = curr.next
            curr.next = prev

            prev = curr

            curr = next_node

        decimal: int = 0
        count = 0

        while prev:
            # print(f"{count=} = {decimal=} {prev.val=}")
            print(f"{prev.val=}**{count=}")

            temp = 2**count
            if prev.val == 1:
                decimal += temp
            count += 1
            prev = prev.next

        return decimal


if __name__ == "__main__":
    l1 = linked_list_builder([1, 0, 1])

    res = Solution().getDecimalValue(l1)
    print(res)
