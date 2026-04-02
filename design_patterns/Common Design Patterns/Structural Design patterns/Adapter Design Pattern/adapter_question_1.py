"""Adapter pattern example for temperature sensors.

Why:
The application expects sensors that expose `get_temperature()` in Celsius,
but a third-party sensor exposes `get_temperature_f()` in Fahrenheit.

How:
`CelsiusAdapter` wraps `FahrenheitSensor`, converts Fahrenheit to Celsius using
`C = (F - 32) * 5/9`, and rounds to 1 decimal place.
"""

from abc import ABC, abstractmethod

from Marklutz_bookcode.timeseqs2B import F


class TemperatureSensor(ABC):
	"""Target interface used by the application."""

	@abstractmethod
	def get_temperature(self) -> float:
		"""Return the current temperature in Celsius."""


class FahrenheitSensor:
	"""Third-party class (adaptee). Cannot be modified."""

	def get_temperature_f(self) -> float:
		return 98.6  # simulated reading


class CelsiusSensor(TemperatureSensor):
	"""Native implementation that already matches the target interface."""

	def get_temperature(self) -> float:
		return 37.0  # simulated reading


class CelsiusAdapter(TemperatureSensor):
	"""Adapts `FahrenheitSensor` to the `TemperatureSensor` interface."""

	def __init__(self, adaptee: FahrenheitSensor) -> None:
		self.adaptee = adaptee

	def get_temperature(self) -> float:
		return round((self.adaptee.get_temperature_f() - 32) * (5 / 9), 1)


def get_average_temperature(sensors: list[TemperatureSensor]) -> float:
	"""Example function that uses the target interface."""
	total = sum(sensor.get_temperature() for sensor in sensors)
	return total / len(sensors)

if __name__ == "__main__":
 
	sensor_1 = FahrenheitSensor()
	sensor_2 = CelsiusSensor()

	# This way the method can work with both native Celsius sensors and adapted Fahrenheit sensors without any changes to the method itself.
	avg_temp = get_average_temperature([CelsiusAdapter(sensor_1), sensor_2])
	raw_sensor = FahrenheitSensor()
	adapted_sensor = CelsiusAdapter(raw_sensor)
	print(f"Adapter output (C): {adapted_sensor.get_temperature()}")

	celsius_sensor = CelsiusSensor()
	print(f"Native Celsius sensor output (C): {celsius_sensor.get_temperature()}")
	avg_temp = get_average_temperature([CelsiusAdapter(sensor_1), celsius_sensor])
	print(f"Average temperature (C): {avg_temp}")