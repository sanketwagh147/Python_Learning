"""
Neural network example
"""

from abc import ABC
from collections.abc import Iterable


class Connectable(Iterable, ABC):
    def connect_to(self, other):
        """Connect neurons or layers"""
        if self == other:
            return

        for s in self:
            for o in other:
                s.outputs.append(o)
                o.inputs.append(s)


class Neuron(Connectable):
    def __init__(self, name):
        self.name = name
        self.inputs = []
        self.outputs = []

    def __iter__(self):
        """Make Neuron iterable (yields itself)"""
        yield self

    def __str__(self):
        return f"{self.name}, {len(self.inputs)} inputs, {len(self.outputs)} outputs"


class NeuronLayer(list, Connectable):
    def __init__(self, name, count):
        """Creates a layer of neurons"""
        super().__init__()
        self.name = name
        for x in range(count):
            self.append(Neuron(f"{name}-{x}"))

    def __str__(self):
        return f"{self.name} with {len(self)} neurons"


# Example Usage
if __name__ == "__main__":
    n1 = Neuron("Neuron-1")
    n2 = Neuron("Neuron-2")
    layer1 = NeuronLayer("Layer-1", 3)
    layer2 = NeuronLayer("Layer-2", 2)

    # Connect individual neurons
    n1.connect_to(n2)

    # Connect a neuron to a layer
    n1.connect_to(layer1)

    # Connect two layers
    layer1.connect_to(layer2)

    # Print results
    print(n1)
    print(n2)
    print(layer1)
    print(layer2)
