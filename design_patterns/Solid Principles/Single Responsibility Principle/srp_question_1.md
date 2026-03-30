# Single Responsibility Principle — Question 1 (Easy)

## Problem: Invoice Processing System

Refactor a monolithic `Invoice` class that violates SRP by handling data, calculation, formatting, and persistence all in one class.

### The Violating Code

```python
class Invoice:
    def __init__(self, items):
        self.items = items
    
    def calculate_total(self):
        return sum(i["price"] * i["qty"] for i in self.items)
    
    def generate_pdf(self):
        # PDF generation logic mixed in
        print(f"[PDF] Invoice total: ${self.calculate_total()}")
    
    def save_to_database(self):
        # Database logic mixed in
        print(f"[DB] Saving invoice: {self.items}")
    
    def send_email(self, to):
        # Email logic mixed in
        print(f"[EMAIL] Sending invoice to {to}")
```

### Requirements

Refactor into separate classes, each with ONE responsibility:
- `Invoice`: holds data + calculates total
- `InvoiceFormatter`: generates PDF/HTML/text output
- `InvoiceRepository`: saves/loads from database
- `InvoiceNotifier`: sends email notifications

### Expected Usage After Refactor

```python
invoice = Invoice(items=[{"name": "Widget", "price": 10, "qty": 3}])
total = invoice.calculate_total()  # → 30

formatter = PDFFormatter()
pdf = formatter.format(invoice)  # → PDF bytes/string

repo = InvoiceRepository(database)
repo.save(invoice)

notifier = EmailNotifier(smtp_client)
notifier.send(invoice, to="customer@example.com")
```

### Constraints

- Each class has exactly ONE reason to change.
- `Invoice` doesn't know about formatting, storage, or notifications.
