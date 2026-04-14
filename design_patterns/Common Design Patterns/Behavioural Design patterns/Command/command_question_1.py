


from abc import ABC, abstractmethod


class Command(ABC):
    @abstractmethod
    def execute(self, editor: "TextEditor"):
        pass

    @abstractmethod
    def undo(self, editor: "TextEditor"):
        pass

class TypeCommand(Command):
    def __init__(self, text: str):
        self.text = text
        self.start_pos = 0

    def execute(self, editor: "TextEditor"):
        self.start_pos = editor._cursor_pos
        editor.text += self.text
        editor._cursor_pos += len(self.text)

    def undo(self, editor: "TextEditor"):
        # Remove the text that was added
        editor.text = editor.text[:self.start_pos]
        editor._cursor_pos = self.start_pos

class DeleteCommand(Command):
    def __init__(self, count: int):
        self.count = count
        self.deleted_text = ""

    def execute(self, editor: "TextEditor"):
        # Store the deleted text for undo
        self.deleted_text = editor.text[-self.count:] if self.count <= len(editor.text) else editor.text
        editor.text = editor.text[:-self.count]
        editor._cursor_pos -= self.count

    def undo(self, editor: "TextEditor"):
        editor.text += self.deleted_text
        editor._cursor_pos += len(self.deleted_text)


class TextEditor:
    def __init__(self):
        self.text: str = ""
        self._cursor_pos: int = 0
        self._command_history: list[Command] = []

    def execute(self, command: Command):
        command.execute(self)
        self._command_history.append(command)

    def undo(self):
        if not self._command_history:
            return
        last_command = self._command_history.pop()
        last_command.undo(self)


if __name__ == "__main__": 
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
        