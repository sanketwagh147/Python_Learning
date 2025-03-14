import json
from abc import ABC, abstractmethod
from typing import Any


# Step 1: Define a Formatter Interface
class MessageFormatter(ABC):
    """Abstract base class for message formatters."""

    @abstractmethod
    def format(self, message: Any) -> str:
        pass


# Step 2: Implement Concrete Formatters
class StringFormatter(MessageFormatter):
    def format(self, message: str) -> str:
        return message


class NumberFormatter(MessageFormatter):
    def format(self, message: int) -> str:
        return str(message)


class JsonFormatter(MessageFormatter):
    def format(self, message: dict) -> str:
        return json.dumps(message, indent=2)


class ListFormatter(MessageFormatter):
    def format(self, message: list) -> str:
        return json.dumps(message, indent=2)


class DefaultFormatter(MessageFormatter):
    """Fallback for unsupported types."""

    def format(self, message: Any) -> str:
        return f"[Unsupported Type] {repr(message)}"


# Step 3: Create a Formatter Factory
class MessageFormatterFactory:
    """Factory that returns the appropriate formatter for a given message type."""

    _formatters = {
        str: StringFormatter(),
        int: NumberFormatter(),
        float: NumberFormatter(),
        dict: JsonFormatter(),
        list: ListFormatter(),
    }

    @staticmethod
    def get_formatter(message: Any) -> MessageFormatter:
        """Get the appropriate formatter based on message type."""
        return MessageFormatterFactory._formatters.get(
            type(message), DefaultFormatter()
        )

    @staticmethod
    def register_formatter(data_type: type, formatter: MessageFormatter):
        """Register a new formatter dynamically at runtime."""
        MessageFormatterFactory._formatters[data_type] = formatter


# Step 4: Define the Log Strategy Interface
class LogStrategy(ABC):
    @abstractmethod
    def log(self, message: Any):
        pass


# Step 5: Implement Concrete Loggers
class ConsoleLogger(LogStrategy):
    def log(self, message: Any):
        formatter = MessageFormatterFactory.get_formatter(message)
        print(f"[Console]: {formatter.format(message)}")


class FileLogger(LogStrategy):
    def log(self, message: Any):
        formatter = MessageFormatterFactory.get_formatter(message)
        print(
            f"[File]: Writing '{formatter.format(message)}' to file."
        )  # Simulating file write


class DatabaseLogger(LogStrategy):
    def log(self, message: Any):
        formatter = MessageFormatterFactory.get_formatter(message)
        print(f"[Database]: Storing '{formatter.format(message)}' in database.")


# Step 6: Demonstrate Usage
if __name__ == "__main__":
    logger = ConsoleLogger()

    # Logging different types of messages
    logger.log("Application started.")
    # Output: [Console]: Application started.

    logger.log(100)
    # Output: [Console]: 100

    logger.log({"user": "Sanket", "action": "login"})
    # Output:
    # [Console]: {
    #   "user": "Sanket",
    #   "action": "login"
    # }

    logger.log(["error1", "error2", "error3"])
    # Output:
    # [Console]: [
    #   "e
