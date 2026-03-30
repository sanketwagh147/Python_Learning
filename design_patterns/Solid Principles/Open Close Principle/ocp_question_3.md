# Open-Closed Principle — Question 3 (Hard)

## Problem: Plugin-Based Report Generator with Auto-Discovery

Build a report system where new report formats, data sources, and filters are added as plugins WITHOUT modifying the core framework.

### Requirements

#### Plugin Registry
```python
class PluginRegistry:
    """Auto-discovers and registers plugins using decorators or metaclasses."""
    _formatters: dict[str, type] = {}
    _sources: dict[str, type] = {}
    _filters: dict[str, type] = {}
    
    @classmethod
    def register_formatter(cls, name: str):
        def decorator(klass): ...
        return decorator
    
    @classmethod
    def get_formatter(cls, name: str) -> ReportFormatter: ...
```

#### Core Framework (NEVER modified)
```python
class ReportFramework:
    def generate(self, source_name: str, filters: list[str], format_name: str) -> Report:
        source = PluginRegistry.get_source(source_name)
        data = source.fetch()
        for f_name in filters:
            filter_plugin = PluginRegistry.get_filter(f_name)
            data = filter_plugin.apply(data)
        formatter = PluginRegistry.get_formatter(format_name)
        return formatter.format(data)
```

#### Plugins (new files, new classes — framework untouched)
```python
@PluginRegistry.register_formatter("pdf")
class PDFFormatter(ReportFormatter):
    def format(self, data: list[dict]) -> Report: ...

@PluginRegistry.register_formatter("csv")
class CSVFormatter(ReportFormatter):
    def format(self, data: list[dict]) -> Report: ...

@PluginRegistry.register_source("database")
class DatabaseSource(DataSource):
    def fetch(self) -> list[dict]: ...

@PluginRegistry.register_filter("date_range")
class DateRangeFilter(DataFilter):
    def apply(self, data: list[dict]) -> list[dict]: ...
```

### Expected Usage

```python
framework = ReportFramework()

# Use existing plugins
report = framework.generate(
    source_name="database",
    filters=["date_range", "active_only"],
    format_name="pdf",
)

# Someone adds a new plugin in a separate file:
@PluginRegistry.register_formatter("excel")
class ExcelFormatter(ReportFormatter):
    def format(self, data):
        return Report(content=f"Excel with {len(data)} rows", format="xlsx")

# Framework works with the new plugin — ZERO modifications
report = framework.generate("database", ["date_range"], "excel")
```

### Bonus: Auto-Discovery

```python
# Automatically import all plugins from a directory
PluginRegistry.auto_discover("plugins/")
# Scans plugins/ directory, imports all modules, decorators auto-register
```

### Constraints

- Core `ReportFramework` class is written ONCE and NEVER edited.
- New functionality = new files with decorated classes.
- `PluginRegistry` uses decorators for registration (metaclass approach as bonus).
- Raise `PluginNotFoundError` for unknown plugin names.
- All plugins conform to their respective ABC (`ReportFormatter`, `DataSource`, `DataFilter`).

### Think About

- This is OCP at the architecture level. How do real frameworks (Flask, pytest, Django) use plugin registries?
- What's the difference between decorator-based and metaclass-based auto-registration?
- How does `entry_points` in `setup.py`/`pyproject.toml` achieve similar plugin discovery?
