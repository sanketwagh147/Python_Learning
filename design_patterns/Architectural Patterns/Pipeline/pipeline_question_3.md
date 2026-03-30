# Pipeline Pattern — Question 3 (Hard)

## Problem: ETL Pipeline with Branching, Merging, and Backpressure

Build an advanced ETL (Extract-Transform-Load) pipeline that supports branching (fan-out), merging (fan-in), typed stages, and backpressure control.

### Requirements

#### Stage Types
```python
class Stage(ABC, Generic[TIn, TOut]):
    def process(self, item: TIn) -> TOut: ...

class FilterStage(Stage[T, T | None]):
    """Pass or drop items based on a predicate."""

class MapStage(Stage[TIn, TOut]):
    """Transform each item."""

class FlatMapStage(Stage[TIn, Iterable[TOut]]):
    """One input → multiple outputs."""

class BranchStage(Stage[TIn, None]):
    """Fan-out: route items to multiple downstream pipelines based on conditions."""
    def __init__(self, routes: dict[str, tuple[Callable, Pipeline]]): ...

class MergeStage:
    """Fan-in: combine results from multiple pipelines into one stream."""
```

#### ETL Pipeline
```python
class ETLPipeline:
    def __init__(self, stages: list[Stage], buffer_size: int = 100): ...
    def pipe(self, stage: Stage) -> "ETLPipeline": ...           # fluent API
    def branch(self, routes: dict) -> dict[str, "ETLPipeline"]: ...
    def merge(self, *pipelines: "ETLPipeline") -> "ETLPipeline": ...
    def run(self, source: Iterator) -> list: ...
```

### Expected Usage

```python
# Sales data ETL
pipeline = (
    ETLPipeline(buffer_size=50)
    .pipe(ParseCSVStage())              # str → dict
    .pipe(ValidateStage(required=["product", "amount", "region"]))
    .pipe(NormalizeStage({"amount": float, "product": str.upper}))
)

# Branch by region
branches = pipeline.branch({
    "us": (lambda r: r["region"] == "US", 
           ETLPipeline().pipe(AddTaxStage(rate=0.08))),
    "eu": (lambda r: r["region"] == "EU",
           ETLPipeline().pipe(AddTaxStage(rate=0.20)).pipe(AddVATStage())),
    "other": (lambda r: True,  # default
              ETLPipeline().pipe(AddTaxStage(rate=0.15))),
})

# Merge branches and load
final = (
    ETLPipeline.merge(branches["us"], branches["eu"], branches["other"])
    .pipe(AggregateByProductStage())
    .pipe(FormatReportStage())
    .pipe(LoadToDBStage(connection))
)

result = final.run(csv_file_iterator)
print(result.stats)
# → {total: 10000, us: 4200, eu: 3100, other: 2700, loaded: 10000}
```

### Constraints

- Type safety: `Stage[TIn, TOut]` — output type of stage N must match input type of stage N+1.
- Backpressure: if the buffer is full, upstream stages wait (simulate with yield/iterator).
- Branch routes are evaluated in order — first matching route wins.
- Merge maintains order within each branch but interleaves between branches.
- Error handling: failed items go to a dead-letter queue with the error + original data.
- Fluent API: `.pipe().pipe().branch()` chaining.
- Statistics collected at each stage: items in, items out, items errored, processing time.

### Think About

- How does this compare to Apache Beam / Spark pipelines?
- What's the difference between pull-based (iterator/generator) and push-based pipelines?
- How would you parallelize individual stages?
