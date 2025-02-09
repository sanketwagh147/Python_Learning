# Interface Segregation Principle ( ISP )

## What it states

###  Clients should not be forced to depend on interfaces they do not use.
    This means that large, general-purpose interfaces should be broken down into smaller, more specific ones so that clients only need to implement the methods they actually use

## Example 1 (Violates ISP)

```python
from abc import ABC, abstractmethod

# ❌ Single Big Interface 
class Machine(ABC):
    @abstractmethod
    def print(self, document):
        pass

    @abstractmethod
    def scan(self, document):
        pass

    @abstractmethod
    def fax(self, document):
        pass

class AllInOnePrinter(Machine):
    def print(self, document):
        print(f"Printing: {document}")

    def scan(self, document):
        print(f"Scanning: {document}")

    def fax(self, document):
        print(f"Faxing: {document}")

class SimplePrinter(Machine):
    def print(self, document):
        print(f"Printing: {document}")

    def scan(self, document):
        raise NotImplementedError("SimplePrinter does not support scanning")

    def fax(self, document):
        raise NotImplementedError("SimplePrinter does not support faxing")

# Usage
printer = SimplePrinter()
printer.print("Hello World")
# printer.scan("Hello World")  # This would raise an error
```

### Problems:
**Unnecessary Methods:** SimplePrinter does not need scan and fax, but it must implement them.

**Violates ISP:** Clients are forced to depend on methods they don’t use.


## Example 1 (Fixes the violation)


```python

# ✅ Separate Smaller interfaces 
class Printer(ABC):
    @abstractmethod
    def print(self, document):
        pass

class Scanner(ABC):
    @abstractmethod
    def scan(self, document):
        pass

class FaxMachine(ABC):
    @abstractmethod
    def fax(self, document):
        pass

class AllInOnePrinter(Printer, Scanner, FaxMachine):
    def print(self, document):
        print(f"Printing: {document}")

    def scan(self, document):
        print(f"Scanning: {document}")

    def fax(self, document):
        print(f"Faxing: {document}")

class SimplePrinter(Printer):
    def print(self, document):
        print(f"Printing: {document}")

# Usage
printer = SimplePrinter()
printer.print("Hello World")

```
### Solution
- To follow ISP, we should split the Machine interface into smaller, more focused interfaces.


### Example 2 ( Violating ISP)
```python
from abc import ABC, abstractmethod

class Payment(ABC):
    @abstractmethod
    def pay(self, amount):
        pass

    @abstractmethod
    def refund(self, amount):
        pass

class CreditCardPayment(Payment):
    def pay(self, amount):
        print(f"Paid {amount} using Credit Card")

    def refund(self, amount):
        print(f"Refunded {amount} to Credit Card")

class BitcoinPayment(Payment):
    def pay(self, amount):
        print(f"Paid {amount} using Bitcoin")

    def refund(self, amount):
        raise NotImplementedError("Bitcoin does not support refunds")  # 🚨 Problem!

```
### Problems


### Example 2  ( Fixing the violation)
```python
class Payable(ABC):
    @abstractmethod
    def pay(self, amount):
        pass

class Refundable(ABC):
    @abstractmethod
    def refund(self, amount):
        pass

class CreditCardPayment(Payable, Refundable):
    def pay(self, amount):
        print(f"Paid {amount} using Credit Card")

    def refund(self, amount):
        print(f"Refunded {amount} to Credit Card")

class BitcoinPayment(Payable):
    def pay(self, amount):
        print(f"Paid {amount} using Bitcoin")

# Usage
cc_payment = CreditCardPayment()
cc_payment.pay(100)
cc_payment.refund(50)

btc_payment = BitcoinPayment()
btc_payment.pay(200)
# btc_payment.refund(100)  # ❌ This method doesn't exist anymore!

```

## Benefits of ISP
- ✅ No Unnecessary Methods: SimplePrinter only implements what it needs
- ✅ More Maintainable Code: Each class has a clear, well-defined responsibility.
- ✅ Flexible & Extensible: If a new type of machine is added, it can implement only the necessary interfaces.


## Conclusions
- ✅ Bad Design (Violates ISP): Large interfaces force classes to implement unused methods.
- ✅ Good Design (Follows ISP): Smaller, focused interfaces keep classes modular, maintainable, and extensible. 🚀

### links
[Python file](interface_segregation.py)