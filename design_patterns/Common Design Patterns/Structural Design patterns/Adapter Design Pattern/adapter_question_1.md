# Adapter Pattern — Question 1 (Easy)

## Problem: Temperature Sensor Adapter

You have a third-party `FahrenheitSensor` that returns temperature in Fahrenheit, but your application exclusively works with Celsius.

### Requirements

- `FahrenheitSensor` (existing, cannot modify):
  ```python
  class FahrenheitSensor:
      def get_temperature_f(self) -> float:
          return 98.6  # simulated reading
  ```
- Your app expects: `sensor.get_temperature()` → returns Celsius.
- Create a `CelsiusAdapter` that wraps `FahrenheitSensor` and exposes `get_temperature() -> float`.

### Expected Usage

```python
raw_sensor = FahrenheitSensor()
sensor = CelsiusAdapter(raw_sensor)

print(sensor.get_temperature())  # → 37.0
```

### Constraints

- Do NOT modify `FahrenheitSensor`.
- Formula: `C = (F - 32) * 5/9`
- Round to 1 decimal place.
