# Bridge Pattern — Question 3 (Hard)

## Problem: Media Player with Codec × Platform Abstraction

A media player must support multiple codecs (MP3, FLAC, AAC, WAV) and multiple output platforms (Desktop, Mobile, Web). Each codec decodes differently, and each platform renders audio differently.

### Requirements

#### Implementation: Codec
```python
class AudioCodec(ABC):
    def decode(self, file_path: str) -> AudioData: ...
    def get_bitrate(self) -> int: ...
    def supports_streaming(self) -> bool: ...
```
Concrete: `MP3Codec`, `FLACCodec`, `AACCodec`

#### Implementation: Output
```python
class AudioOutput(ABC):
    def initialize(self, sample_rate: int, channels: int): ...
    def write_samples(self, samples: bytes): ...
    def flush(self): ...
```
Concrete: `DesktopOutput`, `MobileOutput`, `WebOutput`

#### Abstraction: Player
```python
class MediaPlayer(ABC):
    def __init__(self, codec: AudioCodec, output: AudioOutput): ...
    def play(self, file_path: str): ...
    def stop(self): ...
```
Concrete: `StandardPlayer` (simple playback), `StreamingPlayer` (buffers and streams in chunks)

**This is a TWO-DIMENSIONAL bridge** — the abstraction depends on TWO implementation interfaces.

### Expected Usage

```python
# Desktop + FLAC
player = StandardPlayer(FLACCodec(), DesktopOutput())
player.play("song.flac")
# → [FLAC] Decoding song.flac (lossless, 1411kbps)
# → [Desktop] Initializing: 44100Hz, 2ch
# → [Desktop] Playing 4,320,000 samples
# → [Desktop] Playback complete

# Web + AAC (streaming)
streamer = StreamingPlayer(AACCodec(), WebOutput(), buffer_size=8192)
streamer.play("podcast.aac")
# → [AAC] Decoding podcast.aac (lossy, 256kbps)
# → [Web] Initializing WebAudio: 44100Hz, 2ch
# → [Web] Streaming chunk 1/12...
# → [Web] Streaming chunk 2/12...
# → ...
```

### Constraints

- `AudioData` is a dataclass with `samples: bytes`, `sample_rate: int`, `channels: int`, `duration_seconds: float`.
- `StreamingPlayer` must split `AudioData.samples` into fixed-size chunks.
- Show that adding `OGGCodec` requires 1 new class. Adding `BluetoothOutput` requires 1 new class. Neither changes existing code.
- Demonstrate the **combinatorial explosion** avoided: 3 codecs × 3 outputs × 2 players = 18 classes without Bridge, vs 3 + 3 + 2 = 8 classes with Bridge.

### Think About

- Can a bridge have more than two dimensions? What are the trade-offs?
- How would you add an equalizer between the codec and the output? (Hint: Decorator on AudioOutput)
- Compare this to Strategy pattern — what's the difference?
