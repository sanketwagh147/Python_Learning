"""
Implements code for the Interface Segregation Principle.

Interface Segregation Principle (ISP):
    "Clients should not be forced to depend on interfaces they do not use."

    Instead of one large interface, create smaller, focused interfaces so that
    implementing classes only need to know about the methods that are relevant to them.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum


# ============================================================================
# EXAMPLE 1 — Restaurant Workers
# ============================================================================
# A restaurant has different types of workers: chefs, waiters, and managers.
# Not every worker does every job. A waiter doesn't cook, a chef doesn't
# serve tables. If we force all workers to implement every task, we violate ISP.


# ---- BAD: One fat interface forces irrelevant methods on workers ----

class _RestaurantWorker(ABC):
    """Fat interface — every worker is forced to implement ALL methods."""

    @abstractmethod
    def cook_food(self, dish: str) -> str:
        pass

    @abstractmethod
    def serve_table(self, table_number: int) -> str:
        pass

    @abstractmethod
    def manage_inventory(self, item: str, quantity: int) -> str:
        pass

    @abstractmethod
    def handle_billing(self, table_number: int) -> str:
        pass


class _Chef(_RestaurantWorker):
    def cook_food(self, dish: str) -> str:
        return f"Chef is cooking {dish}"

    # Waiter's job — chef should NOT be forced to implement this
    def serve_table(self, table_number: int) -> str:
        raise NotImplementedError("Chef does not serve tables!")

    def manage_inventory(self, item: str, quantity: int) -> str:
        return f"Chef checked {quantity} units of {item}"

    # Manager's job
    def handle_billing(self, table_number: int) -> str:
        raise NotImplementedError("Chef does not handle billing!")


class _Waiter(_RestaurantWorker):
    # Chef's job
    def cook_food(self, dish: str) -> str:
        raise NotImplementedError("Waiter does not cook!")

    def serve_table(self, table_number: int) -> str:
        return f"Waiter is serving table {table_number}"

    # Manager's job
    def manage_inventory(self, item: str, quantity: int) -> str:
        raise NotImplementedError("Waiter does not manage inventory!")

    def handle_billing(self, table_number: int) -> str:
        return f"Waiter handling bill for table {table_number}"


# ---- GOOD: Segregated interfaces — each role only implements what it needs ----

class Cookable(ABC):
    @abstractmethod
    def cook_food(self, dish: str) -> str:
        pass


class Servable(ABC):
    @abstractmethod
    def serve_table(self, table_number: int) -> str:
        pass


class InventoryManageable(ABC):
    @abstractmethod
    def manage_inventory(self, item: str, quantity: int) -> str:
        pass


class Billable(ABC):
    @abstractmethod
    def handle_billing(self, table_number: int) -> str:
        pass


class Chef(Cookable, InventoryManageable):
    """Chef only cooks and manages kitchen inventory — nothing else."""

    def cook_food(self, dish: str) -> str:
        return f"Chef is cooking {dish}"

    def manage_inventory(self, item: str, quantity: int) -> str:
        return f"Chef checked {quantity} units of {item}"


class Waiter(Servable, Billable):
    """Waiter serves tables and handles bills — no cooking or inventory."""

    def serve_table(self, table_number: int) -> str:
        return f"Waiter is serving table {table_number}"

    def handle_billing(self, table_number: int) -> str:
        return f"Waiter handling bill for table {table_number}"


class Manager(InventoryManageable, Billable):
    """Manager handles inventory and billing — doesn't cook or serve."""

    def manage_inventory(self, item: str, quantity: int) -> str:
        return f"Manager updated {item}: {quantity} units"

    def handle_billing(self, table_number: int) -> str:
        return f"Manager reviewing bill for table {table_number}"


class HeadChef(Cookable, InventoryManageable, Billable):
    """A head chef who also manages inventory and approves bills."""

    def cook_food(self, dish: str) -> str:
        return f"Head Chef is cooking {dish}"

    def manage_inventory(self, item: str, quantity: int) -> str:
        return f"Head Chef verified {quantity} units of {item}"

    def handle_billing(self, table_number: int) -> str:
        return f"Head Chef approved bill for table {table_number}"


