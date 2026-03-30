# Decorator Pattern — Question 1 (Easy)

## Problem: Coffee Shop Order System

Build a coffee ordering system where base drinks can be decorated with add-ons, each adding to the description and price.

### Requirements

- `Beverage(ABC)`: `description() -> str`, `cost() -> float`
- Base drinks: `Espresso` ($2.00), `HouseBlend` ($1.50)
- Decorators: `Milk` (+$0.50), `Whip` (+$0.70), `Caramel` (+$0.60)

### Expected Usage

```python
drink = Espresso()
drink = Milk(drink)
drink = Whip(drink)
drink = Caramel(drink)

print(drink.description())  # → "Espresso + Milk + Whip + Caramel"
print(drink.cost())          # → 3.80
```

### Constraints

- Decorators can be stacked in any order and multiple times (double milk = +$1.00).
- Each decorator wraps the previous and delegates to it.
