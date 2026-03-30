# Composite Pattern — Question 1 (Easy)

## Problem: File System Tree

Model a file system where **directories** contain **files** and other **directories**, and you can compute the total size of any node.

### Requirements

- `FileSystemItem(ABC)` with:
  - `name: str`
  - `get_size() -> int` (abstract)
  - `display(indent: int)` (abstract)

- `File(FileSystemItem)`: leaf node with a fixed `size` in bytes.
- `Directory(FileSystemItem)`: composite that holds children (Files and Directories).
  - `add(item)`, `remove(item)`
  - `get_size()` returns **sum** of all children's sizes (recursive).

### Expected Usage

```python
root = Directory("project")
src = Directory("src")
src.add(File("main.py", 1200))
src.add(File("utils.py", 800))

tests = Directory("tests")
tests.add(File("test_main.py", 600))

root.add(src)
root.add(tests)
root.add(File("README.md", 200))

print(root.get_size())  # → 2800
root.display(0)
# project/
#   src/
#     main.py (1200 bytes)
#     utils.py (800 bytes)
#   tests/
#     test_main.py (600 bytes)
#   README.md (200 bytes)
```

### Constraints

- `display()` should indent children using 2 spaces per level.
- Directories display with a trailing `/`.
