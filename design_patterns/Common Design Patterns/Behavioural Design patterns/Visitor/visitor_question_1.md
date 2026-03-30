# Visitor Pattern — Question 1 (Easy)

## Problem: Shape Area and Perimeter Calculator

Different shapes need different calculation formulas. Use Visitor to add operations without modifying shape classes.

### Requirements

- Shapes: `Circle(radius)`, `Rectangle(width, height)`, `Triangle(a, b, c)`
- Each shape has `accept(visitor)`.
- Visitors:
  - `AreaVisitor`: calculates area for each shape
  - `PerimeterVisitor`: calculates perimeter for each shape

### Expected Usage

```python
shapes = [Circle(5), Rectangle(4, 6), Triangle(3, 4, 5)]

area_calc = AreaVisitor()
for shape in shapes:
    print(f"{shape}: area = {shape.accept(area_calc)}")
# → Circle(r=5): area = 78.54
# → Rectangle(4x6): area = 24.00
# → Triangle(3,4,5): area = 6.00

perimeter_calc = PerimeterVisitor()
for shape in shapes:
    print(f"{shape}: perimeter = {shape.accept(perimeter_calc)}")
# → Circle(r=5): perimeter = 31.42
# → Rectangle(4x6): perimeter = 20.00
# → Triangle(3,4,5): perimeter = 12.00
```

### Constraints

- Shape classes do NOT contain calculation logic — only `accept(visitor)`.
- Adding a new operation (e.g., `DrawVisitor`) requires NO changes to shape classes.
- Use double dispatch: `shape.accept(visitor)` → `visitor.visit_circle(self)`.
