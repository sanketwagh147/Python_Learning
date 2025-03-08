"""
Abstract base class which represents a tree data structure
"""

from abc import ABC, abstractmethod


class Tree(ABC):
    class Position(ABC):
        """An abstract representing the location of a single element"""

        @abstractmethod
        def element(self):
            """Returns the element Stored at this position"""
            raise NotImplementedError("Must be implemented by sub class")

        @abstractmethod
        def __eq__(self, other):
            """Compares other with self returns true if Position represents same location"""
            raise NotImplementedError("Must be implemented by sub class")

        def __ne__(self, other):
            """Compares other with self returns true if Position does not represents same location"""
            return not (self == other)  # Defined in terms of __eq__()

    def root(self):
        """
        Returns position representing the tree's root
        Returns None if empyt
        """
        raise NotImplementedError("Must be implemented by sub class")

    def parent(self, p: Position):
        """
        Returns the position representing p's parent.
        Returns None if p is the root.
        """
        raise NotImplementedError("Must be implemented by sub class")

    def num_children(self, p: Position) -> int:
        """
        Returns the number of children that position p has
        Returns 0 if p is a parent
        """
        raise NotImplementedError("Must be implemented by sub class")

    def children(self, p: Position):
        """
        Returns an iter of positions representing p's children
        Returns an empty iterable if p has no children.
        """
        raise NotImplementedError("Must be implemented by sub class")

    def __len__(self):
        """Return the total number of elements in the tree"""
        raise NotImplementedError("Must be implemented by sub class")
