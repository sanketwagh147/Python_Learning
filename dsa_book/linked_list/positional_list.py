"""
Positional List
"""

from functools import total_ordering
from typing import Any

from dsa_book.common.exceptions import InvalidNodeException
from dsa_book.common.nodes import DNode
from dsa_book.linked_list.doubly_linked_list_base import _DoublyLinkedListBase


class _Position:
    _container: Any
    _node: DNode

    def __init__(self, container, node: DNode) -> None:
        self._container = container
        self._node = node

    def value(self):
        """Returns the value of stored node"""
        return self._node.value

    def __eq__(self, other) -> bool:
        """Return True if other position is same"""
        return type(other) is type(self) and other._node is self._node

    def __ne___(self, other):
        """Return True if other object does not have same location"""
        return not (self == other)


# @total_ordering
class PositionalList(_DoublyLinkedListBase):

    def _validate(self, p):
        """Returns positions node and check if the position is valid"""
        if not isinstance(p, _Position):
            raise TypeError(f"p({p.__class__.__name__}) is not a valid Position type")

        if p._container is not self:
            raise ValueError(
                f"p({p.__class__.__name__}) does not belong to this container"
            )

        if p._node.next is None:
            raise InvalidNodeException(
                f"p({p.__class__.__name__}) does not belong to this container"
            )
        return p._node

    def _make_position(self, node) -> _Position | None:
        """Returns Positional instance of a given node or None"""

        if node is self._header or node is self._trailer:
            return None
        return _Position(self, node)

    def first(self):
        """Returns first pos and none if list is empty"""

        return self._make_position(self._header.next)

    def last(self):
        """Returns last pos and none if list is empty"""

        return self._make_position(self._trailer.prev)

    def before(self, p: DNode):
        """Returns the position before p"""
        node = self._validate(p)
        return self._make_position(node.prev)

    def after(self, p: DNode):
        """Returns the position after p"""
        node = self._validate(p)
        return self._make_position(node.next)

    def __iter__(self):
        """Iteration of elements of the list"""
        cursor = self.first()
        while cursor is not None:
            yield cursor.value()
            cursor = self.after(cursor)  # type: ignore

    # Mutators (method overriding of inherited methods)
    def _insert_between(self, value, before, after):
        node = super()._insert_between(value, before, after)
        return _Position(self, node)  # type: ignore

    def add_first(self, val):
        """Insert element first in the list"""
        return self._insert_between(val, self._header, self._header.next)

    def add_last(self, val):
        """Insert element first in the list"""
        return self._insert_between(val, self._trailer.prev, self._trailer)

    def add_before(self, p, val):
        """Adds node before, with value v at position p"""
        node = self._validate(p)
        return self._insert_between(val, node.prev, node)

    def add_after(self, p, val):
        """Adds node after, with value v at position p"""
        node = self._validate(p)
        return self._insert_between(val, node.prev, node)

    def delete(self, p):
        """Deletes the node at position p"""

        node = self._validate(p)
        return self._delete_node(node)

    def replace(self, p, val):
        """Replace node with position p with val and return old values"""

        original = self._validate(p)
        old_val = original.value
        original.value = val
        return old_val


if __name__ == "__main__":
    # TODO: Writing test cases
    ...
    p1 = PositionalList()
    p1.add_first(1)
    p1.add_last(2)

    p2 = PositionalList()
    p2.add_first(3)
    p2.add_last(4)

    # FIXME : Check why the extend method does not work
    # Observation: Issue lies in positional list of base class
    p1.extend(p2)
    # print(p1)
    for each in p1:
        print(each)
