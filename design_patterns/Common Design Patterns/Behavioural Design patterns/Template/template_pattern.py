"""
Template pattern
"""

from abc import ABC, abstractmethod


class Beverage(ABC):
    """Template class defining the algorithm skeleton"""

    def prepare(self):
        self.boil_water()
        self.brew()
        self.pour_in_cup()
        self.add_condiments()

    def boil_water(self):
        print("Boiling water")

    def pour_in_cup(self):
        print("Pouring into cup")

    @abstractmethod
    def brew(self):
        pass

    @abstractmethod
    def add_condiments(self):
        pass


class Tea(Beverage):
    def brew(self):
        print("Steeping tea leaves")

    def add_condiments(self):
        print("Adding lemon")


class Coffee(Beverage):
    def brew(self):
        print("Brewing coffee grounds")

    def add_condiments(self):
        print("Adding sugar and milk")


# Usage
tea = Tea()
tea.prepare()
# Output:
# Boiling water
# Steeping tea leaves
# Pouring into cup
# Adding lemon

coffee = Coffee()
coffee.prepare()
# Output:
# Boiling water
# Brewing coffee grounds
# Pouring into cup
# Adding sugar and milk
