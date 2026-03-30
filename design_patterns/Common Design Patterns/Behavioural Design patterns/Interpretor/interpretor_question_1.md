# Interpreter Pattern — Question 1 (Easy)

## Problem: Simple Math Expression Interpreter

Build an interpreter that evaluates expressions like `"3 + 5"`, `"10 - 2 * 3"`.

### Requirements

- `Expression(ABC)`: `interpret() -> float`
- `NumberExpression`: literal number
- `AddExpression(left, right)`: left + right
- `SubtractExpression(left, right)`: left - right
- `MultiplyExpression(left, right)`: left * right
- Build the AST manually (no parser needed for this question).

### Expected Usage

```python
# Represents: (3 + 5) * 2
expr = MultiplyExpression(
    AddExpression(NumberExpression(3), NumberExpression(5)),
    NumberExpression(2)
)
print(expr.interpret())  # → 16.0

# Represents: 10 - 2 * 3
expr2 = SubtractExpression(
    NumberExpression(10),
    MultiplyExpression(NumberExpression(2), NumberExpression(3))
)
print(expr2.interpret())  # → 4.0
```

### Constraints

- Each expression class has a single `interpret()` method.
- The tree structure represents operator precedence.
