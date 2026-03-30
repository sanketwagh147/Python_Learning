# State Pattern — Question 1 (Easy)

## Problem: Traffic Light System

A traffic light cycles through states: Green → Yellow → Red → Green. Each state has different behavior.

### Requirements

- `TrafficLightState(ABC)`: `handle(light)`, `color() -> str`
- States: `GreenState`, `YellowState`, `RedState`
- `TrafficLight`: `change()` transitions to next state, `current_color()` returns color.

### Expected Usage

```python
light = TrafficLight()
print(light.current_color())  # → "Green"
light.change()
print(light.current_color())  # → "Yellow"
light.change()
print(light.current_color())  # → "Red"
light.change()
print(light.current_color())  # → "Green" (cycles!)
```

### Constraints

- State transitions are encapsulated INSIDE each state class (GreenState knows it goes to YellowState).
- `TrafficLight` simply delegates to its current state — it doesn't contain transition logic.
- No `if/elif` chains in the TrafficLight class.
