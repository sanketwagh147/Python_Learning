# Interpreter Pattern — Question 3 (Hard)

## Problem: Mini SQL Query Interpreter

Build an interpreter for a simplified SQL-like query language that operates on in-memory data.

### Requirements

#### Supported Grammar
```
SELECT <columns> FROM <table> [WHERE <conditions>] [ORDER BY <column> ASC|DESC] [LIMIT <n>]
```

#### Expression Classes
```python
class SQLExpression(ABC):
    def interpret(self, database: dict[str, list[dict]]) -> list[dict]: ...

class SelectExpression(SQLExpression):
    columns: list[str]  # ["name", "age"] or ["*"]
    source: FromExpression
    where: WhereExpression | None
    order_by: OrderByExpression | None
    limit: LimitExpression | None

class FromExpression(SQLExpression):
    table_name: str

class WhereExpression(SQLExpression):
    condition: Condition  # reuse the Rule pattern from Q2

class OrderByExpression(SQLExpression):
    column: str
    direction: str  # "ASC" or "DESC"

class LimitExpression(SQLExpression):
    count: int
```

#### Parser
```python
class SQLParser:
    @staticmethod
    def parse(query: str) -> SelectExpression: ...
```

### Expected Usage

```python
database = {
    "users": [
        {"id": 1, "name": "Alice", "age": 30, "city": "NYC"},
        {"id": 2, "name": "Bob", "age": 25, "city": "LA"},
        {"id": 3, "name": "Carol", "age": 35, "city": "NYC"},
        {"id": 4, "name": "Dave", "age": 22, "city": "Chicago"},
    ]
}

query = SQLParser.parse("SELECT name, age FROM users WHERE city == 'NYC' ORDER BY age DESC LIMIT 5")
result = query.interpret(database)
print(result)
# [{"name": "Carol", "age": 35}, {"name": "Alice", "age": 30}]

query2 = SQLParser.parse("SELECT * FROM users WHERE age > 24")
result2 = query2.interpret(database)
print(result2)
# [{"id": 1, "name": "Alice", ...}, {"id": 2, "name": "Bob", ...}, {"id": 3, "name": "Carol", ...}]
```

### Constraints

- Parser must handle the full grammar (SELECT, FROM, WHERE, ORDER BY, LIMIT).
- WHERE supports: `==`, `!=`, `>`, `<`, `>=`, `<=`, AND, OR.
- Invalid queries raise `QuerySyntaxError` with a helpful message.
- Table not found raises `TableNotFoundError`.
- Column not found raises `ColumnNotFoundError`.

### Think About

- This is where Interpreter pattern meets its limits. At what complexity would you switch to a parser generator?
- How does SQLAlchemy's expression system relate to this pattern?
- Could you add `INSERT INTO` and `DELETE FROM` support? What changes?
