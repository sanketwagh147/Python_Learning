# Memento Pattern — Question 2 (Medium)

## Problem: Game Save System with Multiple Slots

A game allows saving progress to multiple named slots and restoring from any of them.

### Requirements

- `GameState` (memento): `level`, `health`, `inventory: list[str]`, `position: tuple`, `score`, `timestamp`
- `Game` (originator): play methods + `save_state()` / `load_state(memento)`
- `SaveManager` (caretaker): manages named save slots

### Expected Usage

```python
game = Game()
save_mgr = SaveManager()

game.play_level(1)  # level=1, health=100, score=500
save_mgr.save(game, slot="checkpoint_1")

game.play_level(2)  # level=2, health=75, score=1200
game.pick_up("sword")
save_mgr.save(game, slot="checkpoint_2")

game.play_level(3)  # level=3, health=20, score=1800
game.pick_up("shield")

# Oops, nearly dead — reload from checkpoint 2
save_mgr.load(game, slot="checkpoint_2")
print(game.health)     # → 75
print(game.inventory)  # → ["sword"]  (no shield — that was after checkpoint 2)
print(game.score)      # → 1200

# List all saves
save_mgr.list_saves()
# → checkpoint_1: Level 1, Score 500 (saved at 10:30:00)
# → checkpoint_2: Level 2, Score 1200 (saved at 10:31:00)
```

### Constraints

- Saving must deep-copy mutable state (inventory list).
- Loading from a slot that doesn't exist raises `SaveNotFoundError`.
- `SaveManager` can `delete(slot)` and `overwrite(slot)`.
- Limit: max 5 save slots. Trying to save a 6th raises `SaveSlotFullError`.

### Think About

- Why is deep copying critical for the inventory list?
- How does this differ from the Command pattern's undo? (Memento saves full state; Command saves incremental changes.)
