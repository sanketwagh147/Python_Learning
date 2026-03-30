# Flyweight Pattern — Question 2 (Medium)

## Problem: Game Map Tile System

A 2D game renders a 1000×1000 tile map. Each tile has a type (grass, water, mountain, etc.) with shared texture/properties (intrinsic) but unique position (extrinsic).

### Requirements

#### Flyweight (Shared)
```python
class TileType:
    """Intrinsic state — shared across all tiles of same type."""
    name: str
    texture_path: str
    walkable: bool
    movement_cost: float
```

#### Context (Unique per tile)
```python
class Tile:
    """Extrinsic state — unique per position."""
    x: int
    y: int
    tile_type: TileType  # flyweight reference
```

#### Factory
```python
class TileTypeFactory:
    def get_type(self, name: str) -> TileType: ...
    def registered_count(self) -> int: ...
```

### Expected Usage

```python
factory = TileTypeFactory()
factory.register("grass", texture="grass.png", walkable=True, cost=1.0)
factory.register("water", texture="water.png", walkable=False, cost=999)
factory.register("mountain", texture="mountain.png", walkable=True, cost=3.0)

# Build 1,000,000 tiles but only 3 TileType objects
game_map = []
for x in range(1000):
    for y in range(1000):
        if (x + y) % 3 == 0:
            game_map.append(Tile(x, y, factory.get_type("grass")))
        elif (x + y) % 3 == 1:
            game_map.append(Tile(x, y, factory.get_type("water")))
        else:
            game_map.append(Tile(x, y, factory.get_type("mountain")))

print(f"Tiles: {len(game_map)}")           # 1,000,000
print(f"Unique types: {factory.registered_count()}")  # 3
```

### Constraints

- Calculate and print actual memory usage comparison (with vs without flyweight).
- Use `sys.getsizeof()` to demonstrate savings.
- `TileType` should be frozen (immutable).

### Think About

- What's the trade-off? (Saves memory but adds lookup overhead.)
- When would the flyweight factory need thread-safety?
