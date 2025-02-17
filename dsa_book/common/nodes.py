from dataclasses import dataclass
from typing import Generic, TypeVar, Union

# This
GenericNode = TypeVar("GenericNode", int, str, dict, list)


@dataclass()
class Node(Generic[GenericNode]):
    value: GenericNode
    next: Union["Node[GenericNode]", None] = None

    def __str__(self) -> str:
        return f"<Node : {self.value} {'-> ' if self.next else ''} {self.next if self.next else ''}>"


@dataclass()
class ListNode(Generic[GenericNode]):
    """Same as Node but used for leet code examples"""

    val: GenericNode
    next: Union["ListNode[GenericNode]", None] = None

    def __repr__(self) -> str:
        return f"<Node : {self.val} {'-> ' if self.next else ''} {self.next if self.next else ''}>"

    def __str__(self) -> str:
        return f"<Node : {self.val}>"

    def print_list(self):
        current = self
        while current:
            print(current.val, end=" -> " if current.next else "\n")
            current = current.next  # Move to the next node


@dataclass(slots=True)
class DNode(Node[GenericNode]):
    prev: Union["DNode[GenericNode]", None] = None

    def __str__(self) -> str:
        return f"<Node : {self.value} >"


if __name__ == "__main__":
    ...
    int_node: Node[int] = Node(1)
