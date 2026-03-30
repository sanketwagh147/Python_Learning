# Interface Segregation Principle — Question 2 (Medium)

## Problem: Worker System — Humans and Robots

A `Worker` interface requires eat, sleep, and work. Robots don't eat or sleep.

### The Violating Code

```python
class Worker(ABC):
    @abstractmethod
    def work(self): ...
    @abstractmethod
    def eat(self, food): ...
    @abstractmethod
    def sleep(self, hours): ...
    @abstractmethod
    def get_paid(self, amount): ...

class HumanWorker(Worker):
    def work(self): return "Working on tasks"
    def eat(self, food): return f"Eating {food}"
    def sleep(self, hours): return f"Sleeping {hours}h"
    def get_paid(self, amount): self.balance += amount

class RobotWorker(Worker):
    def work(self): return "Processing tasks"
    def eat(self, food): pass        # meaningless
    def sleep(self, hours): pass      # meaningless
    def get_paid(self, amount): pass  # robots don't get paid
```

### Requirements

Split into role-based interfaces:
```python
class Workable(ABC):
    @abstractmethod
    def work(self) -> str: ...

class Feedable(ABC):
    @abstractmethod
    def eat(self, food: str) -> str: ...

class Sleepable(ABC):
    @abstractmethod
    def sleep(self, hours: int) -> str: ...

class Payable(ABC):
    @abstractmethod
    def get_paid(self, amount: float) -> None: ...
```

#### Concrete
- `HumanWorker(Workable, Feedable, Sleepable, Payable)`
- `RobotWorker(Workable)` — only works!
- `InternWorker(Workable, Feedable, Sleepable)` — works, eats, sleeps, but unpaid
- `ContractWorker(Workable, Payable)` — works and gets paid, manages own food/sleep

### Expected Usage

```python
def assign_task(worker: Workable):
    print(worker.work())  # Works for humans, robots, interns, contractors

def lunch_break(worker: Feedable):
    print(worker.eat("Pizza"))  # Only humans and interns

def payroll(workers: list[Payable]):
    for w in workers:
        w.get_paid(5000)  # Only humans and contractors

workers: list[Workable] = [HumanWorker("Alice"), RobotWorker("Unit-7"), InternWorker("Bob")]
for w in workers:
    assign_task(w)  # All can work
```

### Constraints

- No empty method bodies or `pass` implementations.
- Functions accept the narrowest interface they need.
- Adding a new worker type (e.g., `VolunteerWorker`) doesn't force irrelevant method implementations.

### Think About

- How do you decide where to draw the line when splitting interfaces? Too many tiny interfaces can be as bad as one fat one.
- How does Python's duck typing relate to ISP? (Python doesn't enforce interfaces at compile time.)
- How do protocols (`typing.Protocol`) implement ISP in Python?
