"""
Classic Visitor pattern ( violates OCP)
"""

from abc import ABC
from typing import Any


def _qualname(obj):
    """Get the fully-qualified name of an object (including module)."""
    qual_name = obj.__module__ + "." + obj.__qualname__
    print(qual_name)
    return qual_name


def _declaring_class(obj):
    """Get the name of the class that declared an object."""
    name = _qualname(obj)
    return name[: name.rfind(".")]


# Stores the actual visitor methods
_methods = {}


# Delegating visitor implementation
def _visitor_impl(self, arg):
    """Actual visitor method implementation."""
    method = _methods[(_qualname(type(self)), type(arg))]
    return method(self, arg)


# The actual @visitor decorator
def visitor(arg_type):
    """Decorator that creates a visitor method."""

    def decorator(fn):
        declaring_class = _declaring_class(fn)
        _methods[(declaring_class, arg_type)] = fn

        # Replace all decorated methods with _visitor_impl
        return _visitor_impl

    return decorator


class Expression(ABC):

    # @abstractmethod
    def print(self, buffer):
        pass

    def accept(self, visitor):
        visitor.visit(self)


class DoubleExpression(Expression):
    def __init__(self, value) -> None:
        self.value = value


class AdditionExpression(Expression):
    def __init__(self, left, right) -> None:
        self.left = left
        self.right = right


class ExpressionPrinter:

    def __init__(self) -> None:
        self.buffer = []

    def __str__(self) -> str:
        return "".join(self.buffer)

    @visitor(DoubleExpression)
    def visit(self, de):
        self.buffer.append(str(de.value))

    @visitor(AdditionExpression)
    def visit(self, ae):
        self.buffer.append("(")
        ae.left.accept(self)
        self.buffer.append("+")
        ae.right.accept(self)
        self.buffer.append(")")


if __name__ == "__main__":
    e = AdditionExpression(
        DoubleExpression(1),
        AdditionExpression(DoubleExpression(2), DoubleExpression(3)),
    )
    printer = ExpressionPrinter()
    printer.visit(e)
    print(printer)
