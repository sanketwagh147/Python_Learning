# Bridge Pattern — Question 1 (Easy)

## Problem: Notification System with Multiple Channels

Decouple the **notification type** (urgent, normal, info) from the **delivery channel** (email, SMS, push).

### Requirements

- **Channel interface** (implementation):
  ```python
  class NotificationChannel(ABC):
      def send(self, title: str, message: str): ...
  ```
  Concrete: `EmailChannel`, `SMSChannel`, `PushChannel`

- **Notification base** (abstraction):
  ```python
  class Notification:
      def __init__(self, channel: NotificationChannel): ...
      def notify(self, title: str, message: str): ...
  ```
  Concrete: `UrgentNotification` (adds "🚨 URGENT:" prefix), `NormalNotification`

### Expected Usage

```python
email = EmailChannel()
sms = SMSChannel()

urgent_email = UrgentNotification(email)
urgent_email.notify("Server Down", "Database unreachable")
# → [EMAIL] 🚨 URGENT: Server Down — Database unreachable

normal_sms = NormalNotification(sms)
normal_sms.notify("Reminder", "Meeting at 3pm")
# → [SMS] Reminder — Meeting at 3pm
```

### Constraints

- Adding a new channel (e.g., `SlackChannel`) requires NO changes to notification classes.
- Adding a new notification type (e.g., `ScheduledNotification`) requires NO changes to channel classes.
- This is the core benefit of Bridge — show that both dimensions extend independently.
