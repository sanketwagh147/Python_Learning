from typing import Optional


class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


class Solution:

    def mergeTwoLists( self, list1 , list2 ) -> Optional[ListNode]:
    #create merged list
    merged_list = ListNode()

    curr = merged_list

    while list1 and list2:

        # if list1 is smaller than list2
        if list1.val < list2.val:
            curr.next = list1
            list1 = list1.next
        else:
            curr.next = list2
            list2 = list2.next
        
        # move to next node
        curr = curr.next

    # This will work as the list is sorted in the first place
    curr.next = list1 if list1 else list2

    return merged_list.next
    
    



if __name__ == "__main__":
    list1 = [1, 2, 4]
    list2 = [1, 3, 4]
    l1 = ListNode(1, ListNode(2, ListNode(4)))
    l2 = ListNode(1, ListNode(3, ListNode(4)))
