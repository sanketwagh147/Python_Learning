# Bridge Pattern — Question 2 (Medium)

## Problem: Report Generator (Format × Data Source)

A reporting system generates reports from different data sources in different formats. Without Bridge, you'd need a class for every combination (CSVFinanceReport, PDFFinanceReport, HTMLSalesReport...).

### Requirements

- **Renderer** (implementation side):
  ```python
  class ReportRenderer(ABC):
      def render_header(self, title: str): ...
      def render_row(self, data: dict): ...
      def render_footer(self, summary: str): ...
      def get_output(self) -> str: ...
  ```
  Concrete: `HTMLRenderer`, `CSVRenderer`, `MarkdownRenderer`

- **Report** (abstraction side):
  ```python
  class Report(ABC):
      def __init__(self, renderer: ReportRenderer): ...
      def generate(self) -> str: ...
  ```
  Concrete: `SalesReport`, `InventoryReport` — each fetches different data and calls renderer methods.

### Expected Usage

```python
# Same report, different formats
sales_html = SalesReport(HTMLRenderer())
print(sales_html.generate())
# <h1>Sales Report</h1><table>...<tr><td>Widget</td><td>$50</td></tr>...</table>

sales_csv = SalesReport(CSVRenderer())
print(sales_csv.generate())
# Sales Report
# product,revenue
# Widget,50
# Gadget,120

inventory_md = InventoryReport(MarkdownRenderer())
print(inventory_md.generate())
# # Inventory Report
# | item | stock |
# |------|-------|
# | Widget | 45 |
```

### Constraints

- Reports contain hardcoded sample data (no real DB needed).
- Show that adding `JSONRenderer` requires only 1 new class — no changes to any Report class.
- Show that adding `FinanceReport` requires only 1 new class — no changes to any Renderer.

### Think About

- Without Bridge, how many classes would you need for 3 reports × 4 renderers?
- How does this relate to the Open/Closed Principle?
