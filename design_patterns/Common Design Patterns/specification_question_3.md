# Specification Pattern — Question 3 (Hard)

## Problem: Specification Pattern as a Query Language for Repositories

Build a system where specifications are NOT just in-memory filters but translate into actual database queries (SQL WHERE clauses), allowing efficient server-side filtering.

### Requirements

#### Dual-Mode Specification
Each specification can:
1. **Filter in-memory**: `is_satisfied_by(entity) -> bool` (as usual)
2. **Generate SQL**: `to_sql() -> tuple[str, dict]` (WHERE clause + params)

```python
class Specification(ABC):
    @abstractmethod
    def is_satisfied_by(self, entity) -> bool: ...
    
    @abstractmethod
    def to_sql(self) -> tuple[str, dict]:
        """Returns (WHERE clause, params dict) for parameterized queries."""
    
    def __and__(self, other) -> "AndSpec": ...
    def __or__(self, other) -> "OrSpec": ...
    def __invert__(self) -> "NotSpec": ...
```

#### Concrete Specifications
```python
class Equals(Specification):
    def __init__(self, field: str, value):
        self.field = field
        self.value = value
    
    def is_satisfied_by(self, entity):
        return getattr(entity, self.field) == self.value
    
    def to_sql(self):
        param_name = f"p_{self.field}"
        return f"{self.field} = :{param_name}", {param_name: self.value}

class GreaterThan(Specification): ...
class LessThan(Specification): ...
class Contains(Specification): ...       # SQL LIKE '%value%'
class InList(Specification): ...         # SQL IN (...)
class Between(Specification): ...        # SQL BETWEEN
class IsNull(Specification): ...         # SQL IS NULL / IS NOT NULL
```

#### Composites Generate Proper SQL
```python
class AndSpec(Specification):
    def to_sql(self):
        left_sql, left_params = self.left.to_sql()
        right_sql, right_params = self.right.to_sql()
        return f"({left_sql}) AND ({right_sql})", {**left_params, **right_params}
```

#### Repository Using Specifications
```python
class SQLRepository(Generic[T]):
    def find(self, spec: Specification) -> list[T]:
        where_clause, params = spec.to_sql()
        query = f"SELECT * FROM {self.table} WHERE {where_clause}"
        return self.db.execute(query, params)
    
    def count(self, spec: Specification) -> int: ...
    def exists(self, spec: Specification) -> bool: ...
```

### Expected Usage

```python
# Build complex spec
spec = (
    Equals("status", "active") 
    & GreaterThan("age", 18) 
    & (Contains("name", "Smith") | Contains("name", "Jones"))
    & ~IsNull("email")
)

# Use for in-memory filtering
filtered = [u for u in users if spec.is_satisfied_by(u)]

# Use for SQL query generation
where, params = spec.to_sql()
print(where)
# → (status = :p_status) AND (age > :p_age) AND ((name LIKE :p_name_1) OR (name LIKE :p_name_2)) AND (NOT (email IS NULL))
print(params)
# → {"p_status": "active", "p_age": 18, "p_name_1": "%Smith%", "p_name_2": "%Jones%"}

# Use with repository
repo = SQLRepository(User, db_connection)
active_adults = repo.find(spec)
count = repo.count(Equals("status", "active"))
```

### Constraints

- SQL generation uses **parameterized queries** (NO string interpolation of values).
- Parameter names are unique even in complex trees (handle name collisions).
- `to_sql()` and `is_satisfied_by()` must produce **consistent results** (same entities matched).
- Support at least 7 specification types + 3 composites.
- Write tests verifying SQL output AND in-memory filtering match.

### Think About

- How does SQLAlchemy's filter system work? How is it similar to this?
- How does Django's Q objects (`Q(age__gt=18) | Q(name__contains="Smith")`) implement this?
- What are the limitations of this approach? (Complex JOINs, subqueries, aggregations.)
- Could you add an `to_elasticsearch()` adapter for the same specifications?
