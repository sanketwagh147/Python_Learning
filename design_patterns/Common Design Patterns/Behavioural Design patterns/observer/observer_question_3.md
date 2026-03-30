# Observer Pattern — Question 3 (Hard)

## Problem: Reactive Property System with Computed Values and Cycle Detection

Build a reactive system where properties notify dependents when changed, and computed properties automatically recalculate (like Vue.js/Excel formulas).

### Requirements

#### Reactive Properties
```python
class ReactiveProperty:
    """Observable property that notifies watchers on change."""
    def __init__(self, name: str, initial_value: Any): ...
    
    @property
    def value(self): ...
    
    @value.setter
    def value(self, new_val): ...  # triggers update to all dependents
    
    def watch(self, callback: Callable): ...
    def unwatch(self, callback: Callable): ...

class ComputedProperty:
    """Automatically recalculates when any dependency changes."""
    def __init__(self, name: str, compute_fn: Callable, dependencies: list[ReactiveProperty]): ...
    
    @property
    def value(self): ...  # returns cached computed value
```

#### Scenario: Shopping Cart

```python
price = ReactiveProperty("price", 100.0)
quantity = ReactiveProperty("quantity", 2)
tax_rate = ReactiveProperty("tax_rate", 0.08)

subtotal = ComputedProperty("subtotal", lambda: price.value * quantity.value, [price, quantity])
tax = ComputedProperty("tax", lambda: subtotal.value * tax_rate.value, [subtotal, tax_rate])
total = ComputedProperty("total", lambda: subtotal.value + tax.value, [subtotal, tax])
```

### Expected Usage

```python
total.watch(lambda: print(f"Total changed: ${total.value:.2f}"))

print(total.value)  # → $216.00 (100 * 2 + 100 * 2 * 0.08)

quantity.value = 3
# → Total changed: $324.00 (auto-recalculated!)

price.value = 50
# → Total changed: $162.00

tax_rate.value = 0.10
# → Total changed: $165.00
```

### Key Challenges

1. **Computed depends on computed**: `total` depends on `tax`, which depends on `subtotal`. Changes to `price` cascade: `price → subtotal → tax → total`.
2. **Avoid redundant recalculation**: if both `subtotal` and `tax` change (because price changed), `total` should only recalculate ONCE.
3. **Cycle detection**: prevent `a depends on b depends on a`.
4. **Batching**: multiple changes in quick succession should batch notifications.

### Constraints

- Implement topological sorting for update order (dependencies before dependents).
- Use a dirty-flag approach: mark as dirty, recalculate lazily on access.
- `ComputedProperty` can depend on other `ComputedProperty` objects (transitive).
- Cycle detection at registration time — raise `CyclicDependencyError`.
- Write tests for: basic reactivity, cascading updates, cycle detection, watch/unwatch.

### Think About

- How does Vue.js's reactivity system work at a high level? How is it similar to this?
- How does Excel recalculate cells? What's the dependency graph?
- Could you make this thread-safe for concurrent access?