# ============================================================================
# EXAMPLE 2 — Document Processing (Printer / Scanner / Fax)
# ============================================================================
# Classic ISP example — a simple home printer shouldn't be forced to implement
# fax or scan capabilities it doesn't have.


# ---- BAD: One bloated machine interface ----

class _Machine(ABC):
    @abstractmethod
    def print_doc(self, document: str) -> str:
        pass

    @abstractmethod
    def scan_doc(self, document: str) -> str:
        pass

    @abstractmethod
    def fax_doc(self, document: str, number: str) -> str:
        pass


class _BasicPrinter(_Machine):
    def print_doc(self, document: str) -> str:
        return f"Printing: {document}"

    # Forced to stub out capabilities this printer doesn't have
    def scan_doc(self, document: str) -> str:
        raise NotImplementedError("This printer cannot scan!")

    def fax_doc(self, document: str, number: str) -> str:
        raise NotImplementedError("This printer cannot fax!")


# ---- GOOD: Small, focused interfaces ----

class Printable(ABC):
    @abstractmethod
    def print_doc(self, document: str) -> str:
        pass


class Scannable(ABC):
    @abstractmethod
    def scan_doc(self, document: str) -> str:
        pass


class Faxable(ABC):
    @abstractmethod
    def fax_doc(self, document: str, number: str) -> str:
        pass


class BasicPrinter(Printable):
    """Only prints — no scan, no fax. Clean and honest."""

    def print_doc(self, document: str) -> str:
        return f"Printing: {document}"


class OfficePrinter(Printable, Scannable):
    """Office printer that can print and scan, but no fax."""

    def print_doc(self, document: str) -> str:
        return f"[Office] Printing: {document}"

    def scan_doc(self, document: str) -> str:
        return f"[Office] Scanning: {document}"


class AllInOnePrinter(Printable, Scannable, Faxable):
    """Enterprise machine — prints, scans, and faxes."""

    def print_doc(self, document: str) -> str:
        return f"[All-in-One] Printing: {document}"

    def scan_doc(self, document: str) -> str:
        return f"[All-in-One] Scanning: {document}"

    def fax_doc(self, document: str, number: str) -> str:
        return f"[All-in-One] Faxing '{document}' to {number}"


# ============================================================================
# EXAMPLE 3 — Payment Methods (E-commerce)
# ============================================================================
# Different payment methods have different capabilities. Credit cards support
# refunds, Bitcoin doesn't. Wallets support balance checks, bank transfers
# don't support instant confirmation. Don't lump everything together.


class PaymentStatus(Enum):
    SUCCESS = "success"
    FAILED = "failed"
    PENDING = "pending"


@dataclass
class PaymentResult:
    status: PaymentStatus
    transaction_id: str
    message: str


# ---- BAD: Fat payment interface ----

class _PaymentProcessor(ABC):
    @abstractmethod
    def pay(self, amount: float) -> PaymentResult:
        pass

    @abstractmethod
    def refund(self, transaction_id: str) -> PaymentResult:
        pass

    @abstractmethod
    def check_balance(self) -> float:
        pass

    @abstractmethod
    def get_statement(self, month: int, year: int) -> str:
        pass


class _BitcoinPayment(_PaymentProcessor):
    def pay(self, amount: float) -> PaymentResult:
        return PaymentResult(PaymentStatus.SUCCESS, "BTC-001", f"Paid {amount} BTC")

    def refund(self, transaction_id: str) -> PaymentResult:
        raise NotImplementedError("Bitcoin transactions are irreversible!")

    def check_balance(self) -> float:
        return 1.5

    def get_statement(self, month: int, year: int) -> str:
        raise NotImplementedError("Bitcoin doesn't provide monthly statements!")


# ---- GOOD: Segregated payment interfaces ----

class Payable(ABC):
    @abstractmethod
    def pay(self, amount: float) -> PaymentResult:
        pass


