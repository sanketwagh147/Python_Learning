# Iterator Pattern — Question 1 (Easy)

## Problem: Range Iterator with Custom Step

Build a custom iterator that generates numbers in a range with a step, similar to `range()` but as a class implementing the iterator protocol.

### Requirements

- `CountUp(start, stop, step)`: implements `__iter__` and `__next__`
- Raises `StopIteration` when past the stop value
- Works with `for` loops, `list()`, and `next()`

### Expected Usage

```python
counter = CountUp(1, 10, 2)
for num in counter:
    print(num)
# → 1, 3, 5, 7, 9

print(list(CountUp(0, 5, 1)))  # → [0, 1, 2, 3, 4]

c = CountUp(10, 15, 3)
print(next(c))  # → 10
print(next(c))  # → 13
```

### Constraints

- Implement `__iter__` (returns self) and `__next__` (returns next value or raises `StopIteration`).
- Must be lazy — don't precompute all values.
- Support negative steps (countdown): `CountUp(10, 0, -2)` → 10, 8, 6, 4, 2
