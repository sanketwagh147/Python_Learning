# Mediator Pattern — Question 2 (Medium)

## Problem: Airport Traffic Control System

Aircraft don't communicate with each other directly. The control tower (mediator) coordinates takeoffs, landings, and runway allocation.

### Requirements

#### Mediator
```python
class ControlTower:
    def register_aircraft(self, aircraft: Aircraft): ...
    def request_landing(self, aircraft: Aircraft) -> bool: ...
    def request_takeoff(self, aircraft: Aircraft) -> bool: ...
    def notify_all(self, message: str, exclude: Aircraft = None): ...
```

#### Colleague
```python
class Aircraft:
    callsign: str
    state: str  # "airborne", "landing", "on_ground", "taking_off"
    
    def land(self) -> None: ...
    def takeoff(self) -> None: ...
    def receive_notification(self, message: str): ...
```

#### Rules (enforced by mediator)
- Only ONE aircraft can use the runway at a time.
- Landing has priority over takeoff.
- When an aircraft requests landing, all others are notified to hold.
- After landing/takeoff completes, next queued request is processed.

### Expected Usage

```python
tower = ControlTower()
a1 = Aircraft("AA-100", tower)
a2 = Aircraft("UA-200", tower)
a3 = Aircraft("DL-300", tower)

a1.land()
# → [Tower] AA-100 cleared for landing. Runway occupied.
# → [UA-200] Notification: Hold position — AA-100 is landing

a2.takeoff()  # queued — runway busy
# → [Tower] UA-200 queued for takeoff

a3.land()  # queued with priority
# → [Tower] DL-300 queued for landing (priority)

# After AA-100 lands...
# → [Tower] DL-300 cleared for landing (priority over UA-200's takeoff)
```

### Constraints

- Use a priority queue: landing requests before takeoff requests.
- Aircraft don't know about each other — all coordination through the tower.
- Track runway state: `free`, `occupied_landing`, `occupied_takeoff`.

### Think About

- How does this reduce coupling? What if aircraft communicated directly?
- How would you add multiple runways?
