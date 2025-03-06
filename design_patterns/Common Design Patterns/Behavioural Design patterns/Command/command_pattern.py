"""
We can use bank account methods as is but there is no record 
With Command pattern we give and interface which also logs who did what and we can undo redo
"""

import unittest
from abc import ABC
from enum import Enum


class BankAccount:
    OVERDRAFT_LIMIT = -500

    def __init__(self, balance=0) -> None:
        self.balance = balance

    def deposit(self, amount):
        self.balance += amount
        print(f"Deposited {amount}", f"Balance = {self.balance}")

    def withdraw(self, amount):
        if self.balance - amount >= BankAccount.OVERDRAFT_LIMIT:
            self.balance -= amount
            print(f"Withdrew {amount}.  Balance :{self.balance}")
            return True
        return False

    def __str__(self) -> str:
        return f"Balance = {self.balance}"

    def __repr__(self) -> str:
        return f"Balance = {self.balance}"


class Command(ABC):
    def __init__(self) -> None:
        self.success = None

    def invoke(self):
        pass

    def undo(self):
        pass

    # def undo


class BankAccountCommand(Command):
    class Action(Enum):
        DEPOSIT = 0
        WITHDRAW = 1

    def __init__(self, account: BankAccount, action: Action, amount) -> None:
        super().__init__()
        self.account = account
        self.action = action
        self.amount = amount

    def invoke(self):
        if self.action == self.Action.DEPOSIT:
            self.account.deposit(self.amount)
            self.success = True
        elif self.account == self.Action.WITHDRAW:
            self.success = self.account.withdraw(self.amount)

    def undo(self):
        if not self.success:
            return
        if self.action == self.Action.DEPOSIT:
            self.account.withdraw(self.amount)
        elif self.action == self.Action.WITHDRAW:
            self.account.deposit(self.amount)


class CompositeBankAccountCommand(Command, list):
    def __init__(self, items=[]):
        super().__init__()
        for i in items:
            self.append(i)

    def invoke(self):
        for x in self:
            x.invoke()

    def undo(self):
        for x in reversed(self):
            x.undo()


# TODO: https://www.udemy.com/course/design-patterns-python/learn/lecture/13673798#overview
class MoneyTransferCommand:
    pass


class TestSuite(unittest.TestCase):

    def test_composite_deposit(self):
        ba = BankAccount()
        deposit1 = BankAccountCommand(ba, BankAccountCommand.Action.DEPOSIT, 100)
        deposit2 = BankAccountCommand(ba, BankAccountCommand.Action.DEPOSIT, 50)
        composite: list[BankAccountCommand] = CompositeBankAccountCommand(
            [deposit1, deposit2]
        )
        composite.invoke()
        print(ba)
        composite.undo()
        print(ba)

    def test_transfer_fail(self):
        ba1 = BankAccount(100)
        ba2 = BankAccount()

        amt = 100
        wd = BankAccountCommand(ba1, BankAccountCommand.Action.WITHDRAW, 100)
        dp = BankAccountCommand(ba2, BankAccountCommand.Action.DEPOSIT, 100)
        transfer = CompositeBankAccountCommand([wd, dp])
        transfer.invoke()
        print(f"{ba1=}, {ba2=}")
        transfer.undo()
        print(f"{ba1=}, {ba2=}")


if __name__ == "__main__":
    # ba = BankAccount()
    # cmd = BankAccountCommand(ba, BankAccountCommand.Action.DEPOSIT, 100)
    # cmd.invoke()
    # cmd.undo()
    # cmd.undo()
    # print(ba)

    unittest.main()
