# Visitor Design pattern

The Visitor Pattern allows you to add new operations to existing object structures without modifying their classes. Instead of modifying the objects themselves, you define a separate visitor class that implements the new behavior.

## Visitor Pattern Structure

The Visitor pattern consists of:

1. Element (Visitable):
    - The objects (e.g., Circle, Square) that can be visited.  
    - They implement an accept(visitor) method.
2. Visitor (Operation on Element)
    - Defines methods like visit_circle(), visit_square() to process each type.

## Example (Violates OCP)

```python
class Circle:
    def __init__(self, radius):
        self.radius = radius

    def calculate_area(self):
        return 3.14 * self.radius * self.radius

    def render_svg(self):
        return f"<circle r='{self.radius}'/>"

class Square:
    def __init__(self, side):
        self.side = side

    def calculate_area(self):
        return self.side * self.side

    def render_svg(self):
        return f"<rect width='{self.side}' height='{self.side}'/>"
```

## Example (Follows OCP)

```python
class ShapeVisitor:
    def visit_circle(self, circle):
        pass

    def visit_square(self, square):
        pass


class AreaCalculator(ShapeVisitor):
    def visit_circle(self, circle):
        return 3.14 * circle.radius * circle.radius

    def visit_square(self, square):
        return circle.side * circle.side


class SvgRenderer(ShapeVisitor):
    def visit_circle(self, circle):
        return f"<circle r='{circle.radius}'/>"

    def visit_square(self, square):
        return f"<rect width='{square.side}' height='{square.side}'/>"


class Shape:
    def accept(self, visitor):
        method_name = f"visit_{self.__class__.__name__.lower()}"
        return getattr(visitor, method_name)(self)


class Circle(Shape):
    def __init__(self, radius):
        self.radius = radius


class Square(Shape):
    def __init__(self, side):
        self.side = side


# Usage
circle = Circle(5)
square = Square(4)

area_calculator = AreaCalculator()
svg_renderer = SvgRenderer()

print(circle.accept(area_calculator))  # Output: 78.5
print(circle.accept(svg_renderer))     # Output: <circle r='5'/>

```

## Advantages of Visitor Pattern

✅ Open-Closed Principle (OCP) Compliance.  
✅ Encapsulation of Operations
✅ Easy to Add New Operations  
✅ Promotes Single Responsibility Principle (SRP)

## When to Use the Visitor Pattern?

✅ When you frequently add new operations to a class hierarchy.
✅ When the object structure is stable, but new behaviors are needed.
✅ When you want to keep operations separate from the objects they act on.

## Avoid it when

The class hierarchy frequently changes (adding new shapes requires modifying visitors).  
Only one or two operations are needed (simpler methods might be better)

## Conclusion

The Visitor Pattern is great for adding new operations but not ideal if new elements (shapes) are frequently introduced.
