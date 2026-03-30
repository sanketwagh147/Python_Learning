# Interpreter Pattern — Question 2 (Medium)

## Problem: Boolean Rule Engine

Build an interpreter for boolean rules like `"user.age >= 18 AND user.country == 'US' OR user.is_vip == true"`.

### Requirements

- `Rule(ABC)`: `evaluate(context: dict) -> bool`
- Terminal expressions:
  - `ComparisonRule(field, operator, value)`: e.g., `age >= 18`, `country == "US"`
  - Operators: `==`, `!=`, `>`, `<`, `>=`, `<=`
- Non-terminal expressions:
  - `AndRule(left, right)`: both must be true
  - `OrRule(left, right)`: either must be true
  - `NotRule(rule)`: negation
- A simple `RuleParser` that converts a string rule to an AST.

### Expected Usage

```python
# Manual AST
rule = AndRule(
    ComparisonRule("age", ">=", 18),
    OrRule(
        ComparisonRule("country", "==", "US"),
        ComparisonRule("is_vip", "==", True)
    )
)

context = {"age": 25, "country": "IN", "is_vip": True}
print(rule.evaluate(context))  # → True (age >= 18 AND is_vip)

context2 = {"age": 16, "country": "US", "is_vip": False}
print(rule.evaluate(context2))  # → False (age < 18)

# With parser
rule = RuleParser.parse("age >= 18 AND country == 'US'")
print(rule.evaluate({"age": 25, "country": "US"}))  # → True
```

### Constraints

- `ComparisonRule` must handle string, int, float, and bool comparisons.
- The parser only needs to handle simple `AND`/`OR` combinations (no nested parentheses).
- Context values are looked up by key — raise `KeyError` if field missing.

### Think About

- How does this compare to Django ORM's Q objects?
- When would you switch from Interpreter to a full parser library (e.g., `lark`)?
