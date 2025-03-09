"""
Good example of state design pattern
"""

from abc import ABC, abstractmethod


# State Interface
class ATMState(ABC):
    @abstractmethod
    def insert_card(self, atm):
        pass

    @abstractmethod
    def enter_pin(self, atm, pin):
        pass

    @abstractmethod
    def withdraw_money(self, atm, amount):
        pass

    @abstractmethod
    def eject_card(self, atm):
        pass


# Concrete States
class NoCard(ATMState):
    def insert_card(self, atm):
        print("Card inserted.")
        atm.state = HasCard()

    def enter_pin(self, atm, pin):
        print("Insert a card first.")

    def withdraw_money(self, atm, amount):
        print("Insert a card first.")

    def eject_card(self, atm):
        print("No card to eject.")


class HasCard(ATMState):
    def insert_card(self, atm):
        print("Card already inserted.")

    def enter_pin(self, atm, pin):
        if pin == atm.correct_pin:
            print("PIN correct.")
            atm.state = HasCorrectPIN()
        else:
            print("Incorrect PIN. Try again.")

    def withdraw_money(self, atm, amount):
        print("Enter PIN first.")

    def eject_card(self, atm):
        print("Card ejected.")
        atm.state = NoCard()


class HasCorrectPIN(ATMState):
    def insert_card(self, atm):
        print("Card already inserted.")

    def enter_pin(self, atm, pin):
        print("PIN already entered.")

    def withdraw_money(self, atm, amount):
        if atm.balance >= amount:
            print(f"Withdrawing ${amount}")
            atm.balance -= amount
            if atm.balance == 0:
                atm.state = OutOfMoney()
        else:
            print("Insufficient balance.")

    def eject_card(self, atm):
        print("Card ejected.")
        atm.state = NoCard()


class OutOfMoney(ATMState):
    def insert_card(self, atm):
        print("ATM is out of money.")

    def enter_pin(self, atm, pin):
        print("ATM is out of money.")

    def withdraw_money(self, atm, amount):
        print("ATM is out of money.")

    def eject_card(self, atm):
        print("No card to eject.")


# Context (ATM Machine)
class ATM:
    def __init__(self, balance):
        self.state = NoCard()  # Initial state
        self.correct_pin = 1234
        self.balance = balance

    def insert_card(self):
        self.state.insert_card(self)

    def enter_pin(self, pin):
        self.state.enter_pin(self, pin)

    def withdraw_money(self, amount):
        self.state.withdraw_money(self, amount)

    def eject_card(self):
        self.state.eject_card(self)


# Usage
atm = ATM(500)
atm.eject_card()
# atm.insert_card()
# atm.enter_pin(1234)
# atm.withdraw_money(200)
# atm.eject_card()
# atm.insert_card()
# atm.enter_pin(1234)
# atm.withdraw_money(400)  # Should show insufficient balance
# atm.eject_card()
