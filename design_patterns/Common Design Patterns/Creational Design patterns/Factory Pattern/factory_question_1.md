# Factory Pattern — Question 1 (Easy)

## Problem: Notification Factory

Create a factory that produces different notification objects based on a type string.

### Requirements

- Define a base class `Notification` with an abstract `send(message: str)` method.
- Concrete classes: `EmailNotification`, `SMSNotification`, `PushNotification`.
- A `NotificationFactory.create(type: str) -> Notification` method returns the right instance.

### Expected Usage

```python
factory = NotificationFactory()

email = factory.create("email")
email.send("Your order shipped!")
# → [EMAIL] Your order shipped!

sms = factory.create("sms")
sms.send("OTP: 483920")
# → [SMS] OTP: 483920

push = factory.create("push")
push.send("New message from Alice")
# → [PUSH] New message from Alice

factory.create("fax")
# → ValueError: Unknown notification type: fax
```

### Constraints

- Use `ABC` and `@abstractmethod`.
- Raise `ValueError` for unknown types.
- The factory should NOT use a long `if/elif` chain — use a **dictionary mapping** instead.

### Hints

```python
class NotificationFactory:
    _registry = {
        "email": EmailNotification,
        "sms": SMSNotification,
        "push": PushNotification,
    }
```
