from abc import ABC, abstractmethod
from datetime import time


class NotificationChannel(ABC):

    @abstractmethod
    def send(self, title: str, message: str) -> None:
        ...

class EmailChannel(NotificationChannel):
    def send(self, title: str, message: str) -> None:
        print(f"[EMAIL] {title} — {message}")

class SMSChannel(NotificationChannel):
    def send(self, title: str, message: str) -> None:
        print(f"[SMS] {title} — {message}")

class PushChannel(NotificationChannel):
    def send(self, title: str, message: str) -> None:
        print(f"[PUSH] {title} — {message}")

class Notification(ABC):

    def __init__(self, channel: NotificationChannel) -> None:
        self.channel = channel

    @abstractmethod
    def notify(self, title: str, message: str) -> None:
        ...
	
class NormalNotification(Notification):
    def __init__(self, channel: NotificationChannel) -> None:
        super().__init__(channel)

    def notify(self, title: str, message: str) -> None:
        self.channel.send(title, message)

class UrgentNotification(Notification):
    def __init__(self, channel: NotificationChannel) -> None:
        super().__init__(channel)

    def notify(self, title: str, message: str) -> None:
        self.channel.send(f"URGENT: {title}", message)

class ScheduledNotification(Notification):
    def __init__(self, channel: NotificationChannel, _time: time) -> None:
        super().__init__(channel)
        self.time: time = _time

    def notify(self, title: str, message: str) -> None:
        print(f"Scheduling message at {self.time}")
        self.channel.send(title, message)
        


if __name__ == "__main__": 

        email_channel = EmailChannel()
        sms_channel = SMSChannel()
        push_channel = PushChannel()

        urgent_email = UrgentNotification(email_channel)
        urgent_email.notify("Server Down", "Database unreachable")

        normal_sms = NormalNotification(sms_channel)
        normal_sms.notify("Reminder", "Meeting at 3pm")

        scheduled_push = ScheduledNotification(push_channel, time(6))
        scheduled_push.notify("Maintenance", "Deploy at 06:00")






	
	
	
