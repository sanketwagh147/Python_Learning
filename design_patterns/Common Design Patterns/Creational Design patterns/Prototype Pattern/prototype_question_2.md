# Prototype Pattern — Question 2 (Medium)

## Problem: Game Character Preset System

A game has predefined character archetypes. Players pick an archetype and then customize stats/equipment.

### Requirements

- `Character` class with:
  - `name: str`, `health: int`, `attack: int`, `defense: int`
  - `skills: list[str]`
  - `equipment: dict[str, str]` (slot → item name)

- `CharacterRegistry` that stores named prototypes and clones them on demand:
  ```python
  registry.register("warrior", warrior_prototype)
  registry.register("mage", mage_prototype)
  clone = registry.create("warrior")
  ```

- Pre-register these archetypes:
  - **Warrior**: health=120, attack=15, defense=10, skills=["Slash", "Shield Bash"], equipment={"weapon": "Iron Sword", "armor": "Chainmail"}
  - **Mage**: health=80, attack=25, defense=5, skills=["Fireball", "Heal"], equipment={"weapon": "Staff", "armor": "Robe"}
  - **Rogue**: health=100, attack=20, defense=7, skills=["Backstab", "Stealth"], equipment={"weapon": "Dagger", "armor": "Leather"}

### Expected Usage

```python
registry = CharacterRegistry()
# ... register archetypes ...

p1 = registry.create("warrior")
p1.name = "Aragorn"
p1.skills.append("War Cry")

p2 = registry.create("warrior")
p2.name = "Brienne"

print(p1.skills)  # ["Slash", "Shield Bash", "War Cry"]
print(p2.skills)  # ["Slash", "Shield Bash"]  ← not affected
```

### Constraints

- `CharacterRegistry` should raise `KeyError` if archetype doesn't exist.
- Cloning must be **deep** — modifying a clone's skills/equipment must not affect the prototype.

### Think About

- Why is cloning better here than creating a `CharacterFactory` with `if/elif`?
- What if a `Character` contains a reference to a `Guild` object — should that be deep-copied too?
