from dataclasses import dataclass


@dataclass
class Node:
    value: int
    next: "Node" = None  # type: ignore  # using forward reference

    def __str__(self) -> str:
        return f"<Node : {self.value} {'-> ' if self.next else ''} {self.next if self.next else ''}>"


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


my_linked_list = LinkedList(1)
my_linked_list.append(2)
my_linked_list.append(3)
my_linked_list.append(4)
my_linked_list.append(8)

print("LL before reverse():")
my_linked_list.print_list()

my_linked_list.reverse()

print("\nLL after reverse():")
my_linked_list.print_list()


"""
    EXPECTED OUTPUT:
    ----------------
    LL before reverse():
    1
    2
    3
    4

    LL after reverse():
    4
    3
    2
    1
    
"""
