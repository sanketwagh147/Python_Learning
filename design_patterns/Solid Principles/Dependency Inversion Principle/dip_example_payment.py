"""
Docstring for design_patterns.Solid Principles.Dependency Inversion Principle.dip_example_payment
"""

from abc import ABC, abstractmethod

## Violates DIP

class _PayPalPayment:
    
    def process_payment(self,amount):
        print(f"Processing amount {amount=} via PayPal")

class _OrderService:
    
    def __init__(self) -> None:
        self.payment_processor : _PayPalPayment = _PayPalPayment()

    def checkout(self,amount):
        self.payment_processor.process_payment(amount)
        print("Order places successfully")


class Payment(ABC):
    
    @abstractmethod
    def process_payment(self,amount):
        ...

class PayPalPayment(Payment):

    def process_payment(self,amount):
        print(f"Processing Payment for {amount=} via PayPal")
        print("Getting PayPal connection")
        print("payment via PayPal is successful")

class UPIPayment(Payment):

    def process_payment(self,amount):
        print(f"Processing Payment for {amount=} via UPI")
        print("Getting UPI connection")
        print("payment via UPI is successful")
    

class OrderService:
    
    def __init__(self,payment_processor:Payment) -> None: # This avoids tight coupling and follows DIP
        self.payment_processor = payment_processor

    def checkout(self,amount):
        self.payment_processor.process_payment(amount)
        print("Order places successfully")
    
    
if __name__ == "__main__" :

    payment_method = 'pay_pal'

    payment_methods = {"upi": UPIPayment, "pay_pal": PayPalPayment}

    pay_processor = payment_methods[payment_method]()

    order = OrderService(pay_processor)

    order.checkout(100)

