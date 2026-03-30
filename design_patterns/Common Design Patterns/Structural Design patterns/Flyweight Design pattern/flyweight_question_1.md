# Flyweight Pattern — Question 1 (Easy)

## Problem: Text Editor Character Rendering

A text editor stores millions of characters. Instead of each character object storing its own font/size/color, share these intrinsic properties via Flyweight.

### Requirements

- `CharacterStyle` (flyweight): stores `font`, `size`, `color` — shared and immutable.
- `CharacterStyleFactory`: returns existing style if already created, or creates a new one.
- `Character`: stores the actual `char` (extrinsic) + a reference to its `CharacterStyle` (flyweight).

### Expected Usage

```python
factory = CharacterStyleFactory()

style1 = factory.get_style("Arial", 12, "black")
style2 = factory.get_style("Arial", 12, "black")
style3 = factory.get_style("Arial", 14, "red")

print(style1 is style2)  # True — same object, reused!
print(style1 is style3)  # False — different config

chars = [
    Character("H", style1), Character("e", style1),
    Character("l", style1), Character("l", style1),
    Character("o", style3),  # "o" in red, bigger
]

print(factory.pool_size())  # 2 (only 2 unique styles)
```

### Constraints

- The factory must use a dictionary to cache styles by `(font, size, color)` tuple.
- `CharacterStyle` should be immutable (use `__slots__` or `@dataclass(frozen=True)`).
- Show the memory savings: without flyweight = N style objects; with flyweight = M unique styles (M << N).