class Refundable(ABC):
    @abstractmethod
    def refund(self, transaction_id: str) -> PaymentResult:
        pass


class BalanceCheckable(ABC):
    @abstractmethod
    def check_balance(self) -> float:
        pass


class StatementProvider(ABC):
    @abstractmethod
    def get_statement(self, month: int, year: int) -> str:
        pass


class CreditCardPayment(Payable, Refundable, StatementProvider):
    """Credit cards can pay, refund, and provide statements."""

    def pay(self, amount: float) -> PaymentResult:
        return PaymentResult(PaymentStatus.SUCCESS, "CC-001", f"Charged ${amount}")

    def refund(self, transaction_id: str) -> PaymentResult:
        return PaymentResult(PaymentStatus.SUCCESS, transaction_id, "Refund issued")

    def get_statement(self, month: int, year: int) -> str:
        return f"Credit card statement for {month}/{year}"


class BitcoinPayment(Payable, BalanceCheckable):
    """Bitcoin can pay and check balance — no refunds, no statements."""

    def pay(self, amount: float) -> PaymentResult:
        return PaymentResult(PaymentStatus.SUCCESS, "BTC-001", f"Paid {amount} BTC")

    def check_balance(self) -> float:
        return 1.5


class WalletPayment(Payable, Refundable, BalanceCheckable):
    """Digital wallet — pay, refund, and check balance. No formal statements."""

    def __init__(self, balance: float = 100.0):
        self._balance = balance

    def pay(self, amount: float) -> PaymentResult:
        if amount > self._balance:
            return PaymentResult(PaymentStatus.FAILED, "", "Insufficient balance")
        self._balance -= amount
        return PaymentResult(PaymentStatus.SUCCESS, "WLT-001", f"Paid ${amount}")

    def refund(self, transaction_id: str) -> PaymentResult:
        return PaymentResult(PaymentStatus.SUCCESS, transaction_id, "Refund to wallet")

    def check_balance(self) -> float:
        return self._balance


# ============================================================================
# EXAMPLE 4 — Vehicle Capabilities
# ============================================================================
# Not every vehicle can fly, sail, or go off-road. A bicycle doesn't need
# a fly() method. Segregate vehicle capabilities into focused interfaces.


class Drivable(ABC):
    @abstractmethod
    def drive(self, distance_km: float) -> str:
        pass


class Flyable(ABC):
    @abstractmethod
    def fly(self, altitude_ft: float) -> str:
        pass


class Sailable(ABC):
    @abstractmethod
    def sail(self, distance_nm: float) -> str:
        pass


class FuelRefillable(ABC):
    @abstractmethod
    def refuel(self, liters: float) -> str:
        pass


class ElectricChargeable(ABC):
    @abstractmethod
    def charge(self, kwh: float) -> str:
        pass


class Car(Drivable, FuelRefillable):
    def drive(self, distance_km: float) -> str:
        return f"Car driving {distance_km} km"

    def refuel(self, liters: float) -> str:
        return f"Car refueled with {liters} liters"


class ElectricCar(Drivable, ElectricChargeable):
    def drive(self, distance_km: float) -> str:
        return f"Electric car driving {distance_km} km"

    def charge(self, kwh: float) -> str:
        return f"Electric car charged with {kwh} kWh"


class Airplane(Flyable, FuelRefillable):
    def fly(self, altitude_ft: float) -> str:
        return f"Airplane flying at {altitude_ft} ft"

    def refuel(self, liters: float) -> str:
        return f"Airplane refueled with {liters} liters of jet fuel"


class FlyingCar(Drivable, Flyable, FuelRefillable):
    """Futuristic vehicle that drives AND flies."""

    def drive(self, distance_km: float) -> str:
        return f"Flying car driving {distance_km} km on road"

    def fly(self, altitude_ft: float) -> str:
        return f"Flying car airborne at {altitude_ft} ft"

    def refuel(self, liters: float) -> str:
        return f"Flying car refueled with {liters} liters"


