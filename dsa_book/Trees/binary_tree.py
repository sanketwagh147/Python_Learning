"""
An Abstract binary tree
"""

from abc import abstractmethod

from dsa_book.Trees.trees import Tree


class BinaryTree(Tree):
    """An Abstract base class representing a binary tree structure"""

    @abstractmethod
    def left(self, p):
        """
        Return a position representing p's left child
        Return None if p does not have a left child
        """
        ...

    @abstractmethod
    def right(self, p):
        """
        Return a position representing p's right child
        Return None if p does not have a right child
        """
        ...

    def sibling(self, p):
        """Return a position representing p's sibling or None if no sibling"""
        parent = self.parent(p)

        if parent is None:  # p must be the root
            return None
        else:
            if p == self.left(parent):
                return self.right(parent)
            if p == self.right(parent):
                return self.left(parent)

    def children(self, p):
        """
        Generate an iteration of Positions representing p's children
        """
        if self.left(p) is not None:
            yield self.left(p)
        if self.right(p) is not None:
            yield self.right(p)
