# Mediator Pattern — Question 1 (Easy)

## Problem: Chat Room

Users send messages through a chat room (mediator) rather than directly to each other.

### Requirements

- `ChatRoom` (mediator): `register(user)`, `send(message, sender, recipient=None)`
  - If recipient is None, broadcast to all except sender
  - If recipient specified, send only to that user
- `User`: `name`, `send(message, to=None)`, `receive(message, from_user)`

### Expected Usage

```python
room = ChatRoom()

alice = User("Alice", room)
bob = User("Bob", room)
carol = User("Carol", room)

alice.send("Hello everyone!")  # broadcast
# → [Bob] received from Alice: "Hello everyone!"
# → [Carol] received from Alice: "Hello everyone!"

bob.send("Hi Alice!", to="Alice")  # direct message
# → [Alice] received from Bob: "Hi Alice!"
```

### Constraints

- Users don't hold references to each other — they only know the mediator.
- Unknown recipient name → raise `ValueError`.
