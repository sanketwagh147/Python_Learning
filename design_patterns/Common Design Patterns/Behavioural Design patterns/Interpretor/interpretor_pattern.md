# Interpreter Pattern

Interpreter is a behavioral design pattern that represents the grammar of a small language as a set of classes. Each class knows how to interpret one part of the language, and larger expressions are built by composing smaller ones into an expression tree.

In practice, the pattern is useful when you want to evaluate expressions such as math formulas, filtering rules, query fragments, or a small domain-specific language.

## Core Idea

Instead of writing one large function full of conditionals, you model the language as objects:

- Terminal expressions represent basic values like numbers, strings, or variables.
- Non-terminal expressions combine other expressions using grammar rules such as addition, multiplication, AND, or OR.
- The full expression is usually represented as an AST (Abstract Syntax Tree).
- Calling `interpret()` on the root node evaluates the entire tree.

## Key Components

**Abstract Expression** - Declares the `interpret()` method that every expression must implement.  
**Terminal Expression** - A leaf node such as a number, boolean, or variable.  
**Non-Terminal Expression** - A node that combines one or more expressions.  
**Context** - Optional external data used during interpretation, such as variable values.  
**Client / Parser** - Builds the expression tree and triggers interpretation.  

## How the Pattern Works

1. Define the grammar you want to support.  
2. Create one class per grammar rule.  
3. Build an expression tree manually or through a parser.  
4. Call `interpret()` on the root expression.  
5. Each node delegates work to its child expressions and combines the results.  

For a tiny arithmetic language, the grammar might look like this:

```text
expression := number | expression + expression | expression * expression
```

## Implementation in Python

```python
from abc import ABC, abstractmethod


class Expression(ABC):
    @abstractmethod
    def interpret(self) -> float:
        pass


class NumberExpression(Expression):
    def __init__(self, value: float):
        self.value = value

    def interpret(self) -> float:
        return self.value


class AddExpression(Expression):
    def __init__(self, left: Expression, right: Expression):
        self.left = left
        self.right = right

    def interpret(self) -> float:
        return self.left.interpret() + self.right.interpret()


class MultiplyExpression(Expression):
    def __init__(self, left: Expression, right: Expression):
        self.left = left
        self.right = right

    def interpret(self) -> float:
        return self.left.interpret() * self.right.interpret()


# Represents: (3 + 5) * 2
expr = MultiplyExpression(
    AddExpression(NumberExpression(3), NumberExpression(5)),
    NumberExpression(2)
)

print(expr.interpret())  # 16.0
```

Here:

- `NumberExpression` is a terminal expression.
- `AddExpression` and `MultiplyExpression` are non-terminal expressions.
- The final result comes from interpreting the root node.

## When to Use the Interpreter Pattern

Use Interpreter when:

- You have a small and well-defined grammar.
- You need to evaluate expressions repeatedly.
- You want the grammar rules to be represented directly in code.
- You are building a small rule engine, calculator, or query evaluator.

Common examples include:

- Arithmetic expression evaluators
- Boolean rule engines
- Search or filter conditions
- Simple SQL-like query interpreters
- Configuration or policy languages

## Advantages

1. Makes the grammar explicit in code.  
2. Each rule has a single responsibility.  
3. Easy to extend by adding new expression classes.  
4. Works naturally with tree structures and recursion.  

## Limitations

1. The number of classes grows quickly as the grammar expands.  
2. Large or complex languages become hard to maintain.  
3. Parsing can become more difficult than interpretation itself.  
4. For full programming languages or complex DSLs, parser generators are usually a better choice.  

## Real-World Perspective

The Interpreter Pattern works best for small languages. Once the grammar becomes large, deeply nested, or frequently changing, this pattern starts to feel heavy.

### Real-World Example: Expense Approval Policy

One practical use case is an internal approval engine for employee expenses.

Example rule:

- approve if the requester is an admin
- or approve if the requester is the budget owner
- or approve if the requester is a finance manager and the amount is under 10,000

This becomes a small language of reusable expressions:

- `RoleIs("admin")`
- `BudgetOwnerRule()`
- `DepartmentIs("finance")`
- `AmountLessThan(10_000)`
- `AndRule(...)`
- `OrRule(...)`

At runtime, the request details act as the context, and the root expression decides whether the expense is approved.

A runnable Python version of this example is included in `interpretor_real_world_example.py` in this folder.

That is why it is a good fit for:

- mini calculators
- validation rules
- access-control policies
- simple query systems

But for bigger grammars, tools like parser combinators, `lark`, or compiler-style parsers are often a better approach.

## Relation to the Interpreter Exercises in This Folder

- Question 1 uses a manual arithmetic AST.
- Question 2 adds boolean rules and a context-based evaluation model.
- Question 3 shows a mini SQL interpreter, which is a good example of where the pattern starts approaching its practical limits.

## Conclusion

The Interpreter Pattern is useful when you need to model and evaluate a small language in an object-oriented way. It keeps each rule isolated, makes the expression structure explicit, and works well for recursive evaluation. It is powerful for simple DSLs, but it does not scale well to large grammars.
