"""
State design pattern
"""

from abc import ABC


class State(ABC):

    def on(self, switch):
        print("Light is already ON")

    def off(self, switch):
        print("Light is already OFF")


class Switch:

    def __init__(self) -> None:
        self.state = OffState()

    def on(self):
        self.state.on(self)

    def off(self):
        self.state.off(self)


class OnState(State):
    def __init__(self) -> None:
        print("Light is Turned ON")

    def off(self, switch: Switch):
        print("We are turning the light OFF")
        switch.state = OffState()


class OffState(State):
    def __init__(self) -> None:
        print("Light is Turned OFF")

    def on(self, switch):
        print("We are turning the light OFF")
        switch.state = OnState()


if __name__ == "__main__":
    sw = Switch()
    sw.on()
    sw.off()
