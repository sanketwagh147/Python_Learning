"""Bridge pattern example"""

from abc import ABC, abstractmethod


# Step 1: Define Implementation Interface
class Device(ABC):
    @abstractmethod
    def turn_on(self):
        pass

    @abstractmethod
    def turn_off(self):
        pass


# Step 2: Concrete Implementations
class TV(Device):
    def turn_on(self):
        print("TV is ON")

    def turn_off(self):
        print("TV is OFF")


class Radio(Device):
    def turn_on(self):
        print("Radio is ON")

    def turn_off(self):
        print("Radio is OFF")


# Step 3: Define Abstraction
class RemoteControl:
    def __init__(self, device: Device):
        self.device = device

    def power_on(self):
        self.device.turn_on()

    def power_off(self):
        self.device.turn_off()


# Step 4: Use Refined Abstraction
tv_remote = RemoteControl(TV())
tv_remote.power_on()  # Output: TV is ON
tv_remote.power_off()  # Output: TV is OFF

radio_remote = RemoteControl(Radio())
radio_remote.power_on()  # Output: Radio is ON
radio_remote.power_off()  # Output: Radio is OFF
