# Adapter Pattern — Question 3 (Hard)

## Problem: Legacy XML API ↔ Modern JSON Microservice Bridge

A new microservice communicates via JSON, but it must integrate with a legacy system that only speaks XML. Build a **bi-directional adapter** that translates both ways.

### Requirements

#### Legacy System (cannot modify)
```python
class LegacyOrderSystem:
    def submit_order_xml(self, xml_string: str) -> str:
        """Accepts XML, returns XML response."""

    def get_order_status_xml(self, order_id_xml: str) -> str:
        """Accepts XML order ID, returns XML status."""
```

#### Modern Interface
```python
class OrderService(ABC):
    def submit_order(self, order: dict) -> dict: ...
    def get_order_status(self, order_id: str) -> dict: ...
```

#### Your Adapter Must

1. **Convert dict → XML** for requests TO the legacy system.
2. **Convert XML → dict** for responses FROM the legacy system.
3. Handle **nested structures** — an order has line items:
   ```python
   order = {
       "customer": "Alice",
       "items": [
           {"product": "Laptop", "qty": 1, "price": 999.99},
           {"product": "Mouse", "qty": 2, "price": 29.99},
       ],
       "shipping": {"method": "express", "address": "123 Main St"}
   }
   ```
4. Handle **error responses** — if the legacy system returns `<error>...</error>`, raise a Python exception.

### Expected Usage

```python
legacy = LegacyOrderSystem()
adapter = LegacyOrderAdapter(legacy)

# Modern code uses dict — adapter handles XML translation
result = adapter.submit_order({
    "customer": "Alice",
    "items": [{"product": "Laptop", "qty": 1, "price": 999.99}],
    "shipping": {"method": "standard", "address": "123 Main St"}
})
print(result)  # {"order_id": "ORD-001", "status": "accepted"}

status = adapter.get_order_status("ORD-001")
print(status)  # {"order_id": "ORD-001", "status": "shipped", "tracking": "TRK123"}
```

### Constraints

- Use `xml.etree.ElementTree` for XML processing (stdlib).
- Create helper methods `_dict_to_xml(data, root_tag)` and `_xml_to_dict(xml_string)`.
- Handle lists in XML as repeated elements:
  ```xml
  <items>
    <item><product>Laptop</product><qty>1</qty></item>
    <item><product>Mouse</product><qty>2</qty></item>
  </items>
  ```
- Error XML → raise `LegacySystemError(message)`.

### Think About

- Why is Adapter the right pattern here vs. rewriting the legacy system?
- Could you stack a **Caching Decorator** on top of this adapter for `get_order_status`?
- What if the legacy system changes its XML schema? How do you isolate that change?
