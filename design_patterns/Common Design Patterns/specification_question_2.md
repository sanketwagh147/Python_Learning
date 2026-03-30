# Specification Pattern — Question 2 (Medium)

## Problem: Business Rule Validator with Specification Trees

Build a rule engine where business rules are expressed as specification trees and can be serialized to/from dictionaries for storage or display.

### Requirements

#### Specifications with Metadata
```python
class Specification(ABC):
    name: str  # human-readable name
    
    @abstractmethod
    def is_satisfied_by(self, candidate) -> bool: ...
    
    def explain(self, candidate) -> str:
        """Return human-readable explanation of pass/fail."""
    
    def to_dict(self) -> dict:
        """Serialize to dictionary for storage/debugging."""
```

#### Composite Specifications
```python
class AndSpec(Specification): ...
class OrSpec(Specification): ...
class NotSpec(Specification): ...
```

#### Loan Approval Rules
- `MinCreditScore(score)`: credit_score >= score
- `MaxDebtToIncome(ratio)`: debt_to_income <= ratio
- `MinIncome(amount)`: annual_income >= amount
- `EmploymentStatus(statuses)`: employment in allowed statuses
- `MinAge(age)`: age >= age
- `NoRecentBankruptcy(years)`: no bankruptcy in last N years

### Expected Usage

```python
# Loan approval rule
loan_rule = (
    MinCreditScore(650) 
    & MaxDebtToIncome(0.4) 
    & MinIncome(30000) 
    & EmploymentStatus(["employed", "self-employed"])
    & MinAge(18)
    & NoRecentBankruptcy(7)
)

applicant = LoanApplicant(
    credit_score=720, debt_to_income=0.35, income=55000,
    employment="employed", age=30, last_bankruptcy=None,
)

print(loan_rule.is_satisfied_by(applicant))  # → True

# Detailed explanation
print(loan_rule.explain(applicant))
# → ✓ Credit score 720 >= 650
# → ✓ Debt-to-income 0.35 <= 0.40
# → ✓ Income $55,000 >= $30,000
# → ✓ Employment: employed ∈ [employed, self-employed]
# → ✓ Age 30 >= 18
# → ✓ No bankruptcy in last 7 years
# → RESULT: APPROVED

# Failed applicant
bad_applicant = LoanApplicant(credit_score=580, debt_to_income=0.6, ...)
print(loan_rule.explain(bad_applicant))
# → ✗ Credit score 580 < 650
# → ✗ Debt-to-income 0.60 > 0.40
# → ...
# → RESULT: DENIED (2 rules failed)

# Serialize for storage
print(loan_rule.to_dict())
# → {"and": [{"min_credit_score": 650}, {"max_dti": 0.4}, ...]}
```

### Constraints

- `explain()` traverses the entire specification tree and reports each leaf.
- `to_dict()` produces a serializable representation for DB storage or API response.
- Composites (`AndSpec`, `OrSpec`) recursively call `explain()`/`to_dict()` on children.

### Think About

- How is this used in real financial systems for underwriting rules?
- Could you load rules from a JSON config instead of code?
