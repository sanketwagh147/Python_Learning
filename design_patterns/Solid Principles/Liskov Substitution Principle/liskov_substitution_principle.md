# Liskovs Substitution principle

#### Objects of a subclass should be replaceable with objects of the superclass without affecting the correctness of the program
- LSP ensures that a subclass behaves like its superclass
- The subclass should not remove any behavior expected from super class

### Key Rules of LSP
#### Method Signature Compatibility
A subclass must not change the method signatures of the superclass (e.g., changing parameter types or return types in an incompatible way).

Ex: violating signature compatibility
```python
class Animal:
    def make_sound(self):
        return "Some sound"

class Dog(Animal):
    def make_sound(self, volume):  # Added a new parameter
        return "Bark" * volume  # Violates LSP

```
ex: Correct signature compatibility
```python
class Animal:
    def make_sound(self):
        return "Some sound"

class Dog(Animal):
    def make_sound(self):
        return "Bark"

```

#### Preconditions Should Not Be Strengthened
The subclass should not impose stricter requirements on input values compared to the superclass.

Ex: violating preconditions rule
```python
class PaymentProcessor:
    def process_payment(self, amount):
        if amount <= 0:
            raise ValueError("Amount must be positive")
        print(f"Processing payment of ${amount}")

class CreditCardProcessor(PaymentProcessor):
    def process_payment(self, amount):
        if amount < 100:  # Stricter condition than the superclass
            raise ValueError("Minimum payment for credit cards is $100")  # Violates LSP
        super().process_payment(amount)


```
ex: Correct approach
```python
class PaymentProcessor:
    def process_payment(self, amount):
        if amount <= 0:
            raise ValueError("Amount must be positive")
        print(f"Processing payment of ${amount}")


class CreditCardProcessor(PaymentProcessor):
    # Instead of overriding method add new method specific to this class
    def process_credit_card_payment(self, amount):
        if amount < 100:
            raise ValueError("Minimum payment for credit cards is $100")  # Specific to credit cards
        self.process_payment(amount)

```
#### Postconditions Should Not Be Weakened
The subclass should not provide weaker guarantees than the superclass after execution.

#### Incorrect approach
- The subclass (PremiumAccount) weakens this guarantee by allowing overdrafts without an explicit error.
```python
class BankAccount:
    def __init__(self, balance):
        self.balance = balance

    def withdraw(self, amount):
        if amount > self.balance:
            raise ValueError("Insufficient funds")  # Guarantees that withdrawal never exceeds balance
        self.balance -= amount
        return self.balance  # Guarantees updated balance

class PremiumAccount(BankAccount):
    def withdraw(self, amount):
        # Allows overdraft without an error, weakening the postcondition
        self.balance -= amount
        return max(self.balance, 0)  # Violates LSP, as it allows negative balance silently

```

#### Correct approach : 
The new method (withdraw_with_overdraft()) explicitly allows overdrafts but does not weaken the original guarantee.
```python
class BankAccount:
    def __init__(self, balance):
        self.balance = balance

    def withdraw(self, amount):
        if amount > self.balance:
            raise ValueError("Insufficient funds")  # Ensures no overdraft
        self.balance -= amount
        return self.balance  # Ensures correct balance

class PremiumAccount(BankAccount):
    def withdraw_with_overdraft(self, amount, overdraft_limit):
        if amount > self.balance + overdraft_limit:
            raise ValueError("Overdraft limit exceeded")  # Maintains explicit guarantee
        self.balance -= amount
        return self.balance  # Still ensures correct balance tracking
```
#### No Unexpected Exceptions
A subclass should not introduce new exceptions that the superclass does not throw.

#### Incorrect approach
```python
class PaymentProcessor:
    def process_payment(self, amount):
        if amount <= 0:
            raise ValueError("Amount must be positive")  # Expected exception
        print(f"Processing payment of ${amount}")

class CryptoPaymentProcessor(PaymentProcessor):
    def process_payment(self, amount):
        if amount <= 0:
            raise ValueError("Amount must be positive")  # Expected exception
        
        if amount > 10000:
            raise ConnectionError("Blockchain network error!")  # Unexpected exception

        print(f"Processing crypto payment of ${amount}")
```

The subclass (CryptoPaymentProcessor) introduces a ConnectionError, which existing client code might not be prepared to handle.

#### Correct approach
```python
class CryptoPaymentProcessor(PaymentProcessor):
    def process_payment(self, amount):
        if amount <= 0:
            raise ValueError("Amount must be positive")  # Expected exception
        
        try:
            if amount > 10000:
                raise ConnectionError("Blockchain network error!")  # Internal error
        except ConnectionError:
            raise ValueError("Crypto transaction failed. Please retry.")  # Converts to an expected exception

        print(f"Processing crypto payment of ${amount}")


```
Instead convert the ConnectionError into a ValueError, which is already expected by client code.

This ensures that substituting CryptoPaymentProcessor for PaymentProcessor will not break existing functionality.

### Conclusion:
**No Unexpected Exceptions (Liskov Substitution Principle)***

To follow Liskov Substitution Principle (LSP), subclasses should not introduce new exceptions that the superclass does not throw.

**Consistency**: The subclass should behave just like the superclass, so existing code does not break.

**Predictable Errors**: If a superclass throws only ValueError, the subclass should not suddenly throw ConnectionError or other unexpected exceptions.

**Safer Code**: Keeping errors consistent makes the system easier to maintain and debug.

**Simply put: If a program works fine with the superclass, it should also work fine with the subclass without crashing due to unexpected errors**