# Mediator pattern

Mediator is a behavioral design pattern that lets you reduce chaotic dependencies between objects. The pattern restricts direct communications between the objects and forces them to collaborate only via a mediator object.

## Key Features of the Mediator Pattern

**Decouples Components**: Objects no longer communicate directly; instead, they interact through a central mediator.  
**Simplifies Object Relationships**: Reduces complex many-to-many dependencies.  
**Encapsulates Communication Logic**: Centralizes how components interact.  
**Supports Maintainability & Scalability**: Adding new components is easier without modifying existing ones.  

## Example: ATC Mediator in Python

```python

class AirTrafficControl:
    def __init__(self):
        self.airplanes = []

    def register(self, airplane):
        self.airplanes.append(airplane)

    def send_message(self, message, sender):
        for airplane in self.airplanes:
            if airplane != sender:
                airplane.receive_message(message)

class Airplane:
    def __init__(self, name, atc):
        self.name = name
        self.atc = atc
        self.atc.register(self)

    def send_message(self, message):
        print(f"{self.name} sends: {message}")
        self.atc.send_message(message, self)

    def receive_message(self, message):
        print(f"{self.name} received: {message}")

# Usage
atc = AirTrafficControl()
plane1 = Airplane("Flight 101", atc)
plane2 = Airplane("Flight 202", atc)

plane1.send_message("Requesting permission to land")
plane2.send_message("Clearing runway for landing")

```

## Example: Microservices Mediator

```python
class MessageBroker:
    def __init__(self):
        self.services = {}

    def register(self, service_name, service):
        self.services[service_name] = service

    def send_message(self, service_name, message):
        if service_name in self.services:
            self.services[service_name].receive_message(message)

class Service:
    def __init__(self, name, broker):
        self.name = name
        self.broker = broker
        self.broker.register(name, self)

    def send_message(self, to_service, message):
        print(f"{self.name} sends message to {to_service}: {message}")
        self.broker.send_message(to_service, message)

    def receive_message(self, message):
        print(f"{self.name} received: {message}")

# Usage
broker = MessageBroker()
service_a = Service("ServiceA", broker)
service_b = Service("ServiceB", broker)

service_a.send_message("ServiceB", "Hello, ServiceB!")
service_b.send_message("ServiceA", "Hello, ServiceA!")

```

## Steps to Implement the Mediator Pattern

1️⃣ Identify Colleagues – Determine objects that need to communicate without direct dependencies.

2️⃣ Define a Mediator Interface – Create an abstract class or interface defining communication methods.

3️⃣ Implement a Concrete Mediator – Manage interactions between colleagues and handle communication logic.

4️⃣ Define Colleague Components – Ensure components interact only via the mediator, not directly with each other.

5️⃣ Instantiate and Use the Mediator – Register colleagues, trigger communication through the mediator.

6️⃣ Extend for More Functionality (Optional) – Implement event-based mediation, custom logic, or use a Singleton for a single mediator instance.

This approach reduces dependencies, simplifies interactions, and improves maintainability.

## Conclusion

The Mediator Pattern is useful when: ✅ You need to reduce direct dependencies between objects.  
✅ Multiple components must communicate but should not be tightly coupled.  
✅ You want a centralized way to handle communication.
