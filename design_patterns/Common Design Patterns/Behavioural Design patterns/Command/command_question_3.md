# Command Pattern — Question 3 (Hard)

## Problem: Task Queue with Priority, Scheduling, and Retry

Build a command-based task queue that supports priority ordering, delayed execution, and automatic retry on failure.

### Requirements

#### Command Interface
```python
class Task(ABC):
    name: str
    priority: int  # lower = higher priority
    max_retries: int
    
    @abstractmethod
    def execute(self) -> TaskResult: ...
    
    @abstractmethod
    def undo(self) -> None: ...
```

`TaskResult`: `success: bool`, `message: str`, `retry_after: float | None`

#### Concrete Tasks
- `SendEmailTask(to, subject, body)` — simulates email sending (randomly fails 30% of the time)
- `ProcessPaymentTask(order_id, amount)` — simulates payment (fails if amount > 10000)
- `GenerateReportTask(report_type, params)` — always succeeds but takes "time"
- `CleanupTask(resource_ids)` — cleanup resources, used as compensation in undo

#### TaskQueue
```python
class TaskQueue:
    def enqueue(self, task: Task, delay_seconds: float = 0): ...
    def process_next(self) -> TaskResult: ...
    def process_all(self) -> list[TaskResult]: ...
    def pending_count(self) -> int: ...
    def failed_tasks(self) -> list[Task]: ...
    def retry_failed(self) -> list[TaskResult]: ...
```

### Expected Usage

```python
queue = TaskQueue()

queue.enqueue(SendEmailTask("alice@test.com", "Welcome", "Hello!"), delay_seconds=5)
queue.enqueue(ProcessPaymentTask("ORD-001", 99.99), priority=1)  # high priority
queue.enqueue(GenerateReportTask("monthly", {"month": "Jan"}), priority=3)

results = queue.process_all()
# → ProcessPaymentTask (priority 1) runs first
# → SendEmailTask runs after 5s delay
# → GenerateReportTask runs last

# If email failed:
print(queue.failed_tasks())  # [SendEmailTask(...)]
queue.retry_failed()  # retries up to max_retries
```

### Constraints

- Priority queue (use `heapq` — lower priority number = runs first).
- Delayed tasks: track `ready_at` timestamp; skip if not ready during `process_next()`.
- Retry: failed tasks go to a dead-letter queue after `max_retries` exhausted.
- Each task's `undo()` can be used for compensation (e.g., refund a payment).
- `process_all()` processes in priority order, respecting delays.
- Thread-safe: the queue must work with concurrent producers and consumers.

### Think About

- How does this compare to Celery/RQ in Python?
- Where does the Command pattern end and the Queue/Scheduler pattern begin?
- Could you combine this with the Saga pattern for multi-step workflows?
