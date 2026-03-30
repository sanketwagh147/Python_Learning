# Observer Pattern — Question 1 (Easy)

## Problem: Weather Station with Multiple Displays

A weather station publishes temperature updates. Multiple displays subscribe and react to changes.

### Requirements

- `WeatherStation` (subject): `register(observer)`, `unregister(observer)`, `set_temperature(temp)`
- `Display(ABC)` (observer): `update(temperature: float)`
- Concrete: `PhoneDisplay`, `TVDisplay`, `WebDashboard`

### Expected Usage

```python
station = WeatherStation()
phone = PhoneDisplay("Alice's Phone")
tv = TVDisplay("Living Room TV")

station.register(phone)
station.register(tv)

station.set_temperature(25.0)
# → [Alice's Phone] Temperature updated: 25.0°C
# → [Living Room TV] Temperature updated: 25.0°C

station.unregister(tv)
station.set_temperature(30.0)
# → [Alice's Phone] Temperature updated: 30.0°C
# (TV not notified — unregistered)
```

### Constraints

- Observers don't know about each other.
- Subject doesn't know the type of observers — only the interface.
- Support any number of observers.
