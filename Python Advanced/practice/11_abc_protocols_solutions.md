# ABCs and Protocols Practice Solutions

## Solution 1 - Payment Gateway Contract
ABCs are useful when you want explicit inheritance and shared helper logic.

```python
from abc import ABC, abstractmethod


class PaymentGateway(ABC):
    @abstractmethod
    def authorize(self, order_id, amount):
        raise NotImplementedError

    @abstractmethod
    def capture(self, authorization_id):
        raise NotImplementedError

    def supports_partial_capture(self) -> bool:
        return False
```

## Solution 2 - Storage Provider Protocol
Protocols are ideal when test doubles should not need inheritance.

```python
from typing import Protocol


class StorageProvider(Protocol):
    def upload(self, path: str, content: bytes) -> str:
        ...

    def exists(self, path: str) -> bool:
        ...
```

## Solution 3 - Notification Channels
Define only the behavior the dispatcher needs.

```python
from typing import Protocol


class NotificationChannel(Protocol):
    def send(self, recipient: str, message: str) -> str:
        ...


def dispatch(channel: NotificationChannel, recipient: str, message: str) -> str:
    return channel.send(recipient, message)
```

## Solution 4 - Exporter Plugins with Runtime Validation
If you need runtime checks, combine registration with a runtime-checkable protocol.

```python
from typing import Protocol, runtime_checkable


@runtime_checkable
class Exporter(Protocol):
    def export(self, rows: list[dict]) -> bytes:
        ...


def register_exporter(name, exporter, registry):
    if not isinstance(exporter, Exporter):
        raise TypeError(f"{name} does not satisfy Exporter")
    registry[name] = exporter
```

## Solution 5 - Rule Engine Extensions
Protocols let the engine accept mixed rule implementations while keeping type hints useful.

```python
from typing import Protocol


class FraudRule(Protocol):
    severity: str

    def evaluate(self, payload: dict) -> bool:
        ...


def evaluate_rules(rules: list[FraudRule], payload: dict) -> list[str]:
    return [rule.severity for rule in rules if rule.evaluate(payload)]
```