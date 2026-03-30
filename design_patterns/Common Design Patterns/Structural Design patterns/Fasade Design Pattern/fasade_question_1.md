# Facade Pattern — Question 1 (Easy)

## Problem: Home Theater Facade

A home theater has many components (TV, sound system, streaming player, lights). Create a facade that simplifies "watch movie" into a single call.

### Requirements

- Subsystems (each with their own methods):
  - `TV`: `turn_on()`, `set_input(source)`, `turn_off()`
  - `SoundSystem`: `turn_on()`, `set_volume(level)`, `set_mode(mode)`, `turn_off()`
  - `StreamingPlayer`: `turn_on()`, `play(movie)`, `stop()`, `turn_off()`
  - `SmartLights`: `dim(level)`, `turn_on()`

- `HomeTheaterFacade`:
  - `watch_movie(movie_name)` — orchestrates turning everything on in the right order
  - `end_movie()` — shuts everything down

### Expected Usage

```python
facade = HomeTheaterFacade(TV(), SoundSystem(), StreamingPlayer(), SmartLights())
facade.watch_movie("Inception")
# → TV on, input set to HDMI1
# → Sound on, volume 40, mode surround
# → Lights dimmed to 20%
# → Playing "Inception"

facade.end_movie()
# → Player stopped, lights on, sound off, TV off
```

### Constraints

- The client only calls 2 methods. All complexity is hidden behind the facade.
- Subsystems remain usable independently.
