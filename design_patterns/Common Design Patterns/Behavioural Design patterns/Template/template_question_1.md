# Template Method Pattern — Question 1 (Easy)

## Problem: Report Generator with Fixed Steps

Different reports (PDF, HTML, CSV) follow the same generation process but differ in specific steps.

### Requirements

- `ReportGenerator(ABC)` with template method `generate(data)`:
  1. `fetch_data()` → get the data (same for all)
  2. `format_header()` → format the report header (abstract)
  3. `format_body(data)` → format the data rows (abstract)
  4. `format_footer()` → add the footer (abstract)
  5. `save(content)` → save to file (abstract)

- Concrete: `PDFReport`, `HTMLReport`, `CSVReport`

### Expected Usage

```python
data = [{"name": "Alice", "score": 95}, {"name": "Bob", "score": 87}]

pdf = PDFReport("grades")
pdf.generate(data)
# → Formatting PDF header...
# → Formatting PDF body (2 rows)...
# → Adding PDF footer...
# → Saved to grades.pdf

html = HTMLReport("grades")
html.generate(data)
# → Formatting HTML header: <html><body>...
# → Formatting HTML body: <table>...
# → Saved to grades.html
```

### Constraints

- `generate()` is defined in the base class and calls the steps in order — subclasses CANNOT change the order.
- Subclasses only override the specific step methods.
