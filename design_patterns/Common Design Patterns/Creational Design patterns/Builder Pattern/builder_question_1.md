# Builder Pattern — Question 1 (Easy)

## Problem: HTML Form Builder

Build a `FormBuilder` that constructs an HTML form step by step.

### Requirements

- `FormBuilder` should support adding:
  - Text input fields (name, placeholder)
  - A submit button (label)
  - A form title (`<h2>` tag)
- A `build()` method returns the complete HTML string.

### Expected Usage

```python
form = (
    FormBuilder()
    .set_title("Contact Us")
    .add_text_input("name", placeholder="Your name")
    .add_text_input("email", placeholder="Your email")
    .add_submit_button("Send")
    .build()
)
print(form)
```

### Expected Output

```html
<h2>Contact Us</h2>
<form>
  <input type="text" name="name" placeholder="Your name">
  <input type="text" name="email" placeholder="Your email">
  <button type="submit">Send</button>
</form>
```

### Constraints

- Use **method chaining** (each method returns `self`).
- The builder should be **reusable** — calling `build()` should reset internal state.

### Hints

- Store fields in a list. `build()` joins them into one string.
- Think about what happens if `set_title()` is never called.
