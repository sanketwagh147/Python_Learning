"""
Concrete implementation of linked binary tree
"""

from dsa_book.Trees.binary_tree import BinaryTree


class LinkedBinaryTree(BinaryTree):
    """Linked representation of a binary tree structure"""

    class _Node:

        # Slots replaces __dict__ and avoids aditional attributes:
        __slots__ = "_element", "_parent", "_left", "_right"

        def __init__(self, element, parent=None, left=None, right=None) -> None:
            self._element = element
            self._parent = parent
            self._left = left
            self._right = right

    class Position(BinaryTree.Position):
        """Represents locatio nof single element"""

        def __init__(self, container, node) -> None:
            self._container = container
            self._node = node

        def element(self):
            """Return Element stored at this position"""
            return self._node._element

        def __eq__(self, other):
            """Return True if other is a position representing the same location"""
            return type(other) is type(self) and other._node is self._node

        def _validate(self, p):
            """Return associated node if is a valid position"""
