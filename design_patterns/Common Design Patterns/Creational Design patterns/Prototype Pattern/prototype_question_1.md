# Prototype Pattern — Question 1 (Easy)

## Problem: Document Template Cloner

A document management system has pre-built templates. Users clone a template and customize it rather than building from scratch.

### Requirements

- Create a `Document` class with: `title`, `content`, `font`, `font_size`, `margins` (dict).
- Implement a `clone()` method that returns a **deep copy**.
- Changing the clone must NOT affect the original.

### Expected Usage

```python
template = Document(
    title="Untitled",
    content="",
    font="Arial",
    font_size=12,
    margins={"top": 1, "bottom": 1, "left": 1.5, "right": 1.5}
)

my_doc = template.clone()
my_doc.title = "My Resume"
my_doc.content = "Work experience..."
my_doc.margins["left"] = 2.0

print(template.margins["left"])  # → 1.5 (unchanged!)
print(my_doc.margins["left"])    # → 2.0
```

### Constraints

- Use `copy.deepcopy` inside `clone()`.
- Demonstrate that shallow copy would fail (mutating nested `margins` dict on clone affects original).

### Hints

```python
import copy

class Document:
    def clone(self):
        return copy.deepcopy(self)
```
