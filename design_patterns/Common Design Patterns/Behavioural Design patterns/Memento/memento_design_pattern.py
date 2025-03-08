"""
Memento Pattern snapshot
"""


class Memento:
    def __init__(self, balance) -> None:
        self.balance = balance


class BankAccount:

    def __init__(self, balance=0) -> None:
        self.balance = balance
        self.changes = [Memento(self.balance)]
        self.current = 0

    def deposit(self, amount):
        self.balance += amount
        memento = Memento(self.balance)
        self.changes.append(memento)
        self.current += 1
        return memento

    def restore(self, memento):
        if memento:
            self.balance = memento.balance
            self.changes.append(memento)
            self.current = len(self.changes) - 1

    def undo(self):
        if self.current > 0:
            self.current -= 1
            memento = self.changes[self.current]
            self.balance = memento.balance
            return memento
        return None

    def redo(self):
        if self.current + 1 < len(self.changes):
            self.current += 1
            memento = self.changes[self.current]
            self.balance = memento.balance
            return memento
        return None

    def __str__(self) -> str:
        return f"Balance {self.balance}"


if __name__ == "__main__":
    ba = BankAccount(100)
    t1 = ba.deposit(100)
    t2 = ba.deposit(1000)
    print(ba)
    ba.undo()
    print(ba)
    ba.undo()
    print(ba)
    ba.redo()
    print(ba)
