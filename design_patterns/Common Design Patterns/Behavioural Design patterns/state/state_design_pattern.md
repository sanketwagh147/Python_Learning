# State Design Pattern

The State Design Pattern is a behavioral design pattern that allows an object to change its behavior when its internal state changes. It helps implement state-dependent behavior while maintaining a clean and maintainable code structure.

## Key Concepts

**Context**: The main object that holds a reference to the current state.  
**State Interface**: Defines common behavior for all possible states.  
**Concrete States**: Different implementations of the state interface, representing various behaviors.  

## When to Use

When an object's: behavior depends on its state.  
When you have multiple if-else or switch statements controlling behavior based on state.  
When you need to encapsulate state-specific logic separately.  

## Real-World Analogy

The buttons and switches in your smartphone behave differently depending on the current state of the device:

When the phone is unlocked, pressing buttons leads to executing various functions.  
When the phone is locked, pressing any button leads to the unlock screen.  
When the phone’s charge is low, pressing any button shows the charging screen.

## Example

```python
from abc import ABC, abstractmethod

# State Interface
class TrafficLightState(ABC):
    @abstractmethod
    def handle(self, traffic_light):
        pass

# Concrete States
class RedLight(TrafficLightState):
    def handle(self, traffic_light):
        print("Red Light - Stop")
        traffic_light.state = GreenLight()  # Transition to Green

class GreenLight(TrafficLightState):
    def handle(self, traffic_light):
        print("Green Light - Go")
        traffic_light.state = YellowLight()  # Transition to Yellow

class YellowLight(TrafficLightState):
    def handle(self, traffic_light):
        print("Yellow Light - Slow Down")
        traffic_light.state = RedLight()  # Transition to Red

# Context
class TrafficLight:
    def __init__(self):
        self.state = RedLight()  # Initial State

    def change(self):
        self.state.handle(self)  # Delegate behavior to the state

# Usage
traffic_light = TrafficLight()

for _ in range(6):
    traffic_light.change()

```
