# Command Pattern — Question 2 (Medium)

## Problem: Smart Home Remote Control with Undo/Redo and Macros

Build a remote control that can execute, undo, redo commands, and run macro (multi-command) sequences.

### Requirements

- `Command(ABC)`: `execute()`, `undo()`
- Concrete commands:
  - `LightOnCommand(light)` / `LightOffCommand(light)`
  - `ThermostatSetCommand(thermostat, temperature)` — remembers old temp for undo
  - `MusicPlayCommand(player, song)` / `MusicStopCommand(player)`
- `MacroCommand(commands: list)`: executes all commands in order; undo reverses all in reverse order
- `RemoteControl`:
  - `execute(command)`, `undo()`, `redo()`
  - `history() -> list[str]` — returns command names in order

### Expected Usage

```python
remote = RemoteControl()

# Individual commands
remote.execute(LightOnCommand(living_room_light))
remote.execute(ThermostatSetCommand(thermostat, 22))
remote.execute(MusicPlayCommand(player, "Jazz Playlist"))

remote.undo()  # stops music
remote.undo()  # thermostat back to previous temp
remote.redo()  # thermostat forward to 22 again

# Macro: "Movie Mode"
movie_mode = MacroCommand([
    LightOffCommand(living_room_light),
    ThermostatSetCommand(thermostat, 20),
    MusicStopCommand(player),
])
remote.execute(movie_mode)
# → Light off, thermostat to 20, music stopped

remote.undo()  # undoes ALL three in reverse
```

### Constraints

- Redo stack clears when a new command is executed.
- `ThermostatSetCommand` must store the PREVIOUS temperature to enable undo.
- MacroCommand undoes in reverse order of execution.

### Think About

- How does the Command pattern enable "transaction-like" behavior?
- Where is the invoker, receiver, and command in this system?
