class Node:
    def __init__(self, value):
        self.value = value
        self.next = None

    def __repr__(self):
        return f"<Node:{self.value}>"


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
            current_node = self.head
            while current_node.next is not None:
                current_node = current_node.next
            current_node.next = new_node
        self.length += 1

    def print_list(self):
        temp = self.head
        while temp is not None:
            print(temp.value)
            temp = temp.next

    def make_empty(self):
        self.head = None
        self.tail = None
        self.length = 0

    def partition_list(self, x: int):
        lt_x_head = ltx_tail = None
        gt_x_head = gt_x_tail = None

        current = self.head

        while current:
            next_node = current.next
            current.next = None

            if current.value < x:
                if not lt_x_head:
                    lt_x_head = ltx_tail = current
                else:
                    ltx_tail.next = current
                    ltx_tail = current
            else:
                if not gt_x_head:
                    gt_x_head = gt_x_tail = current
                else:
                    gt_x_head.next = current
                    gt_x_tail = current

            current = next_node

        if ltx_tail:
            ltx_tail.next = gt_x_head
            return lt_x_head
        else:
            return gt_x_head


if __name__ == "__main__":
    ll = LinkedList(3)
    ll.append(8)
    ll.append(5)
    ll.append(10)
    ll.append(2)
    ll.append(1)

    ll.partition_list(5)

    # Function to convert linked list to Python list
    # def linkedlist_to_list(head):
    #     result = []
    #     current = head
    #     while current:
    #         result.append(current.value)
    #         current = current.next
    #     return result

    # # Function to test partition_list
    # def test_partition_list():
    #     test_cases_passed = 0

    #     print("-----------------------")

    #     # Test 1: Normal Case
    #     print("Test 1: Normal Case")
    #     x = 3
    #     print(f"x = {x}")
    #     ll = LinkedList(3)
    #     ll.append(1)
    #     ll.append(4)
    #     ll.append(2)
    #     ll.append(5)
    #     print("Before:", linkedlist_to_list(ll.head))
    #     ll.partition_list(x)
    #     print("After:", linkedlist_to_list(ll.head))
    #     if linkedlist_to_list(ll.head) == [1, 2, 3, 4, 5]:
    #         print("PASS")
    #         test_cases_passed += 1
    #     else:
    #         print("FAIL")

    #     print("-----------------------")

    #     # Test 2: All Equal Values
    #     print("Test 2: All Equal Values")
    #     x = 3
    #     print(f"x = {x}")
    #     ll = LinkedList(3)
    #     ll.append(3)
    #     ll.append(3)
    #     print("Before:", linkedlist_to_list(ll.head))
    #     ll.partition_list(x)
    #     print("After:", linkedlist_to_list(ll.head))
    #     if linkedlist_to_list(ll.head) == [3, 3, 3]:
    #         print("PASS")
    #         test_cases_passed += 1
    #     else:
    #         print("FAIL")

    #     print("-----------------------")

    #     # Test 3: Single Element
    #     print("Test 3: Single Element")
    #     x = 3
    #     print(f"x = {x}")
    #     ll = LinkedList(1)
    #     print("Before:", linkedlist_to_list(ll.head))
    #     ll.partition_list(x)
    #     print("After:", linkedlist_to_list(ll.head))
    #     if linkedlist_to_list(ll.head) == [1]:
    #         print("PASS")
    #         test_cases_passed += 1
    #     else:
    #         print("FAIL")

    #     print("-----------------------")

    #     # Test 4: Already Sorted
    #     print("Test 4: Already Sorted")
    #     x = 2
    #     print(f"x = {x}")
    #     ll = LinkedList(1)
    #     ll.append(2)
    #     ll.append(3)
    #     print("Before:", linkedlist_to_list(ll.head))
    #     ll.partition_list(x)
    #     print("After:", linkedlist_to_list(ll.head))
    #     if linkedlist_to_list(ll.head) == [1, 2, 3]:
    #         print("PASS")
    #         test_cases_passed += 1
    #     else:
    #         print("FAIL")

    #     print("-----------------------")

    #     # Test 5: Reverse Sorted
    #     print("Test 5: Reverse Sorted")
    #     x = 2
    #     print(f"x = {x}")
    #     ll = LinkedList(3)
    #     ll.append(2)
    #     ll.append(1)
    #     print("Before:", linkedlist_to_list(ll.head))
    #     ll.partition_list(x)
    #     print("After:", linkedlist_to_list(ll.head))
    #     if linkedlist_to_list(ll.head) == [1, 3, 2]:
    #         print("PASS")
    #         test_cases_passed += 1
    #     else:
    #         print("FAIL")

    #     print("-----------------------")

    #     # Test 6: All Smaller Values
    #     print("Test 6: All Smaller Values")
    #     x = 2
    #     print(f"x = {x}")
    #     ll = LinkedList(1)
    #     ll.append(1)
    #     ll.append(1)
    #     print("Before:", linkedlist_to_list(ll.head))
    #     ll.partition_list(x)
    #     print("After:", linkedlist_to_list(ll.head))
    #     if linkedlist_to_list(ll.head) == [1, 1, 1]:
    #         print("PASS")
    #         test_cases_passed += 1
    #     else:
    #         print("FAIL")

    #     print("-----------------------")

    #     # Test 7: Single Element, Equal to Partition
    #     print("Test 7: Single Element, Equal to Partition")
    #     x = 3
    #     print(f"x = {x}")
    #     ll = LinkedList(3)
    #     print("Before:", linkedlist_to_list(ll.head))
    #     ll.partition_list(x)
    #     print("After:", linkedlist_to_list(ll.head))
    #     if linkedlist_to_list(ll.head) == [3]:
    #         print("PASS")
    #         test_cases_passed += 1
    #     else:
    #         print("FAIL")

    #     print("-----------------------")

    #     # Summary
    #     print(f"{test_cases_passed} out of 7 tests passed.")

    # # Run the test function
    # test_partition_list()
