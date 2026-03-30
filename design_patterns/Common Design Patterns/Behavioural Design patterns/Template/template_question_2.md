# Template Method Pattern — Question 2 (Medium)

## Problem: Data Import Pipeline with Hooks

A data import system follows fixed steps but allows optional hooks for customization.

### Requirements

#### Template
```python
class DataImporter(ABC):
    def run(self, source: str) -> ImportResult:
        """Template method — fixed sequence."""
        self.validate_source(source)       # abstract
        raw = self.extract(source)          # abstract
        self.before_transform(raw)          # hook (optional override)
        transformed = self.transform(raw)   # abstract
        self.after_transform(transformed)   # hook (optional override)
        self.validate_data(transformed)     # abstract
        count = self.load(transformed)      # abstract
        self.on_complete(count)             # hook (optional override)
        return ImportResult(count)
```

Hooks have default (no-op) implementations. Subclasses MAY override them.

#### Concrete Importers
- `CSVImporter`: reads CSV, strips whitespace, loads to in-memory store
- `JSONImporter`: reads JSON, flattens nested structures, loads to store
- `XMLImporter`: reads XML, converts to dicts, loads to store

#### Hook Examples
- `CSVImporter.before_transform()`: logs "Processing CSV with N rows"
- `JSONImporter.after_transform()`: validates JSON schema
- `XMLImporter.on_complete()`: sends notification

### Expected Usage

```python
importer = CSVImporter(delimiter=",")
result = importer.run("data/users.csv")
# → Validating source: data/users.csv ✓
# → Extracting 500 rows from CSV...
# → [Hook] Processing CSV with 500 rows
# → Transforming: stripping whitespace, normalizing dates...
# → Validating: checking required fields...
# → Loading 500 records...
# → Import complete: 500 records imported
```

### Constraints

- Template method `run()` is `final` — subclasses cannot override it (use a docstring or naming convention to indicate this).
- Hooks default to no-op — subclasses only override the ones they need.
- If `validate_source()` fails, raise `ImportError` before any other step runs.

### Think About

- What's the difference between an abstract method and a hook?
- How does Template Method compare to Strategy? (TM uses inheritance; Strategy uses composition.)
- Could you convert this to use the Strategy pattern instead? What trade-offs?
