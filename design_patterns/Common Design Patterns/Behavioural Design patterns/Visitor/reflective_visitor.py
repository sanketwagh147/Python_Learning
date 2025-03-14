"""
Reflective Visitor pattern ( violates OCP)
"""

from abc import ABC, abstractmethod
from typing import Any


class Expression(ABC):

    # @abstractmethod
    def print(self, buffer):
        pass


class DoubleExpression(Expression):
    def __init__(self, value) -> None:
        self.value = value


class AdditionExpression(Expression):
    def __init__(self, left, right) -> None:
        self.left = left
        self.right = right


class ExpressionPrinter:

    @staticmethod
    def print(expression: Any, buffer):

        if isinstance(expression, DoubleExpression):
            buffer.append(str(expression.value))
        if isinstance(expression, AdditionExpression):
            buffer.append("(")
            ExpressionPrinter.print(expression.left, buffer)
            buffer.append("+")
            ExpressionPrinter.print(expression.right, buffer)
            buffer.append(")")


Expression.print = lambda self, b: ExpressionPrinter.print(self, b)  # type: ignore


if __name__ == "__main__":
    e = AdditionExpression(
        DoubleExpression(1),
        AdditionExpression(DoubleExpression(2), DoubleExpression(3)),
    )
    buffer = []
    e.print(buffer)
    # ExpressionPrinter.print(e, buffer)
    print("".join(buffer))
    # print("".join(buffer), " = ", e.eval())
