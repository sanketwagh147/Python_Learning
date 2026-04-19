from abc import ABC, abstractmethod


IntOrFloat = int | float


def _require_expressions(
    class_name: str, expressions: tuple["Expression", ...], minimum: int
) -> None:
    if len(expressions) < minimum:
        raise ValueError(f"{class_name} requires at least {minimum} expressions")


class Expression(ABC):
    @abstractmethod
    def interpret(self) -> IntOrFloat:
        pass


class NumberExpression(Expression):
    def __init__(self, value: IntOrFloat) -> None:
        self.value = value

    def interpret(self) -> IntOrFloat:
        return self.value


class AddExpression(Expression):
    def __init__(self, *expressions: Expression) -> None:
        _require_expressions(self.__class__.__name__, expressions, 2)
        self.expressions = expressions

    def interpret(self) -> IntOrFloat:
        total = 0
        for expression in self.expressions:
            total += expression.interpret()
        return total


class SubtractExpression(Expression):
    def __init__(self, *expressions: Expression) -> None:
        _require_expressions(self.__class__.__name__, expressions, 2)
        self.expressions = expressions

    def interpret(self) -> IntOrFloat:
        result = self.expressions[0].interpret()
        for expression in self.expressions[1:]:
            result -= expression.interpret()
        return result


class MultiplyExpression(Expression):
    def __init__(self, *expressions: Expression) -> None:
        _require_expressions(self.__class__.__name__, expressions, 2)
        self.expressions = expressions

    def interpret(self) -> IntOrFloat:
        product = 1
        for expression in self.expressions:
            product *= expression.interpret()
        return product


if __name__ == "__main__":
    expr = MultiplyExpression(
        AddExpression(NumberExpression(3), NumberExpression(5), NumberExpression(4)),
        NumberExpression(2),
        NumberExpression(0.5),
    )
    print(expr.interpret())

    expr2 = SubtractExpression(
        NumberExpression(20),
        NumberExpression(3),
        MultiplyExpression(NumberExpression(2), NumberExpression(4)),
    )
    print(expr2.interpret())
