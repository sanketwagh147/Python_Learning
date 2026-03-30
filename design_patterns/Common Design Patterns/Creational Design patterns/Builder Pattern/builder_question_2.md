# Builder Pattern — Question 2 (Medium)

## Problem: SQL Query Builder

Create a `QueryBuilder` that constructs SQL SELECT statements step by step.

### Requirements

- Support these operations:
  - `select(*columns)` — columns to select (default: `*`)
  - `from_table(name)` — the table name
  - `where(condition)` — add a WHERE clause (multiple calls = AND)
  - `order_by(column, direction="ASC")` — ORDER BY clause
  - `limit(n)` — LIMIT clause
  - `build()` — returns the final SQL string

### Expected Usage

```python
query = (
    QueryBuilder()
    .select("name", "email", "age")
    .from_table("users")
    .where("age > 18")
    .where("active = true")
    .order_by("name")
    .limit(10)
    .build()
)
print(query)
# SELECT name, email, age FROM users WHERE age > 18 AND active = true ORDER BY name ASC LIMIT 10
```

### Test Cases

```python
# Case 1: Simple select all
QueryBuilder().from_table("products").build()
# → "SELECT * FROM products"

# Case 2: Multiple where clauses
QueryBuilder().select("id").from_table("orders").where("status = 'pending'").where("total > 100").build()
# → "SELECT id FROM orders WHERE status = 'pending' AND total > 100"

# Case 3: Missing from_table should raise ValueError
QueryBuilder().select("name").build()
# → ValueError: "from_table() is required"
```

### Constraints

- Validate that `from_table()` was called before `build()`.
- Multiple `where()` calls are combined with `AND`.
- If `select()` is never called, default to `*`.

### Think About

- How would you extend this to support `JOIN` clauses?
- Could you introduce a **Director** class that has preset query templates?
