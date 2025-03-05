"""
Explains Broker chain
cqs command query subsystem
"""

from abc import ABC
from enum import Enum
from typing import Any


class Event(list):

    def __call__(self, *args: Any, **kwds: Any) -> Any:
        for item in self:
            item(*args, **kwds)


class WhatToQuery(Enum):
    ATTACK = 1
    DEFENSE = 2
    HEALTH = 2


class Query:
    def __init__(self, creature_name, what_to_query, default_val) -> None:
        self.creature_name = creature_name
        self.value = default_val
        self.what_to_query = what_to_query


class Game:

    def __init__(self):
        self.queries = Event()

    def perform_query(self, sender, query):
        self.queries(sender, query)


class CreatureModifier(ABC):

    def __init__(self, game, creature) -> None:
        self.creature = creature
        self.game = game
        self.game.queries.append(self.handle)

    def handle(self, sender, query):
        pass

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.game.queries.remove(self.handle)


class DoubleAttackModifier(CreatureModifier):

    def handle(self, sender, query):
        if (
            sender.name == self.creature.name
            and query.what_to_query == WhatToQuery.ATTACK
        ):
            query.value *= 2


class Creature:
    def __init__(self, game, name, attack, defense, health=100) -> None:
        self.name = name
        self.game = game
        self.initial_attack = attack
        self.initial_defense = defense
        self.initial_health = health

    @property
    def attack(self):
        q = Query(self.name, WhatToQuery.ATTACK, self.initial_attack)
        self.game.perform_query(self, q)
        return q.value

    @property
    def defense(self):
        q = Query(self.name, WhatToQuery.DEFENSE, self.initial_defense)
        self.game.perform_query(self, q)
        return q.value

    @property
    def health(self):
        q = Query(self.name, WhatToQuery.HEALTH, self.initial_health)
        self.game.perform_query(self, q)
        return q.value

    def __str__(self) -> str:
        return f"{self.name} ({self.attack} / {self.defense} / {self.health})"


if __name__ == "__main__":
    game = Game()
    panda = Creature(game, "Kung Fu Panda", 60, 40)
    # print(panda)
    # dam = DoubleAttackModifier(game, panda)
    # print(panda)
    with DoubleAttackModifier(game, panda):
        print(panda)
    print(panda)
