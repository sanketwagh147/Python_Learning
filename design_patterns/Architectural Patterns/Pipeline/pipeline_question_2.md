# Pipeline Pattern — Question 2 (Medium)

## Problem: Data Validation and Transformation Pipeline with Error Tracking

Build a pipeline that processes records through validation and transformation stages, collecting errors per record without stopping the pipeline.

### Requirements

#### Stage Interface
```python
class PipelineStage(ABC):
    def process(self, record: dict) -> tuple[dict | None, list[str]]:
        """Returns (transformed_record_or_None, list_of_errors)."""

class ValidationStage(PipelineStage):
    """Validates a record. Returns (record, errors) — does not transform."""

class TransformStage(PipelineStage):
    """Transforms a record. Returns (new_record, errors)."""
```

#### Concrete Stages
- `RequiredFieldsValidator(fields)`: checks required fields exist
- `TypeValidator(field_types: dict)`: checks field types match expectations
- `RangeValidator(field, min, max)`: checks numeric field is in range
- `NormalizeFieldTransform(field, fn)`: applies transformation to a field
- `DefaultValueTransform(field, default)`: fills missing fields

#### Pipeline
```python
class DataPipeline:
    def __init__(self, stages: list[PipelineStage]): ...
    def run(self, records: list[dict]) -> PipelineResult: ...
```

### Expected Usage

```python
pipeline = DataPipeline([
    DefaultValueTransform("status", "active"),
    RequiredFieldsValidator(["name", "email", "age"]),
    TypeValidator({"name": str, "age": int, "email": str}),
    RangeValidator("age", 0, 150),
    NormalizeFieldTransform("email", str.lower),
])

records = [
    {"name": "Alice", "email": "ALICE@EX.COM", "age": 30},
    {"name": "Bob", "age": "twenty"},         # bad type + missing email
    {"name": "Charlie", "email": "c@x.com", "age": 200},  # age out of range
]

result = pipeline.run(records)
print(result.valid_records)
# → [{"name": "Alice", "email": "alice@ex.com", "age": 30, "status": "active"}]

print(result.errors)
# → {1: ["Missing field: email", "Field 'age' expected int, got str"],
#    2: ["Field 'age' out of range: 200 not in [0, 150]"]}
```

### Constraints

- Pipeline processes ALL records — doesn't stop on first error.
- Each record collects its own error list.
- If a validation fails, the record is excluded from further processing.
- Transform stages only apply to valid records.
- `PipelineResult`: `valid_records`, `errors: dict[int, list[str]]`, `stats` (total, valid, invalid).

### Think About

- How does this compare to validation in Django Forms or Pydantic?
- Could you combine this with the Strategy pattern for pluggable validators?
