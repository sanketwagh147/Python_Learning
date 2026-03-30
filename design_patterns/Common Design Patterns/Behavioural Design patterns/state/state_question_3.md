# State Pattern — Question 3 (Hard)

## Problem: TCP-like Connection State Machine

Build a TCP-style connection that implements the full state machine with proper event handling, timeouts, and error recovery.

### Requirements

#### States
```
CLOSED ──(connect)──→ SYN_SENT ──(ack_received)──→ ESTABLISHED
ESTABLISHED ──(close)──→ FIN_WAIT ──(ack_received)──→ CLOSED
ESTABLISHED ──(receive)──→ (data delivered, stays ESTABLISHED)
ESTABLISHED ──(timeout)──→ IDLE ──(ping)──→ ESTABLISHED
IDLE ──(timeout)──→ CLOSED
ANY ──(error)──→ ERROR ──(reset)──→ CLOSED
```

#### State Interface
```python
class ConnectionState(ABC):
    def connect(self, connection: Connection): ...
    def disconnect(self, connection: Connection): ...
    def send(self, connection: Connection, data: bytes): ...
    def receive(self, connection: Connection) -> bytes: ...
    def timeout(self, connection: Connection): ...
    def error(self, connection: Connection, error: Exception): ...
```

#### Connection Context
```python
class Connection:
    state: ConnectionState
    buffer: bytes
    max_retries: int
    retry_count: int
    last_activity: float
    
    def connect(self, host: str, port: int): ...
    def send(self, data: bytes): ...
    def receive(self) -> bytes: ...
    def close(self): ...
```

### Expected Usage

```python
conn = Connection()
print(conn.state_name)  # → "CLOSED"

conn.connect("localhost", 8080)
# → [SYN_SENT] Connecting to localhost:8080...
# → [SYN_SENT] SYN acknowledged
# → "ESTABLISHED"

conn.send(b"Hello")
# → [ESTABLISHED] Sending 5 bytes...
# → Data sent successfully

data = conn.receive()
# → [ESTABLISHED] Received 12 bytes

conn.close()
# → [FIN_WAIT] Closing connection...
# → [FIN_WAIT] FIN acknowledged
# → "CLOSED"

# Error handling
conn.connect("localhost", 8080)
conn.error(ConnectionError("Network failure"))
# → [ERROR] Connection error: Network failure
print(conn.state_name)  # → "ERROR"
conn.reset()
# → "CLOSED"

# Invalid operation
conn.send(b"data")  # while CLOSED
# → ConnectionError: Cannot send data in CLOSED state
```

### Constraints

- Every state handles ALL events — invalid events raise clear errors.
- State transitions must log: `f"[{old_state}] → [{new_state}]"`.
- Implement retry logic: if `send()` fails in ESTABLISHED, retry up to `max_retries` before transitioning to ERROR.
- `IDLE` state: if ESTABLISHED with no activity for 30s → transition to IDLE. If IDLE for 60s → auto-CLOSED.
- `Connection` tracks all state transitions in a `transition_history` list.
- Write at least 6 test cases: happy path, error recovery, timeout, invalid transitions, retry exhaustion, reset.

### Think About

- How does this compare to Python's `asyncio` state machine for connections?
- What if states need shared context (e.g., retry count)? Should state objects be stateless or stateful?
- Could you define this state machine declaratively (data-driven) instead of with classes?
