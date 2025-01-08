class Node:
    def __init__(self, value):
        self.value = value
        self.next = None

    def __repr__(self) -> str:
        return f"[Node : {self.value}]"


class LinkedList:
    def __init__(self, value):
        new_node = Node(value)
        self.head = new_node
        self.length = 1

    def append(self, value):
        new_node = Node(value)
        if self.length == 0:
            self.head = new_node
        else:
            current = self.head
            while current.next is not None:
                current = current.next
            current.next = new_node
        self.length += 1
        return True

    def print_list(self):
        temp = self.head
        while temp is not None:
            print(temp.value)
            temp = temp.next

    def make_empty(self):
        self.head = None
        self.length = 0

    def reverse_between(self, start_index: int, end_index: int):
        """
        Reverse the nodes of the linked list from start_index to end_index (inclusive) in one pass and in-place.

        Parameters:
        start_index (int): Starting index of the segment to reverse (0-based).
        end_index (int): Ending index of the segment to reverse (0-based).
        """
        if not self.head or start_index == end_index:
            return

        dummy = Node(0)
        dummy.next = self.head
        prev_start = dummy

        # Step 1: Traverse to the node before start_index
        for _ in range(start_index):
            if not prev_start.next:  # Handle out-of-bounds indices
                return
            prev_start = prev_start.next

        # Step 2: Reverse the segment from start_index to end_index
        current = prev_start.next
        prev = None
        for _ in range(end_index - start_index + 1):
            if not current:  # Handle out-of-bounds indices
                return
            next_node = current.next
            current.next = prev
            prev = current
            current = next_node

        # Step 3: Reconnect the reversed segment
        start_node = prev_start.next
        prev_start.next = prev
        start_node.next = current

        # Update head if necessary
        if dummy.next != self.head:
            self.head = dummy.next

    def reverse_between2(self, start_index: int, end_index: int):
        """
        ex 1:
        ll = 0 1 2 |3 4 5| 6
        start_index = 3
        end_index =  5
        -> 1 2 5 4 3 6
        """
        if self.length <= 1:
            return None

        """
        
        2->5

        5->4
        4->3
        3 -> 6
        
        """
        dummy = Node(0)
        dummy.next = self.head
        prev_start = dummy
        temp = []

        for _ in range(start_index):
            if not prev_start.next:
                return

            prev_start = prev_start.next
            temp.append(prev_start)

        current = prev_start.next
        prev = None

        for _ in range(end_index, start_index + 1):
            if not current:
                return

            next_node = current.next
            current.next = prev
            prev = current
            current = next_node

        start_node = prev_start.next
        prev_start.next = prev
        start_node.next = current

        if dummy.next != self.head:
            self.head = dummy.next

        print(temp)
        print("hello")


linked_list = LinkedList(0)
linked_list.append(1)
linked_list.append(2)
linked_list.append(3)
linked_list.append(4)
linked_list.append(5)

print("Original linked list: ")
linked_list.print_list()

# Reverse a sublist within the linked list
linked_list.reverse_between(2, 4)
print("Reversed sublist (2, 4): ")
linked_list.print_list()
exit()

# Reverse another sublist within the linked list
linked_list.reverse_between(0, 4)
print("Reversed entire linked list: ")
linked_list.print_list()

# Reverse a sublist of length 1 within the linked list
linked_list.reverse_between(3, 3)
print("Reversed sublist of length 1 (3, 3): ")
linked_list.print_list()

# Reverse an empty linked list
empty_list = LinkedList(0)
empty_list.make_empty
empty_list.reverse_between(0, 0)
print("Reversed empty linked list: ")
empty_list.print_list()


"""
    EXPECTED OUTPUT:
    ----------------
    Original linked list: 
    1
    2
    3
    4
    5
    Reversed sublist (2, 4): 
    1
    2
    5
    4
    3
    Reversed entire linked list: 
    3
    4
    5
    2
    1
    Reversed sublist of length 1 (3, 3): 
    3
    4
    5
    2
    1
    Reversed empty linked list: 
    None
    
"""
