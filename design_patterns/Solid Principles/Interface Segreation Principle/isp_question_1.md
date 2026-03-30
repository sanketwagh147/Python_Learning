# Interface Segregation Principle — Question 1 (Easy)

## Problem: Printer/Scanner/Fax — The Fat Interface

A `Machine` interface forces all implementations to support print, scan, and fax — even simple printers.

### The Violating Code

```python
class Machine(ABC):
    @abstractmethod
    def print_doc(self, doc): ...
    @abstractmethod
    def scan_doc(self, doc): ...
    @abstractmethod
    def fax_doc(self, doc): ...

class MultiFunctionPrinter(Machine):
    def print_doc(self, doc): print(f"Printing: {doc}")
    def scan_doc(self, doc): print(f"Scanning: {doc}")
    def fax_doc(self, doc): print(f"Faxing: {doc}")

class SimplePrinter(Machine):
    def print_doc(self, doc): print(f"Printing: {doc}")
    def scan_doc(self, doc): raise NotImplementedError("Can't scan!")  # ← Forced to implement
    def fax_doc(self, doc): raise NotImplementedError("Can't fax!")    # ← Forced to implement
```

### Requirements

Split into focused interfaces:
- `Printer(ABC)`: `print_doc(doc)`
- `Scanner(ABC)`: `scan_doc(doc)`
- `Faxer(ABC)`: `fax_doc(doc)`

Classes implement ONLY what they support:
- `SimplePrinter(Printer)`: only prints
- `PrinterScanner(Printer, Scanner)`: prints and scans
- `AllInOnePrinter(Printer, Scanner, Faxer)`: does everything

### Expected Usage

```python
def do_printing(printer: Printer):
    printer.print_doc("report.pdf")  # Works for ALL printers

def do_scanning(scanner: Scanner):
    scanner.scan_doc("photo.jpg")  # Only called on scanners

simple = SimplePrinter()
do_printing(simple)  # ✓ Works
# do_scanning(simple)  # Type error — SimplePrinter is not a Scanner
```

### Constraints

- No class implements methods it doesn't support.
- No `NotImplementedError` anywhere.
- Functions accept the narrowest possible interface.
