# Pipeline Pattern

Processes data through a **sequence of stages**, where each stage transforms its input and passes the result to the next stage.

## Key Concepts

- **Stage**: A single transformation unit with a `process(data) -> data` method.
- **Pipeline**: Composes multiple stages; data flows from first stage to last.
- Each stage is **independent** — it only knows its own input/output contract.

## Pipeline vs Chain of Responsibility

| Feature | Pipeline | Chain of Responsibility |
|---|---|---|
| **Goal** | Transform data step-by-step | Find a handler that can process a request |
| **Every stage runs?** | ✅ Yes, all stages run in order | ❌ Stops at the first handler that handles it |
| **Data flow** | Output of stage N → input of stage N+1 | Same request forwarded along |
| **Typical use** | ETL, text processing, image filters | Logging, auth, validation middlewares |

## Structure

```
Input ──→ Stage 1 ──→ Stage 2 ──→ Stage 3 ──→ Output
```

## Example

```python
class Stage(ABC):
    @abstractmethod
    def process(self, data: str) -> str: ...

class StripHTMLStage(Stage):
    def process(self, data):
        return re.sub(r"<[^>]+>", "", data)

pipeline = Pipeline()
pipeline.add_stage(StripHTMLStage())
pipeline.add_stage(NormalizeWhitespaceStage())
result = pipeline.execute(raw_html)
```

## When to Use

✅ Data needs to pass through multiple ordered transformations  
✅ Each transformation is independent and reusable  
✅ You want to easily reorder, add, or remove stages  
✅ ETL processes, text/image processing, compiler passes  

## When NOT to Use

❌ Processing should stop early when one handler matches (use CoR)  
❌ Steps have complex dependencies on each other  
❌ A simple function composition suffices
