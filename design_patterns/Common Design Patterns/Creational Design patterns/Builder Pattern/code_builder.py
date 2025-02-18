class CodeBuilder:
    def __init__(self, class_name):
        self.class_name = class_name
        self.fields = []  # Stores (field_name, field_value) tuples
        self.indent = "  "  # Two spaces for indentation

    def add_field(self, field_name, field_value):
        """Adds a field with a default value to the class."""
        self.fields.append((field_name, field_value))
        return self  # Enables method chaining

    def __str__(self):
        """Generates the class definition with correct indentation."""
        result = [f"class {self.class_name}:"]

        if not self.fields:
            result.append(self.indent + "pass")  # Handle empty class

        else:
            result.append(self.indent + "def __init__(self):")
            for name, value in self.fields:
                result.append(self.indent * 2 + f"self.{name} = {value}")

        return "\n".join(result)


# Sample Usage:
cb = CodeBuilder("Person").add_field("name", '""').add_field("age", "0")
print(cb)
