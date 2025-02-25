"""
Flyweight Design pattern
"""

from typing import Dict


class BetterFormattedText:

    def __init__(self, plain_text) -> None:
        self.plain_text = plain_text
        self.formatting = []

    class TextRange:

        def __init__(self, start, end, capitalize=False) -> None:
            self.start = start
            self.end = end
            self.capitalize = capitalize

        def covers(self, position):
            """check if position is valid"""

            return self.start <= position < self.end

    def get_range(self, start, end):
        range = self.TextRange(start, end)
        self.formatting.append(range)
        return range

    def __str__(self) -> str:
        result = []
        for i in range(len(self.plain_text)):
            c = self.plain_text[i]
            for r in self.formatting:
                if r.covers(i) and r.capitalize:
                    c = c.upper()
                    result.append(c)
                else:
                    result.append(c)

        return "".join(result)


# 1️⃣ Flyweight Class
class Character:
    def __init__(self, char: str, font: str, size: int, color: str):
        self.char = char  # Intrinsic state (shared)
        self.font = font
        self.size = size
        self.color = color

    def display(self, position: int):
        print(
            f"Displaying '{self.char}' at position {position} with font={self.font}, size={self.size}, color={self.color}"
        )


# 2️⃣ Flyweight Factory
class CharacterFactory:
    _characters: Dict[str, Character] = {}

    @classmethod
    def get_character(cls, char: str, font: str, size: int, color: str):
        """Creates or reuses a flyweight Character object."""
        key = (char, font, size, color)

        if key not in cls._characters:
            cls._characters[key] = Character(char, font, size, color)
        return cls._characters[key]  # Return shared character


# 3️⃣ Client Code
def main():
    factory = CharacterFactory()

    text = "HELLO WORLD"
    positions = range(len(text))

    # Reuse flyweight objects for same characters
    for char, pos in zip(text, positions):
        character = factory.get_character(char, "Arial", 12, "Black")
        character.display(pos)


if __name__ == "__main__":
    txt = "My name is Sanket"
    bftxt = BetterFormattedText(txt)
    bftxt.get_range(12, 17).capitalize = True
    print(bftxt)
    main()
