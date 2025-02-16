# Builder pattern

The Builder pattern is a creational design pattern used to construct complex objects step by step.
It allows you to create different representations of an object using the same construction process

### Why to use Builder Pattern ?
- Handling of complex object creation: In case the object has too many optional params or configs ,using constructors with too many parameters can become confusion
- The step by step construction process makes code easier to understand
- Separated object construction from its representation


### How to make one
1. **Builder**: Defines steps to build the object
2. **Concrete Builder**: Implement steps to create specific representation
3. **Director(Optional)** : Control the building process
4. **Product**: The final complex object which is created.

# Example 
```python
# Product: The complex object  we want to create

class Computer:

    def __init__(self):
        self.cpu = None
        self.ram = None
        self.storage = None

    def __str__(self):
        return f"<Computer with {self.cpu}, {self.ram} RAM and {self.storage} Storage"

# Builder Interface
class ComputerBuilder:

    def set_cpu(self,cpu):
        ...
    def set_ram(self,ram):
        ...
    def set_storage(self,storage):
        ...
    def build(self):
        ...

# Concrete Builder

class GamingComputerBuilder(ComputerBuilder):

    def __init__(self):
        self.computer = Computer()

    
    def set_cpu(self,cpu):
        self.computer.cpu = cpu

    def set_ram(self,ram):
        self.computer.ram = ram

    def set_storage(self,storage):
        self.computer.storage = storage
        
    def build(self):
        return self.computer

# Director (optional)
class ComputerDirector:
    @staticmethod
    def construct_gaming_computer(cpu, ram, storage):
        return (
            GamingComputerBuilder()
            .set_cpu(cpu)
            .set_ram(ram)
            .set_storage(storage)
            .build()
        )

# Client Code
gaming_pc = ComputerDirector.construct_gaming_computer("AMD Ryzen 9", "64GB", "2TB NVMe SSD")
print(gaming_pc)

```

### When to use builder pattern
1. Object has many optional or complex configurations
2. Want to separate object creation from its representation
3. If you need a step-by-step process to build an object



