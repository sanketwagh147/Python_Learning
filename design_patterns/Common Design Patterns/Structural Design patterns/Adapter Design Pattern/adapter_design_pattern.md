# Adapter Design pattern

The Adapter Pattern is a structural design pattern that allows objects with incompatible interfaces to work together. It acts as a bridge between two different interfaces, enabling a class to be used in a way that it was not originally designed for.

## Key Concept

The Adapter pattern converts the interface of a class into another interface that a client expects. It is useful when integrating new code with legacy code or third-party libraries.

## Components of the Adapter Pattern

1. Target (Expected Interface): The existing interface that the client expects.
2. Adaptee (Existing Class): The class that needs adaptation.
3. Adapter: A class that bridges the gap between the Target and the Adaptee by converting calls from one interface to another.

## Example

```python
# Target Interface
class Target:
    def request(self):
        """This is the expected interface method."""
        raise NotImplementedError("You should implement this method.")

# Adaptee with an incompatible interface.
class Adaptee:
    def specific_request(self):

        # task which will make it compatible
        return "Adaptee's specific request."


# Object Adapter using composition.
class ObjectAdapter(Target):
    def __init__(self, adaptee):
        self.adaptee = adaptee

    def request(self):
        # Delegate the call to the adaptee's method.
        return self.adaptee.specific_request()

# Client code using the adapter.
adaptee_instance = Adaptee()
adapter = ObjectAdapter(adaptee_instance)
print("Object Adapter Output:", adapter.request())
```

## Key Takeaways

- ✅ Bridges incompatible interfaces without modifying existing code.
- ✅ Composition (Object Adapter) is preferred for better flexibility.
- ✅ Used in real-world scenarios like API integrations, legacy system support, and data conversion.

## When to Use Adapter Pattern?

- ✔️ When integrating third-party libraries that have different method names.
- ✔️ When using legacy code that needs to be adapted to a new interface.
- ✔️ When two incompatible systems need to work together without modifying them.
