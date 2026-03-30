# Decorator Pattern — Question 3 (Hard)

## Problem: Data Stream Processing with Function Decorators + Class Decorators

Build a data stream processor that supports BOTH class-based decorators and Python function decorators (`@decorator` syntax) for transforming data.

### Requirements

#### Part A: Class-Based Decorators (Structural Pattern)

```python
class DataStream(ABC):
    def read(self) -> str: ...

class FileStream(DataStream):
    """Reads raw data from a simulated file."""

class EncryptionDecorator(DataStream):
    """Encrypts/decrypts data using a simple cipher."""

class CompressionDecorator(DataStream):
    """Compresses data (simulate with zlib or simple encoding)."""

class Base64Decorator(DataStream):
    """Encodes data to base64."""
```

Stacking: `FileStream → Compression → Encryption → Base64`

#### Part B: Python `@decorator` Functions

Implement the same pipeline using Python's `@` decorator syntax on a `process()` function:

```python
@base64_encode
@encrypt(key="secret")
@compress
def process(data: str) -> str:
    return data
```

#### Part C: Comparison

Write both versions processing the same input, show they produce equivalent output, and explain:
- When would you use the class-based approach?
- When would you prefer the `@decorator` approach?

### Expected Usage

```python
# Class-based
stream = FileStream("Hello, World! This is sensitive data.")
stream = CompressionDecorator(stream)
stream = EncryptionDecorator(stream, key="secret")
stream = Base64Decorator(stream)
result1 = stream.read()

# Function-based
result2 = process("Hello, World! This is sensitive data.")

print(result1 == result2)  # True (same transformation pipeline)
```

### Constraints

- Encryption: use a simple Caesar cipher (shift by key length).
- Compression: use `zlib.compress` / `zlib.decompress`.
- Base64: use `base64.b64encode`.
- Must also implement `write()` / reverse pipeline for decoding.
- The function decorators must preserve the original function's `__name__` and `__doc__` (use `functools.wraps`).

### Think About

- Class decorators maintain state (e.g., compression dictionary). Function decorators are stateless. When does this matter?
- How would you make the class-based pipeline support both `read()` (decode) and `write()` (encode)?
- Could you combine both approaches — class decorator that also works as a function decorator?
