from dataclasses import dataclass
from typing import Generic, TypeVar, Union


# This
GenericNode = TypeVar("GenericNode")


@dataclass
class Node(Generic[GenericNode]):
    value: GenericNode
    next: Union["Node[GenericNode]", None] = None

    def __str__(self) -> str:
        return f"<Node : {self.value} {'-> ' if self.next else ''} {self.next if self.next else ''}>"
