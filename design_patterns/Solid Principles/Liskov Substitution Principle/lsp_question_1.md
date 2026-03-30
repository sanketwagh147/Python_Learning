# Liskov Substitution Principle — Question 1 (Easy)

## Problem: Bird Hierarchy — Can All Birds Fly?

A classic LSP violation: a `Penguin` is a `Bird`, but penguins can't fly.

### The Violating Code

```python
class Bird:
    def fly(self):
        return "Flying!"

class Penguin(Bird):
    def fly(self):
        raise NotImplementedError("Penguins can't fly!")

def make_bird_fly(bird: Bird):
    print(bird.fly())  # Crashes for Penguin!
```

**Problem**: Code that works with `Bird` breaks when given a `Penguin`. This violates LSP.

### Requirements

Refactor so that subtypes can always replace the base type:

```python
class Bird(ABC):
    def move(self) -> str: ...
    def eat(self) -> str: ...

class FlyingBird(Bird):
    def fly(self) -> str: ...

class SwimmingBird(Bird):
    def swim(self) -> str: ...
```

Concrete: `Eagle(FlyingBird)`, `Penguin(SwimmingBird)`, `Duck(FlyingBird, SwimmingBird)` — yes, ducks both fly AND swim!

### Expected Usage

```python
birds: list[Bird] = [Eagle(), Penguin(), Duck()]

for bird in birds:
    print(bird.move())  # All birds can move — no crashes!

flying_birds: list[FlyingBird] = [Eagle(), Duck()]
for fb in flying_birds:
    print(fb.fly())  # Only ever called on birds that CAN fly
```

### Constraints

- Any function accepting `Bird` works with ALL bird subtypes.
- `Penguin` is never passed to code expecting `FlyingBird`.
- No `NotImplementedError` or `raise` in any overridden method.
