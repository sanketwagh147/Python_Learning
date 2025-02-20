"""
Leet code problem 142
Youtube: https://www.youtube.com/watch?v=UmudS7EXz6o

"""


class Solution:
    def detectCycle(self, head: Optional[ListNode]) -> Optional[ListNode]:

        # Slow fast ( 2pointer approach)
        # 1️⃣  initialize fast and slow to head
        slow, fast = head, head

        # 2️⃣ loop till end if there is a cycle fast and slow will meet at some point
        while fast and fast.next:

            slow = slow.next
            fast = fast.next.next

            if slow == fast:
                # 3️⃣ Break when both meet at the same point
                break
        else:
            return None

        # 4️⃣  Reset slow to head
        slow = head

        # 5️⃣ move one step
        while slow != fast:
            slow = slow.next
            fast = fast.next

        return fast or slow
