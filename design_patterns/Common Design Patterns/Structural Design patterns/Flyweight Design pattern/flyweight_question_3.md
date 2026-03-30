# Flyweight Pattern — Question 3 (Hard)

## Problem: Document Rendering Engine with Mixed Intrinsic/Extrinsic State

Build a document rendering engine where paragraphs share formatting styles (flyweight) but each has unique content, position, and page assignment.

### Requirements

#### Flyweight
```python
@dataclass(frozen=True)
class ParagraphStyle:
    font_family: str
    font_size: int
    line_height: float
    color: str
    alignment: str  # left, center, right, justify
    margins: tuple[int, int, int, int]  # top, right, bottom, left
```

#### Context
```python
class Paragraph:
    content: str
    style: ParagraphStyle  # flyweight
    page: int
    y_position: float  # vertical position on page
```

#### Rendering Engine
```python
class DocumentEngine:
    def __init__(self):
        self._style_factory = StyleFactory()
    
    def add_heading(self, text: str, level: int) -> None: ...
    def add_body(self, text: str) -> None: ...
    def add_quote(self, text: str) -> None: ...
    def add_code(self, text: str) -> None: ...
    def render(self) -> str: ...
    def stats(self) -> dict: ...  # paragraph_count, unique_styles, memory_saved
```

### Expected Usage

```python
doc = DocumentEngine()
doc.add_heading("Chapter 1: Introduction", level=1)
doc.add_body("Lorem ipsum dolor sit amet...")
doc.add_body("Consectetur adipiscing elit...")  # same style as prev body
doc.add_quote("To be or not to be — Shakespeare")
doc.add_body("More body text here...")
doc.add_code("print('hello world')")
doc.add_heading("Chapter 2: Deep Dive", level=1)
doc.add_body("Another paragraph...")

doc.render()
stats = doc.stats()
print(stats)
# {'paragraphs': 8, 'unique_styles': 4, 'memory_saved_bytes': ...}
# 4 styles: heading-1, body, quote, code (despite 8 paragraphs)
```

### Key Challenge

Implement a `StyleFactory` that:
1. Uses `@functools.lru_cache` internally (since `ParagraphStyle` is frozen/hashable).
2. Tracks cache hits vs misses for the `stats()` report.
3. Supports custom style overrides: `add_body("text", color="red")` creates a new style variant ONLY if it doesn't already exist.

### Constraints

- Calculate real memory savings using `sys.getsizeof`.
- `ParagraphStyle` must be immutable (`frozen=True`).
- Handle edge case: two styles identical in all fields except one should be separate flyweights.
- Add a `to_html()` method on Paragraph that renders the content with inline CSS from the style.

### Think About

- How does Python's string interning relate to Flyweight?
- When would you use `__slots__` alongside Flyweight for even more savings?
- At what scale does Flyweight stop being worth it?
