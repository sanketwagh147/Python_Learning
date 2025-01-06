from dataclasses import dataclass


@dataclass
class Node:
    value: int
    next: "Node" = None  # type: ignore  # using forward reference

    def __str__(self) -> str:
        # return f"<Node : {self.value} {'-> ' if self.next else ''} {self.next if self.next else ''}>"
        return f"<Node : {self.value} >"


class LinkedList:
    def __init__(self, value):
        new_node = Node(value)
        self.head = new_node
        self.tail = new_node
        self.length = 1

    def print_list(self):
        temp = self.head
        while temp is not None:
            print(temp)
            temp = temp.next

    def append(self, value):
        new_node = Node(value)
        if self.length == 0:
            self.head = new_node
            self.tail = new_node
        else:
            self.tail.next = new_node
            self.tail = new_node
        self.length += 1
        return True

    def pop(self):
        if self.length == 0:
            return None
        temp = self.head
        pre = self.head
        while temp.next:
            pre = temp
            temp = temp.next
        self.tail = pre
        self.tail.next = None
        self.length -= 1
        if self.length == 0:
            self.head = None
            self.tail = None
        return temp

    def prepend(self, value):
        new_node = Node(value)
        if self.length == 0:
            self.head = new_node
            self.tail = new_node
        else:
            new_node.next = self.head
            self.head = new_node
        self.length += 1
        return True

    def pop_first(self):
        if self.length == 0:
            return None
        temp = self.head
        self.head = self.head.next
        temp.next = None
        self.length -= 1
        if self.length == 0:
            self.tail = None
        return temp

    def get(self, index):
        if index < 0 or index >= self.length:
            return None
        temp = self.head
        for _ in range(index):
            temp = temp.next
        return temp

    def set_value(self, index, value):
        temp = self.get(index)
        if temp:
            temp.value = value
            return True
        return False

    def insert(self, index, value):
        if index < 0 or index > self.length:
            return False
        if index == 0:
            return self.prepend(value)
        if index == self.length:
            return self.append(value)
        new_node = Node(value)
        temp = self.get(index - 1)
        new_node.next = temp.next
        temp.next = new_node
        self.length += 1
        return True

    def remove(self, index) -> Node | None:

        # handle out of bounds i.e (less than 0 or more than equal to self.length)

        if index < 0 or index >= self.length:
            return None

        # remove first
        if index == 0:
            return self.pop_first()

        # remove last
        if index == self.length:
            return self.pop()

        prev = self.get(index - 1)

        temp = prev.next

        prev.next = temp.next

        temp.next = None

        self.length -= 1
        return temp

    def reverse(self):
        if not self.head or self.length == 1:
            return self

        # swap head and tail
        current = self.head
        self.head = self.tail
        self.tail = current

        # Initaial assign

        before = None

        for _ in range(self.length):
            # set after as the next Node  of current
            after, current.next = current.next, before

            # start reversing set current to be of previous
            # current.next = before

            # now move before to next node
            before, current = current, after

            # now move current to next node
            # current = after

    def reverse2(self):
        prev = None
        # start from head
        curr = self.head

        # stop
        while curr is not None:

            # save next item in temp
            temp = curr.next

            # set next to be prev
            curr.next = prev

            # set previos item to be the curr
            prev = curr

            # set current item to be the next item
            curr = temp

    def find_middle_node(self):
        slow_pointer = self.head
        fast_pointer = self.head

        while fast_pointer and fast_pointer.next:
            slow_pointer = slow_pointer.next
            fast_pointer = fast_pointer.next.next

        return slow_pointer

    def has_loop(self):
        """
        Detects cycle / loop present in a linked list
        using Floyd's cycle-finding algorithm(tortoise and the hare)
        If cycle is present the pointer will eventually meet each other
        """
        slow_pointer = self.head
        fast_pointer = self.head

        while fast_pointer and fast_pointer.next:
            print("*")
            slow_pointer = slow_pointer.next
            fast_pointer = fast_pointer.next.next
            if slow_pointer is fast_pointer:
                return True

        return False


def find_kth_from_end(ll: LinkedList, k: int):
    """Given K return the kth element in list starting backwards"""

    # Handle k
    if k <= 0:
        raise ValueError(f"{k=} is invalid")

    #
    slow_pointer = ll.head
    fast_pointer = ll.head

    for _ in range(k):

        if not fast_pointer:
            return None
        fast_pointer = fast_pointer.next

    while fast_pointer:
        slow_pointer = slow_pointer.next
        fast_pointer = fast_pointer.next

    return slow_pointer


if __name__ == "__main__":
    my_linked_list = LinkedList(1)
    my_linked_list.append(2)
    # my_linked_list.append(3)
    # my_linked_list.append(4)
    # my_linked_list.append(5)

    k = 3
    result = find_kth_from_end(my_linked_list, k)

    print(result.value)  # Output: 4

    # my_linked_list_1 = LinkedList(1)
    # my_linked_list_1.append(2)
    # my_linked_list_1.append(3)
    # my_linked_list_1.append(4)
    # my_linked_list_1.tail.next = my_linked_list_1.head
    # print(my_linked_list_1.has_loop())  # Returns True

    # my_linked_list_2 = LinkedList(1)
    # my_linked_list_2.append(2)
    # my_linked_list_2.append(3)
    # my_linked_list_2.append(4)
    # print(my_linked_list_2.has_loop())  # Returns False

    # my_linked_list = LinkedList(1)
    # my_linked_list.append(2)
    # my_linked_list.append(3)
    # my_linked_list.append(4)
    # my_linked_list.append(5)
    # my_linked_list.append(6)
    # my_linked_list.append(7)
    # my_linked_list.append(7)
    # my_linked_list.append(7)

    # print(my_linked_list.find_middle_node())

    # print("LL before reverse():")
    # my_linked_list.print_list()

    # my_linked_list.reverse()

    # print("\nLL after reverse():")
    # my_linked_list.print_list()
