from typing import Optional

from common.nodes import Node


class Solution:
    def deleteDuplicates(self, head: Optional[Node]) -> Optional[Node]:

        dummy = head
        curr = head

        while curr:

            if curr.next and curr.val == curr.next.val:

                # This removes the link between same next node
                curr.next = curr.next.next
            else:
                # Move to next node
                curr = curr.next

        return dummy