class Boat(Sailable, FuelRefillable):
    def sail(self, distance_nm: float) -> str:
        return f"Boat sailing {distance_nm} nautical miles"

    def refuel(self, liters: float) -> str:
        return f"Boat refueled with {liters} liters"


class Bicycle(Drivable):
    """A bicycle only drives — no fuel, no electricity, no flying."""

    def drive(self, distance_km: float) -> str:
        return f"Bicycle pedaling {distance_km} km"


# ============================================================================
# Functions that depend ONLY on the interfaces they need
# ============================================================================

def process_payment(processor: Payable, amount: float) -> None:
    """Works with ANY Payable — doesn't care about refunds or balance."""
    result = processor.pay(amount)
    print(f"  Payment: {result.message} [{result.status.value}]")


def issue_refund(processor: Refundable, transaction_id: str) -> None:
    """Works with ANY Refundable — doesn't care about payment or balance."""
    result = processor.refund(transaction_id)
    print(f"  Refund: {result.message} [{result.status.value}]")


def print_documents(printer: Printable, docs: list[str]) -> None:
    """Works with ANY Printable — doesn't need scan or fax."""
    for doc in docs:
        print(f"  {printer.print_doc(doc)}")


def refuel_vehicles(vehicles: list[FuelRefillable], liters: float) -> None:
    """Works with ANY FuelRefillable — doesn't care if it flies or drives."""
    for v in vehicles:
        print(f"  {v.refuel(liters)}")


# ============================================================================
# DEMO
# ============================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("EXAMPLE 1 — Restaurant Workers")
    print("=" * 60)
    chef = Chef()
    waiter = Waiter()
    manager = Manager()
    head_chef = HeadChef()

    print(chef.cook_food("Pasta Carbonara"))
    print(chef.manage_inventory("Olive Oil", 20))
    print(waiter.serve_table(5))
    print(waiter.handle_billing(5))
    print(manager.manage_inventory("Napkins", 200))
    print(manager.handle_billing(3))
    print(head_chef.cook_food("Truffle Risotto"))
    print(head_chef.handle_billing(1))

    print("\n" + "=" * 60)
    print("EXAMPLE 2 — Document Processing")
    print("=" * 60)
    basic = BasicPrinter()
    office = OfficePrinter()
    allinone = AllInOnePrinter()

    print_documents(basic, ["Report.pdf"])
    print_documents(office, ["Invoice.pdf"])
    print(f"  {office.scan_doc('Contract.pdf')}")
    print_documents(allinone, ["Memo.pdf"])
    print(f"  {allinone.fax_doc('Memo.pdf', '+1-555-0100')}")

    print("\n" + "=" * 60)
    print("EXAMPLE 3 — Payment Methods")
    print("=" * 60)
    cc = CreditCardPayment()
    btc = BitcoinPayment()
    wallet = WalletPayment(balance=50.0)

    process_payment(cc, 99.99)
    issue_refund(cc, "CC-001")
    print(f"  CC Statement: {cc.get_statement(3, 2026)}")

    process_payment(btc, 0.005)
    print(f"  BTC Balance: {btc.check_balance()} BTC")
    # btc has no refund() — and we never need to call it!

    process_payment(wallet, 25.0)
    issue_refund(wallet, "WLT-001")
    print(f"  Wallet Balance: ${wallet.check_balance()}")

    print("\n" + "=" * 60)
    print("EXAMPLE 4 — Vehicle Capabilities")
    print("=" * 60)
    car = Car()
    ecar = ElectricCar()
    plane = Airplane()
    fcar = FlyingCar()
    boat = Boat()
    bike = Bicycle()

    print(car.drive(100))
    print(ecar.drive(80))
    print(ecar.charge(40))
    print(plane.fly(35000))
    print(fcar.drive(50))
    print(fcar.fly(5000))
    print(boat.sail(12))
    print(bike.drive(10))

    print("\nRefueling all fuel-based vehicles:")
    refuel_vehicles([car, plane, fcar, boat], liters=50)
    # bike and ecar are NOT FuelRefillable — they're never forced to implement it!
