# Pipeline Pattern — Question 1 (Easy)

## Problem: Text Processing Pipeline

Build a pipeline that transforms text through a series of processing steps.

### Requirements

- `Stage(ABC)`: `process(data: str) -> str`
- Stages: `StripWhitespace`, `Lowercase`, `RemovePunctuation`, `RemoveStopWords`
- `Pipeline`: chains stages and runs data through all stages in order.

### Expected Usage

```python
pipeline = Pipeline([
    StripWhitespace(),
    Lowercase(),
    RemovePunctuation(),
    RemoveStopWords(["the", "a", "is", "in"]),
])

result = pipeline.run("  The Quick, Brown Fox — IS in the FIELD!  ")
print(result)  # → "quick brown fox field"
```

### Constraints

- Each stage receives the output of the previous stage.
- Stages are independent and reusable.
- The pipeline can be built dynamically by adding/removing stages.
