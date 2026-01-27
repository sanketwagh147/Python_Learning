"""
Docstring for design_patterns.Solid Principles.Single Responsibility Principle.srp_order_example
"""

from dataclasses import dataclass
from enum import Enum
from abc import ABC, abstractmethod


class Category(Enum):
    ZERO = 0.0
    FIVE = 5.0
    TWELVE = 12.0
    EIGHTEEN = 18.0
    TWENTY_EIGHT = 28.0

    @property
    def percent(self) -> float:
        return float(self.value)

    @property
    def tax_multiplier(self) -> float:
        return float(self.value // 100)


@dataclass
class Item:
    name: str
    price: float
    quantity: int
    category: Category
    item_tax: float = 0.0
    item_total: float = 0.0


class Order:

        
    def __init__(self, items: list[Item]) -> None:
        self.items = items
        self.total_amount = 0.0
        self.total_tax = 0.0

    def __str__(self) -> str:
        return "|".join([item.name for item in self.items])



class Calculator(ABC):

    def __init__(self) -> None:
        self.calculated_tax = 0.0
        self.calculated_total = 0.0

    @abstractmethod
    def calculate_total(self, order: Order):
        ...

    @abstractmethod
    def calculate_tax(self, order: Order):
        ...

class GroceryShopCalculator(Calculator):
    def calculate_total(self, order: Order):
        total = 0

        for item in order.items:
            item_total = item.price * item.quantity
            item.item_total = item_total
            total += item_total

        self.calculated_total = total
        return total

    def calculate_tax(self, order: Order):
        tax = 0
        for item in order.items:
            item_tax = item.category.tax_multiplier * item.item_total
            item.item_tax = item_tax
            tax += item_tax

            
        self.calculated_tax = tax

        return tax


class Payment(ABC):
    @abstractmethod
    def process_payment(self, amount): ...


class PayPalPayment(Payment):
    def process_payment(self, amount):
        print(f"Processing Payment for {amount=} via PayPal")
        print("Getting PayPal connection")
        print("payment via PayPal is successful")


class UPIPayment(Payment):
    def process_payment(self, amount):
        print(f"Processing Payment for {amount=} via UPI")
        print("Getting UPI connection")
        print("payment via UPI is successful")


class Sender(ABC):
    @abstractmethod
    def send(self, order: Order): ...


class InvoiceSender(Sender):
    def send(self, order: Order):
        print(f"Sending invoice for order {order} via {self.__class__.__name__}")


class Repository(ABC):
    @abstractmethod
    def save(self): ...
    
class OrderRepository:
    def save(self, order: Order):
        print(f"Saving order {order} to database")


# usage of SRP compliant OrderService & using DIP compliant dependencies
class OrderService:
    def __init__(
        self,
        order_calculator: Calculator,
        payment_processor: Payment,
        invoice_sender: Sender,
        order_repository: OrderRepository,
    ) -> None:
        self.order_calculator = order_calculator
        self.payment_processor = payment_processor
        self.invoice_sender = invoice_sender
        self.order_repository = order_repository

    def checkout(self, order: Order, payment_amount: float):
        total = self.order_calculator.calculate_total(order)
        tax = self.order_calculator.calculate_tax(order)

        print(f"Order Total : {total}, Tax : {tax}, Payable Amount : {self.order_calculator.calculated_total + self.order_calculator.calculated_tax}")

        self.payment_processor.process_payment(payment_amount)

        self.order_repository.save(order)

        self.invoice_sender.send(order)


if __name__ == "__main__":
    grocery_items = [
        Item(name="Imported Bananas", price=10, quantity=12, category=Category.EIGHTEEN),
        Item(name="Mangoes", price=200, quantity=6, category=Category.TWENTY_EIGHT),
    ]

    order = Order(grocery_items)

    order_calculator = GroceryShopCalculator()
    payment_processor = PayPalPayment()
    invoice_sender = InvoiceSender()
    order_repository = OrderRepository()

    order_service = OrderService(
        order_calculator,
        payment_processor,
        invoice_sender,
        order_repository,
    )

    order_service.checkout(order, payment_amount=236.0)