from typing import Optional

from icecream import ic

from dsa_book.common.data_builders.linked_list_builder import linked_list_builder
from dsa_book.common.nodes import Node as ListNode


class Solution:
    def getIntersectionNode(
        self, headA: ListNode, headB: ListNode
    ) -> Optional[ListNode]:

        # Check if both are not null
        if not headA or not headB:
            return None

        pointer_a = headA
        pointer_b = headB

        # When a pointer reaches the end of its list, move it to the head of the other list.
        while pointer_a != pointer_b:
            # This means pointer a continue from head b if it reaches the end of its list
            pointer_a = pointer_a.next if pointer_a else headB
            pointer_b = pointer_b.next if pointer_b else headA

        return pointer_a
