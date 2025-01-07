class Node:
    def __init__(self, value):
        self.value = value
        self.next = None

    def __repr__(self) -> str:
        if self.next:
            next_node_value = self.next.value
        else:
            next_node_value = "None"

        return f" [Node({self.value})->NextNode({next_node_value})] "


class LinkedList:
    def __init__(self, value):
        new_node = Node(value)
        self.head = new_node
        self.length = 1

    def __repr__(self):
        nodes = []
        current = self.head
        while current:
            nodes.append(repr(current))  # Use Node's __repr__
            current = current.next
        return "->".join(nodes)  # Display as 'data1->data2->data3'

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

    def print_list(self):
        if self.head is None:
            print("empty list")
        else:
            temp = self.head
            values = []
            while temp is not None:
                values.append(str(temp.value))
                temp = temp.next
            print(" -> ".join(values))

    def remove_duplicates_(self):

        curr_pointer = self.head
        if self.length < 0:
            return None

        if self.head:

            uniques = {self.head.value}
        else:
            uniques = set()

        for _ in range(self.length):
            # while curr_pointer:
            next_node = curr_pointer.next
            curr_pointer.next = None

            # If it is present then point previous node to next node
            if next_node != None and next_node.value in uniques:
                # Remove
                nxt = next_node.next
                curr_pointer.next = None
                curr_pointer = nxt
                self.length -= 1

                ...
            # If not present  in uniques add to uniques and
            else:
                if next_node != None:
                    uniques.add(next_node.value)
                curr_pointer.next = next_node

            curr_pointer = next_node

    def remove_duplicates(self):

        if not self.head:
            return

        uniques = set()
        curr_pointer = self.head
        uniques.add(curr_pointer.value)

        while curr_pointer and curr_pointer.next:
            next_node = curr_pointer.next

            if next_node.value in uniques:

                # remove duplicate by skipping
                curr_pointer.next = next_node.next
                self.length -= 1

            else:
                uniques.add(next_node.value)
                curr_pointer = next_node


def test_remove_duplicates(linked_list, expected_values):
    print("Before: ", end="")
    linked_list.print_list()
    linked_list.remove_duplicates()
    print("After:  ", end="")
    linked_list.print_list()

    # Collect values from linked list after removal
    result_values = []
    node = linked_list.head
    while node:
        result_values.append(node.value)
        node = node.next

    # Determine if the test passes
    if result_values == expected_values:
        print("Test PASS\n")
    else:
        print("Test FAIL\n")


# Test 1: List with no duplicates
ll = LinkedList(1)
ll.append(2)
ll.append(3)
# test_remove_duplicates(ll, [1, 2, 3])

# Test 2: List with some duplicates
ll = LinkedList(1)
ll.append(2)
ll.append(1)
ll.append(3)
ll.append(2)
# test_remove_duplicates(ll, [1, 2, 3])
# exit()

# Test 3: List with all duplicates
ll = LinkedList(1)
ll.append(1)
ll.append(1)
test_remove_duplicates(ll, [1])
# exit()

# Test 4: List with consecutive duplicates
ll = LinkedList(1)
ll.append(1)
ll.append(2)
ll.append(2)
ll.append(3)
test_remove_duplicates(ll, [1, 2, 3])

# Test 5: List with non-consecutive duplicates
ll = LinkedList(1)
ll.append(2)
ll.append(1)
ll.append(3)
ll.append(2)
ll.append(4)
test_remove_duplicates(ll, [1, 2, 3, 4])

# Test 6: List with duplicates at the end
ll = LinkedList(1)
ll.append(2)
ll.append(3)
ll.append(3)
test_remove_duplicates(ll, [1, 2, 3])

# Test 7: Empty list
ll = LinkedList(None)
ll.head = None  # Directly setting the head to None
ll.length = 0  # Adjusting the length to reflect an empty list
test_remove_duplicates(ll, [])
