# Composite Pattern — Question 2 (Medium)

## Problem: Organization Hierarchy with Budget Rollup

Model a company's org chart where departments contain employees and sub-departments. Each node can report its total salary cost.

### Requirements

- `OrgUnit(ABC)`:
  - `name: str`
  - `total_cost() -> float` (abstract)
  - `headcount() -> int` (abstract)
  - `display(indent)` (abstract)

- `Employee(OrgUnit)`: leaf — has `salary`, `role`.
  - `total_cost()` → own salary
  - `headcount()` → 1

- `Department(OrgUnit)`: composite — has children (Employees and sub-Departments).
  - `total_cost()` → sum of all children recursively
  - `headcount()` → sum of all children recursively
  - `add(unit)`, `remove(unit)`
  - `average_salary() -> float`

### Expected Usage

```python
eng = Department("Engineering")
eng.add(Employee("Alice", "Senior Dev", 120000))
eng.add(Employee("Bob", "Junior Dev", 75000))

backend = Department("Backend Team")
backend.add(Employee("Charlie", "Backend Lead", 130000))
backend.add(Employee("Dave", "Backend Dev", 90000))
eng.add(backend)

company = Department("Acme Corp")
company.add(eng)
company.add(Employee("Eve", "CEO", 200000))

print(company.total_cost())    # → 615000
print(company.headcount())     # → 5
print(eng.average_salary())    # → 103750.0 (4 people in eng)
company.display(0)
```

### Constraints

- `average_salary()` should work at any level (department or whole company).
- Handle edge case: empty department → `average_salary()` returns 0.0 (no division by zero).

### Think About

- How would you add a `find_highest_paid()` method that works recursively?
- What if you need to serialize this tree to JSON?
