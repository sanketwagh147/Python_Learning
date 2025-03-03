"""
This demostartes method chain 

"""


class Creature:
    def __init__(self, name, attack, defense, health) -> None:
        self.name = name
        self.attack = attack
        self.defense = defense
        self.health = health

    def __str__(self) -> str:
        return f"<Creature {self.name} {self.health=} ({self.attack}/{self.defense})>"


class CreatureModifier:

    def __init__(self, creature) -> None:
        self.creature = creature
        self.next_modifier = None

    def add_modifier(self, modifier):
        # if already has a modifier
        if self.next_modifier:
            # add to the next modifier
            self.next_modifier.add_modifier(modifier)
        else:
            self.next_modifier = modifier

    def handle(self) -> None:
        """subclasses need to handle this"""

        if self.next_modifier:
            self.next_modifier.handle()


class DisableModifier(CreatureModifier):
    """Using this all powers will be disabled"""

    def handle(self) -> None:
        print("Disable")


class EnableModifier(CreatureModifier):
    """Using this all powers will be disabled"""

    def handle(self) -> None:
        return super().handle()


class DoubleAttackModifier(CreatureModifier):

    def handle(self):
        print(f"We are doubling {self.creature.name}'s attack")
        self.creature.attack *= 2

        return super().handle()


class IncreaseDefense(CreatureModifier):

    def handle(self):
        if self.creature.health <= 30:
            print(f"We are doubling {self.creature.name}'s defense")
            self.creature.defense *= 2

        return super().handle()


class Damage(CreatureModifier):

    def __init__(self, creature, damage) -> None:
        super().__init__(creature)
        self.damage = damage

    def handle(self):
        if self.creature.health > 0:
            print(f"We are adding damage {self.creature.name}'s ")
            self.creature.health -= self.damage

        return super().handle()


if __name__ == "__main__":
    panda = Creature("Panda", 100, 100, 100)

    # print(panda)
    root = CreatureModifier(panda)

    root.add_modifier(DoubleAttackModifier(panda))
    root.add_modifier(Damage(panda, 30))
    # print(panda)
    root.add_modifier(IncreaseDefense(panda))
    # print(panda)
    root.add_modifier(Damage(panda, 30))
    root.add_modifier(Damage(panda, 30))
    root.add_modifier(DisableModifier(panda))
    root.add_modifier(IncreaseDefense(panda))
    root.add_modifier(IncreaseDefense(panda))
    root.add_modifier(IncreaseDefense(panda))
    print(panda)
    root.add_modifier(EnableModifier(panda))
    root.add_modifier(DoubleAttackModifier(panda))
    root.add_modifier(DoubleAttackModifier(panda))
    root.add_modifier(DoubleAttackModifier(panda))
    print(panda)

    root.handle()

    print(panda)
