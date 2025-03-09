"""
Informs when a property is changes
"""

from typing import Any


class Event(list):

    def __call__(self, *args: Any, **kwds: Any) -> Any:

        for item in self:
            item(*args, **kwds)


class PropertyObservable:
    def __init__(self) -> None:
        self.property_changed = Event()


class Person(PropertyObservable):

    def __init__(self, age=0) -> None:
        super().__init__()
        self._age = age

    @property
    def age(self):
        return self._age

    @property
    def can_vote(self):
        return self._age >= 18

    @age.setter
    def age(self, value):
        if self._age == value:
            return

        old_can_vote = self.can_vote
        self._age = value
        self.property_changed("age", value)

        if old_can_vote != self.can_vote:
            self.property_changed("can_vote", self.can_vote)


class TrafficAuthority:

    def __init__(self, person: Person) -> None:
        self.person = person
        person.property_changed.append(self.person_changed)

    def person_changed(self, name, value):

        if name == "age":
            if value < 16:
                print("You cannot drive")
            else:
                print("You can drive now")

                self.person.property_changed.remove(self.person_changed)


if __name__ == "__main__":

    def person_changed(name, value):
        if name == "can_vote":
            print(f"Voting ability changed : {value}")

    p = Person()
    # ta = TrafficAuthority(p)
    p.property_changed.append(person_changed)

    for age in range(12, 20):

        print(f"Setting age to {age}")
        p.age = age
