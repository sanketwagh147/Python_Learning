# Specification Pattern — Question 1 (Easy)

## Problem: Product Filter with Composable Specifications

Filter products in an online store using composable specification objects instead of hardcoded filter logic.

### Requirements

```python
class Specification(ABC):
    @abstractmethod
    def is_satisfied_by(self, item) -> bool: ...
    
    def __and__(self, other): ...  # AndSpec
    def __or__(self, other): ...   # OrSpec
    def __invert__(self): ...      # NotSpec
```

Concrete:
- `PriceBelow(max_price)`: price < max
- `InCategory(category)`: matches category
- `InStock()`: stock > 0
- `MinRating(min_rating)`: rating >= min

### Expected Usage

```python
products = [
    Product("Laptop", price=999, category="electronics", stock=5, rating=4.5),
    Product("Book", price=15, category="books", stock=0, rating=4.8),
    Product("Phone", price=699, category="electronics", stock=10, rating=3.9),
    Product("Shirt", price=25, category="clothing", stock=20, rating=4.2),
]

# Affordable electronics in stock
spec = PriceBelow(800) & InCategory("electronics") & InStock()
results = [p for p in products if spec.is_satisfied_by(p)]
# → [Phone]

# Highly rated OR cheap
spec2 = MinRating(4.5) | PriceBelow(30)
results2 = [p for p in products if spec2.is_satisfied_by(p)]
# → [Laptop, Book, Shirt]

# NOT electronics
spec3 = ~InCategory("electronics")
results3 = [p for p in products if spec3.is_satisfied_by(p)]
# → [Book, Shirt]
```

### Constraints

- Specifications are reusable and composable.
- New filters = new Specification classes. No changes to existing code.
