# Memento Design pattern

## Definition

The Memento Pattern is a behavioral design pattern used to capture and restore an object's state without exposing its internal details. It allows for undo/redo functionality by storing snapshots of an object's state.

## 1️⃣ Key Components

**Originator** – The object whose state needs to be saved and restored.  
**Memento** – Stores the internal state of the originator.
**Caretaker** – Manages the saved states (mementos) but does not modify them.

## 2️⃣ When to Use?

✔ Implementing Undo/Redo functionality (e.g., text editors, games).  
✔ Restoring previous states (e.g., database transactions, version control).  
✔ Protecting the encapsulation of object state.

## 3️⃣ Advantages & Disadvantages

✔ Encapsulation preserved – Internal state is hidden from external objects.  
✔ Undo/Redo support – Enables state rollback functionality.  
✔ Simplifies state management – Previous states are stored efficiently.  

❌ Memory overhead – Storing too many states can consume excessive memory.  
❌ Performance issues – Frequent state saving may slow down execution.

## The Memento Pattern helps preserve state and improve user experience in web applications

## Python Example

```python
# Memento: Stores the state
class Memento:
    def __init__(self, state):
        self._state = state

    def get_state(self):
        return self._state

# Originator: Holds the current state and creates/restores mementos
class TextEditor:
    def __init__(self):
        self._content = ""

    def write(self, text):
        self._content = text

    def save(self):
        return Memento(self._content)  # Save state

    def restore(self, memento):
        self._content = memento.get_state()  # Restore state

    def show(self):
        print(f"Current Content: {self._content}")

# Caretaker: Manages undo/redo functionality
class History:
    def __init__(self):
        self._undo_stack = []  # Stores saved states
        self._redo_stack = []  # Stores undone states

    def backup(self, memento):
        self._undo_stack.append(memento)  # Save state
        self._redo_stack.clear()  # Clear redo history on new action

    def undo(self):
        if self._undo_stack:
            self._redo_stack.append(self._undo_stack.pop())  # Move to redo stack
            return self._undo_stack[-1] if self._undo_stack else None
        return None

    def redo(self):
        if self._redo_stack:
            memento = self._redo_stack.pop()
            self._undo_stack.append(memento)  # Restore last undone state
            return memento
        return None

# Example Usage
editor = TextEditor()
history = History()

# Initial Write
editor.write("Hello, World!")
history.backup(editor.save())
editor.show()

# Modify Text
editor.write("Hello, Python!")
history.backup(editor.save())
editor.show()

# Undo
memento = history.undo()
if memento:
    editor.restore(memento)
editor.show()

# Redo
memento = history.redo()
if memento:
    editor.restore(memento)
editor.show()
```
