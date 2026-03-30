# Factory Pattern — Question 3 (Hard)

## Problem: Abstract Factory — Cross-Platform UI Toolkit

Build an **Abstract Factory** that creates families of related UI components for different platforms.

### Requirements

#### Product Interfaces
```
Button(ABC)       → render(), on_click(callback)
TextField(ABC)    → render(), get_value() -> str
Checkbox(ABC)     → render(), is_checked() -> bool
Dialog(ABC)       → render(), show(title, message)
```

#### Concrete Families
- **Web**: `WebButton`, `WebTextField`, `WebCheckbox`, `WebDialog` — renders HTML
- **Mobile**: `MobileButton`, `MobileTextField`, `MobileCheckbox`, `MobileDialog` — renders native mobile markup
- **Desktop**: `DesktopButton`, `DesktopTextField`, `DesktopCheckbox`, `DesktopDialog` — renders desktop widgets

#### Abstract Factory
```python
class UIFactory(ABC):
    def create_button(self, label: str) -> Button: ...
    def create_text_field(self, placeholder: str) -> TextField: ...
    def create_checkbox(self, label: str) -> Checkbox: ...
    def create_dialog(self) -> Dialog: ...
```

#### Application Layer
```python
class LoginForm:
    """Uses UIFactory — doesn't know which platform it's rendering for."""
    def __init__(self, factory: UIFactory):
        self.username = factory.create_text_field("Username")
        self.password = factory.create_text_field("Password")
        self.remember = factory.create_checkbox("Remember me")
        self.submit = factory.create_button("Login")
        self.dialog = factory.create_dialog()

    def render(self):
        """Render all components."""

    def submit_form(self):
        """Validate and show success/error dialog."""
```

### Expected Usage

```python
# Web platform
web_form = LoginForm(WebUIFactory())
web_form.render()
# → <input type="text" placeholder="Username">
# → <input type="text" placeholder="Password">
# → <input type="checkbox"> Remember me
# → <button>Login</button>

# Mobile platform
mobile_form = LoginForm(MobileUIFactory())
mobile_form.render()
# → [NativeTextField: Username]
# → [NativeTextField: Password]
# → [NativeCheckbox: Remember me]
# → [NativeButton: Login]
```

### Constraints

- `LoginForm` must work with ANY factory — it should never import concrete classes.
- Add a **factory selector** function:
  ```python
  def get_factory(platform: str) -> UIFactory:
      # Returns the right factory for "web", "mobile", or "desktop"
  ```
- All product interfaces use `ABC`.

### Think About

- What happens when you add a new component (e.g., `Dropdown`)? Every factory must be updated.
- What happens when you add a new platform (e.g., `TVUIFactory`)? Only new classes, no changes to existing code.
- When would you pick Abstract Factory over Factory Method?
