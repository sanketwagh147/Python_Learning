from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from attr import dataclass


@dataclass
class BaseMessage(ABC):
    """Abstract base for all message types."""

    pass


@dataclass
class TextMessage(BaseMessage):
    text: str


@dataclass
class EmailMessage(BaseMessage):
    subject: str
    body: str


@dataclass
class PushMessage(BaseMessage):
    title: str
    content: str


M = TypeVar("M", bound=BaseMessage)


class Notification(ABC, Generic[M]):
    @abstractmethod
    def send(self, message: M) -> None:
        pass


class TextNotification(Notification[TextMessage]):
    def send(self, message: TextMessage) -> None:
        print(f"Sending text message: {message.text}")


class EmailNotification(Notification[EmailMessage]):
    def send(self, message: EmailMessage) -> None:
        print(f"Sending email with subject: {message.subject} and body: {message.body}")


class PushNotification(Notification[PushMessage]):
    def send(self, message: PushMessage) -> None:
        print(
            f"Sending push notification with title: {message.title} and content: {message.content}"
        )
