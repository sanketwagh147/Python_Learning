"""Doubly Linked Lists"""

from dsa_book.common.nodes import DNode


class DoublyLinkedList:

    def __init__(self, value) -> None:
        new_node = DNode(value)

        # initially head and tail would be same
        self.head = new_node
        self.tail = new_node
        self.length = 1

    def print_list(self):
        temp = self.head
        while temp is not None:
            print(temp.value)
            temp = temp.next

    def append(self, value):
        new_node = DNode(value)

        # if head or tail are None this means list is empty
        if self.head is None or self.tail is None:
            self.head = new_node
            self.tail = new_node
        else:
            self.tail.next = new_node
            new_node.prev = self.tail
            self.tail = new_node
            self.length += 1

        return True

    def pop(self):

        # Check if empty
        if self.length == 0:
            return None

        temp = self.tail
        # Handles popping when item length is 1 and will be 0 after poppin
        if self.length == 1:
            self.head = None
            self.tail = None
        else:

            # set the temp var to be the last var
            # set the tail to current tails previous element
            self.tail = self.tail.prev  # type: ignore

            # As we remove the last item so post removal self.tail.next is None
            self.tail.next = None  # type: ignore

            # remove the link between last  node
            temp.prev = None  # type: ignore

        self.length -= 1

        return temp

    def prepend(self, val):
        new_node = DNode(val)

        if self.length == 0:
            self.head = new_node
            self.tail = new_node
        else:
            new_node.next = self.head
            self.head.prev = new_node  # type: ignore
            self.head = new_node

        self.length += 1
        return True

    def pop_first(self):
        """remove first item and return it"""
        # if list is empty
        if self.length == 0:
            return None
        # select item to pop is the head
        temp = self.head

        # if list is of len 1 post pop it would be 0 thus making head & tail point to None
        if self.length == 1:
            self.head = None
            self.tail = None
        else:
            self.head = self.head.next  # type: ignore
            self.head.prev = None  # type: ignore
            temp.next = None  # type: ignore
        self.length -= 1
        return temp

    def get(self, index):
        if index >= self.length or index < 0:
            return None

        if index < self.length / 2:
            temp = self.head
            for _ in range(index):
                temp = temp.next  # type: ignore
        else:
            temp = self.tail
            for _ in (range(self.length, index, -1),):
                temp = temp.prev  # type: ignore
        return temp

    def set_value(self, index, value):
        """sets a value"""

        item = self.get(index)
        if item:
            item.value = value
            return True

        return False

    def insert(self, index, value):
        # inserts at a particular index

        if index < 0 or index > self.length:
            return False

        if index == 0:
            return self.prepend(value)
        if index == self.length:
            return self.append(value)
        new_node = DNode(value)
        before = self.get(index - 1)
        after = before.next  # type: ignore
        new_node.prev = before  # type: ignore
        new_node.next = after
        before.next = after.prev = new_node  # type: ignore
        self.length += 1
        return True

    def remove(self, index):

        if index < 0 or index > self.length:
            return None

        if index == 0:
            return self.pop_first()

        if index == self.length - 1:
            return self.pop()

        temp = self.get(index)

        # set previous of temp to point to
        temp.next.prev = temp.prev  # type: ignore
        temp.prev.next = temp.next  # type: ignore
        temp.next = None  # type: ignore
        temp.prev = None  # type: ignore

        self.length -= 1
        return temp

    def inspect_list(self):
        for each in self.__dict__:
            print(f"{each} : {self.__dict__[each]}")


if __name__ == "__main__":
    dl = DoublyLinkedList(2)
    # dl.print_list()
    dl.append(3)
    # dl.append(4)
    # dl.append(2)
    # print(dl.pop())
    # print(dl.pop())
    # print(dl.pop())
    # dl.inspect_list()
    dl.prepend(1)
    dl.prepend(0)
    # print(dl.pop_first())
    # print(dl.pop_first())
    # print(dl.pop_first())
    # print(dl.get(0))
    dl.set_value(0, 100)
    dl.set_value(2, 200)
    dl.insert(1, 50)
    dl.insert(4, 40)
    dl.remove(4)
    dl.remove(1)
    dl.remove(2)
    # print(dl.get(2))

    dl.print_list()