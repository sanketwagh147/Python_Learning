# Proxy Pattern — Question 1 (Easy)

## Problem: Lazy-Loading Image Proxy

An image viewer shows thumbnails. Full images are large and should only be loaded from disk when actually displayed.

### Requirements

- `Image(ABC)`: `display() -> None`, `info() -> str`
- `RealImage`: loads file in `__init__` (print "Loading image..."), displays it.
- `ImageProxy`: holds the filename. Does NOT load until `display()` is called. Subsequent calls reuse the loaded image.

### Expected Usage

```python
images = [ImageProxy("photo1.jpg"), ImageProxy("photo2.jpg"), ImageProxy("photo3.jpg")]

# No loading has happened yet!
print(images[0].info())     # → "Proxy for photo1.jpg (not loaded)"
images[0].display()          # → "Loading photo1.jpg... Displaying photo1.jpg"
images[0].display()          # → "Displaying photo1.jpg" (no reload!)
print(images[0].info())     # → "photo1.jpg (1920x1080, 2.4MB)"
```

### Constraints

- `ImageProxy` implements the same `Image` interface.
- Loading only happens ONCE, on first `display()` call.
- The rest of the app treats `ImageProxy` the same as `RealImage`.
