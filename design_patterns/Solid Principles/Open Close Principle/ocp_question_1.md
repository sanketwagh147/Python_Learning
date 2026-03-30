# Open-Closed Principle — Question 1 (Easy)

## Problem: Shape Area Calculator Without if/elif

Calculate areas for different shapes without modifying existing code when new shapes are added.

### The Violating Code

```python
class AreaCalculator:
    def calculate(self, shape):
        if shape["type"] == "circle":
            return 3.14 * shape["radius"] ** 2
        elif shape["type"] == "rectangle":
            return shape["width"] * shape["height"]
        elif shape["type"] == "triangle":
            return 0.5 * shape["base"] * shape["height"]
        else:
            raise ValueError(f"Unknown shape: {shape['type']}")
```

**Problem**: Adding a new shape (e.g., Trapezoid) requires modifying `AreaCalculator`.

### Requirements

Refactor to follow OCP:
- `Shape(ABC)` with abstract `area() -> float` method.
- Concrete: `Circle`, `Rectangle`, `Triangle`
- `AreaCalculator`: works with any `Shape` — no `if/elif` needed.

### Expected Usage After Refactor

```python
shapes = [Circle(5), Rectangle(4, 6), Triangle(3, 8)]
calculator = AreaCalculator()

for shape in shapes:
    print(f"{shape}: {calculator.calculate(shape):.2f}")

# Adding new shape — NO changes to AreaCalculator!
class Trapezoid(Shape):
    def __init__(self, a, b, h):
        self.a, self.b, self.h = a, b, h
    def area(self):
        return 0.5 * (self.a + self.b) * self.h

shapes.append(Trapezoid(3, 5, 4))
# Calculator still works without modification!
```

### Constraints

- `AreaCalculator` class is NEVER modified after initial creation.
- New shapes are added by creating new classes, not touching existing code.
