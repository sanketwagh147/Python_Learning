# Command Pattern — Question 1 (Easy)

## Problem: Text Editor with Undo

Build a simple text editor that supports typing text and undoing the last action.

### Requirements

- `Command(ABC)`: `execute()`, `undo()`
- `TypeCommand`: adds text at the cursor position
- `DeleteCommand`: deletes N characters from cursor position
- `TextEditor`: has a buffer (string), cursor position, and command history

### Expected Usage

```python
editor = TextEditor()
editor.execute(TypeCommand("Hello "))
editor.execute(TypeCommand("World"))
print(editor.text)  # → "Hello World"

editor.undo()
print(editor.text)  # → "Hello "

editor.execute(TypeCommand("Python"))
print(editor.text)  # → "Hello Python"

editor.execute(DeleteCommand(3))
print(editor.text)  # → "Hello Pyt"

editor.undo()
print(editor.text)  # → "Hello Python"
```

### Constraints

- Each command is stored in a history stack.
- `undo()` pops the last command and calls its `undo()` method.
- Commands must capture enough state to reverse themselves.
