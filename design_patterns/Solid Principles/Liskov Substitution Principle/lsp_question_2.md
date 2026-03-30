# Liskov Substitution Principle — Question 2 (Medium)

## Problem: Rectangle/Square — The Classic LSP Trap

Mathematically, a Square IS a Rectangle. But in code, making `Square` extend `Rectangle` violates LSP.

### The Violating Code

```python
class Rectangle:
    def __init__(self, width, height):
        self._width = width
        self._height = height
    
    @property
    def width(self):
        return self._width
    
    @width.setter
    def width(self, value):
        self._width = value
    
    @property
    def height(self):
        return self._height
    
    @height.setter
    def height(self, value):
        self._height = value
    
    def area(self):
        return self._width * self._height

class Square(Rectangle):
    def __init__(self, side):
        super().__init__(side, side)
    
    @Rectangle.width.setter
    def width(self, value):
        self._width = value
        self._height = value  # must keep sides equal
    
    @Rectangle.height.setter
    def height(self, value):
        self._width = value
        self._height = value

# This function breaks with Square
def resize_rectangle(rect: Rectangle):
    rect.width = 10
    rect.height = 5
    assert rect.area() == 50  # Fails for Square! (area = 25)
```

### Requirements

1. **Explain** why this violates LSP (what invariant/postcondition does Square break?).
2. **Refactor** using one of these approaches:
   - Approach A: Separate `Shape` ABC with `area()` — `Rectangle` and `Square` are siblings, not parent-child.
   - Approach B: Make `Rectangle` immutable (no setters) — creating a new shape instead of mutating.
   - Approach C: `Square` is a factory method that creates a `Rectangle` with equal sides (composition).

3. Implement ALL THREE approaches and discuss trade-offs.

### Expected Usage (Approach A)

```python
class Shape(ABC):
    def area(self) -> float: ...

class Rectangle(Shape):
    def __init__(self, w, h): ...
    def area(self): return self.width * self.height

class Square(Shape):
    def __init__(self, side): ...
    def area(self): return self.side ** 2

# No inheritance relationship — can't substitute incorrectly
shapes: list[Shape] = [Rectangle(10, 5), Square(7)]
for s in shapes:
    print(s.area())  # Always correct!
```

### Think About

- "Is-a" in mathematics ≠ "Is-a" in programming. Why?
- What is the difference between behavioral subtyping (LSP) and structural subtyping?
- How do immutable objects help prevent LSP violations?
