# Memento Pattern — Question 1 (Easy)

## Problem: Text Editor Snapshot (Save/Restore)

Build a text editor that can save snapshots of its state and restore to any previous snapshot.

### Requirements

- `EditorMemento`: stores `content: str`, `cursor_position: int`, `timestamp`
- `TextEditor` (originator): `type(text)`, `move_cursor(pos)`, `save() -> EditorMemento`, `restore(memento)`
- `History` (caretaker): `push(memento)`, `pop() -> EditorMemento`, `list_snapshots()`

### Expected Usage

```python
editor = TextEditor()
history = History()

editor.type("Hello ")
history.push(editor.save())

editor.type("World")
history.push(editor.save())

editor.type("!!!")
print(editor.content)  # → "Hello World!!!"

editor.restore(history.pop())
print(editor.content)  # → "Hello World"

editor.restore(history.pop())
print(editor.content)  # → "Hello "
```

### Constraints

- `EditorMemento` should be **opaque** — the `History` class cannot access or modify its internals.
- Use `__slots__` or make memento attributes private.
- `save()` returns a NEW memento each time (not a reference to internal state).
