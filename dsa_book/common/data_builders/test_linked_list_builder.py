from dsa_book.common.builders import linked_list_builder
from dsa_book.common.nodes import Node


def test_linked_list_builder_empty():
    result = linked_list_builder([])
    assert result is None


def test_linked_list_builder_single_element():
    result = linked_list_builder([1])
    assert result.value == 1
    assert result.next is None


def test_linked_list_builder_multiple_elements():
    result = linked_list_builder([1, 2, 3])
    assert result.value == 1
    assert result.next.value == 2
    assert result.next.next.value == 3
    assert result.next.next.next is None


def test_linked_list_builder_none():
    result = linked_list_builder(None)
    assert result is None
