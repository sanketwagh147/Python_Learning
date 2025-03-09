# Observer design pattern

The Observer Pattern is a behavioral design pattern where an object (subject) maintains a list of dependents (observers) and notifies them automatically of any state changes.

## Where the Observer Pattern is Useful

When multiple objects need to react to a state change in another object.  
When you want to achieve loose coupling between components.  
When changes in one object should trigger automatic updates in others.  
When implementing event-driven or real-time systems.  
When you need a scalable way to manage dynamic subscribers.  
When following the Publish-Subscribe model for notifications.  
When designing reactive and asynchronous applications  

## Real World Analogy

If you subscribe to a newspaper or magazine, you no longer need to go to the store to check if the next issue is available. Instead, the publisher sends new issues directly to your mailbox right after publication or even in advance.

The publisher maintains a list of subscribers and knows which magazines they’re interested in. Subscribers can leave the list at any time when they wish to stop the publisher sending new magazine issues to them.

## Key Features

Decouples subject and observers (loose coupling).  
Automatic updates when the subject's state changes.  
Supports event-driven programming (e.g., UI event handling, stock market updates).  
Follows the Publish-Subscribe model, making it scalable and maintainable.  
Common Use Cases:  
GUI frameworks (event listeners on buttons).  
Real-time systems (stock market tickers, live notifications).  
Logging frameworks (multiple log handlers).  
Messaging systems (publishers and subscribers).  
This pattern improves modularity, flexibility, and maintainability in software design  

## Python Example

```python
 from typing import List


# Subject (Publisher)
class NewsPublisher:
    def __init__(self) -> None:
        self.subscribers: List[Subscriber] = []
        self.latest_news = ""

    def subscribe(self, subscriber: "Subscriber") -> None:
        """Adds a new subscriber."""
        self.subscribers.append(subscriber)

    def unsubscribe(self, subscriber: "Subscriber") -> None:
        """Removes an existing subscriber."""
        self.subscribers.remove(subscriber)

    def notify_subscribers(self) -> None:
        """Notifies all subscribers about the latest news."""
        for subscriber in self.subscribers:
            subscriber.update(self.latest_news)

    def publish_news(self, news: str) -> None:
        """Publishes new news and notifies subscribers."""
        self.latest_news = news
        print(f"\n[News Publisher] Breaking News: {news}")
        self.notify_subscribers()


# Observer (Subscriber)
class Subscriber:
    def __init__(self, name: str) -> None:
        self.name = name

    def update(self, news: str) -> None:
        """Receives news updates from the publisher."""
        print(f"[{self.name}] Received News Update: {news}")


# Client Code
if __name__ == "__main__":
    # Create a news publisher
    publisher = NewsPublisher()

    # Create subscribers
    alice = Subscriber("Alice")
    bob = Subscriber("Bob")
    charlie = Subscriber("Charlie")

    # Subscribe to the news publisher
    publisher.subscribe(alice)
    publisher.subscribe(bob)
    publisher.subscribe(charlie)

    # Publish news
    publisher.publish_news("Python 3.13 Released!")
    publisher.publish_news("AI Achieves Human-Level Intelligence!")

    # Unsubscribe Bob and publish more news
    publisher.unsubscribe(bob)
    publisher.publish_news("SpaceX Launches First Mars Colony Mission!")
```
