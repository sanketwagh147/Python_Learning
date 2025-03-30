"""
DSA Book Abstract tree
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from enum import auto
from typing import Iterable


class Tree(ABC):

    class Position(ABC):
        """Represents location of single Element"""

        ...

        @abstractmethod
        def element(self):
            """Return element stored in this position"""
            ...

        @abstractmethod
        def __eq__(self, other):
            """Return true if other position is same as self"""
            ...

    @abstractmethod
    def root(self):
        """Return trees root or None if empty"""
        ...

    @abstractmethod
    def parent(self, p):
        """Return trees parent or None if empty"""
        ...

    @abstractmethod
    def num_children(self, p):
        """Return no of children the at positon p"""
        ...

    @abstractmethod
    def children(self, p) -> Iterable:
        """Generates an iteration of Positions that represents p's children"""
        ...

    def __len__(self):
        """Returns the total number of elements in the tree"""
        ...

    def is_root(self, p):
        """Returns True if p is same as the root"""
        return self.root() == p

    def is_leaf(self, p):
        """Return True if position p does not have any children"""
        return self.num_children(p) == 0

    def is_empty(self) -> bool:
        """Return True if Tree is empty"""
        return len(self) == 0

    def depth(self, p):
        """Returns the number of levels separating positions p from the root"""

        # if p is the root then the depth of p is 0
        if self.is_root(p):
            return 0
        # otherwise dept of p is one plus the depth of the parent of p
        else:
            return 1 + self.depth(self.parent(p))

    def _height(self, p):
        """Return height of a subtree rooted at position p"""

        # if p is a leaf the height of p is 0
        if self.is_leaf(p):
            return 0
        # otherwise the height of p is one more than the max height of p children
        else:
            return 1 + max(self._height(child) for child in self.children(p))

    def height(self, p=None):
        """
        Returns the height of the subtree rooted at Position p

        If p is None return the height of the entire tree

        """
        if p is None:
            p = self.root()

            return self._height(p)


if __name__ == "__main__":
    from enum import Enum

    class StrEnum(str, Enum):
        def __new__(cls, value):
            print(value)
            obj = str.__new__(cls, value)
            obj._value_ = obj.lower()

            return obj

    class CommonStatus(StrEnum): ...

    class CommonStrings(CommonStatus):
        YES = auto()
        NO = "no"
        OK = "ok"
        CANCEL = "cancel"
        ERROR = "error"
        SUCCESS = auto()

        def __str__(self):
            return self.value  # Ensures print(CommonStrings.OK) → "ok"

        def __repr__(self):
            return f'"{self.value}"'  # Ensures dict representation is correct

        def __json__(self):
            return self.value  # Ensures JSON serialization works correctly

    # Example usage
    d = {"ad": CommonStrings.SUCCESS}
    print(d)
