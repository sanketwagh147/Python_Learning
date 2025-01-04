class Node:
    def __init__(self, value: int, next=None) -> None:
        self.value = value
        self.next: Node | None = next


class Stack:
    def __init__(self, val) -> None:
        node = Node(val)
        self.top: Node = node
        self.height = 1

    def print_stack(self):
        temp = self.top
        while temp is not None:
            print(temp.value)
            temp = temp.next

    def push(self, val):
        new_node: Node = Node(val)
        new_node.next = self.top
        self.top = new_node

        self.height += 1
        return new_node

    def pop(self):
        if self.height == 0:
            return None
        temp = self.top
        self.top = self.top.next
        temp.next = None
        self.height -= 1
        return temp


if __name__ == "__main__":
    st = Stack(1)
    st.push(2)
    st.push(3)
    st.print_stack()
