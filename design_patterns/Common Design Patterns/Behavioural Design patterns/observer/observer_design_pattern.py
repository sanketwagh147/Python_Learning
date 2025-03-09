"""
Observer Design pattern
"""

from typing import Any


class Event(list):

    def __call__(self, *args: Any, **kwds: Any) -> Any:

        for item in self:
            item(*args, **kwds)


class Person:

    def __init__(self, name, address) -> None:
        self.name = name
        self.address = address
        self.falls_ill = Event()

    def catch_a_cold(self):
        self.falls_ill(self.name, self.address)


def call_doctor(name, address):
    print(f"Name {name} needs a doctor at address: {address}")


if __name__ == "__main__":
    p = Person("sanket", "kanda road")
    p.falls_ill.append(
        lambda name, address: print(f"Patient {name} is ill at {address}")
    )
    p.falls_ill.append(call_doctor)
    p.catch_a_cold()

    # p.falls_ill.remove(call_doctor)

    # p.catch_a_cold()
