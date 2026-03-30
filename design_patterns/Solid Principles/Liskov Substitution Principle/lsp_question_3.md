# Liskov Substitution Principle — Question 3 (Hard)

## Problem: Detect and Fix LSP Violations in a Payment System

You're reviewing a payment processing system. Find ALL LSP violations, explain each, and fix them.

### The Code Under Review

```python
class PaymentProcessor(ABC):
    @abstractmethod
    def process(self, amount: float) -> PaymentResult: ...
    
    @abstractmethod
    def refund(self, transaction_id: str, amount: float) -> RefundResult: ...
    
    @abstractmethod
    def get_balance(self) -> float: ...

class CreditCardProcessor(PaymentProcessor):
    def process(self, amount):
        if amount <= 0:
            raise ValueError("Amount must be positive")
        # Process credit card...
        return PaymentResult(success=True, transaction_id="CC-001")
    
    def refund(self, transaction_id, amount):
        return RefundResult(success=True)
    
    def get_balance(self):
        return self.credit_limit - self.used_amount

class CryptoProcessor(PaymentProcessor):
    def process(self, amount):
        if amount <= 0:
            raise ValueError("Amount must be positive")
        if amount < 10:
            raise ValueError("Crypto minimum is $10")  # ← VIOLATION 1: Strengthened precondition
        return PaymentResult(success=True, transaction_id="BTC-001")
    
    def refund(self, transaction_id, amount):
        raise NotImplementedError("Crypto payments cannot be refunded")  # ← VIOLATION 2
    
    def get_balance(self):
        return self.wallet_balance

class GiftCardProcessor(PaymentProcessor):
    def process(self, amount):
        if amount <= 0:
            raise ValueError("Amount must be positive")
        if amount > self.card_balance:
            return PaymentResult(success=False, error="Insufficient balance")
        self.card_balance -= amount
        return PaymentResult(success=True, transaction_id="GC-001")
    
    def refund(self, transaction_id, amount):
        self.card_balance += amount
        return RefundResult(success=True)
    
    def get_balance(self):
        return None  # ← VIOLATION 3: Weakened postcondition (should return float, returns None)

class PromotionalProcessor(PaymentProcessor):
    """Free promotional credit — process always succeeds, but sets a flag."""
    def process(self, amount):
        self.was_promotional = True  # ← VIOLATION 4: Unexpected side effect
        return PaymentResult(success=True, transaction_id="PROMO-001", amount_charged=0)
    
    def refund(self, transaction_id, amount):
        return RefundResult(success=True, amount_refunded=0)
    
    def get_balance(self):
        return float("inf")  # ← VIOLATION 5: Unexpected return value
```

### Task

1. **Identify ALL 5 violations** and explain each:
   - Which LSP rule does each violate? (precondition, postcondition, invariant, history constraint)
   
2. **Refactor** the entire hierarchy:
   - Split `PaymentProcessor` into focused interfaces: `Processable`, `Refundable`, `BalanceCheckable`
   - `CryptoProcessor` does NOT implement `Refundable`
   - Use proper return types (no `None` for balance, no `NotImplementedError`)
   - Configure minimum amounts as constructor params, not hardcoded preconditions
   - Handle promotional payments as a decorator or separate concept

3. **Write tests** that verify LSP compliance:
   ```python
   def verify_lsp(processor: PaymentProcessor):
       """Any processor passing these tests is LSP-compliant."""
       # Can process positive amounts
       result = processor.process(50.0)
       assert isinstance(result, PaymentResult)
       
       # Returns float balance
       balance = processor.get_balance()
       assert isinstance(balance, float)
   ```

### Constraints

- Every class must be substitutable for its declared interfaces.
- No `NotImplementedError` in any method.
- No strengthened preconditions in subtypes.
- No weakened postconditions in subtypes.
- Code calling `PaymentProcessor` must work identically with ANY subtype.

### Think About

- LSP violations are often hidden behind "reasonable" design decisions. How do you catch them in code review?
- How does ISP (Interface Segregation) help prevent LSP violations?
- What is the relationship between LSP and Design by Contract (preconditions, postconditions, invariants)?
