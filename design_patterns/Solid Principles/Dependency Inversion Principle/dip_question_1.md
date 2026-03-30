# Dependency Inversion Principle — Question 1 (Easy)

## Problem: Notification Service Depends on Concrete Email

A `NotificationService` directly creates and uses an `EmailSender`. This tight coupling makes it impossible to switch to SMS or test without sending real emails.

### The Violating Code

```python
class NotificationService:
    def __init__(self):
        self.sender = EmailSender()  # ← Direct dependency on concrete class
    
    def notify(self, user, message):
        self.sender.send(user.email, message)

class EmailSender:
    def send(self, to, message):
        # Actually sends an email via SMTP
        print(f"Sending email to {to}: {message}")
```

### Requirements

Refactor to depend on abstraction:
```python
class MessageSender(ABC):
    @abstractmethod
    def send(self, recipient: str, message: str) -> None: ...

class EmailSender(MessageSender): ...
class SMSSender(MessageSender): ...
class SlackSender(MessageSender): ...

class NotificationService:
    def __init__(self, sender: MessageSender):  # ← Depends on abstraction
        self.sender = sender
```

### Expected Usage

```python
# Production
service = NotificationService(EmailSender(smtp_host="smtp.gmail.com"))
service.notify(user, "Your order shipped!")

# Testing — no real email sent
mock_sender = MockSender()
service = NotificationService(mock_sender)
service.notify(user, "Test message")
assert mock_sender.last_message == "Test message"

# Switch to SMS — NotificationService unchanged
service = NotificationService(SMSSender(api_key="..."))
```

### Constraints

- `NotificationService` NEVER imports or references concrete sender classes.
- Sender is injected via constructor (dependency injection).
- Write a `MockSender` for testing.
