# Mediator Pattern — Question 3 (Hard)

## Problem: Event-Driven UI Form with Cross-Field Validation

Build a form system where UI components communicate through a mediator using events. Changing one field can trigger validation, enable/disable other fields, and update computed fields.

### Requirements

#### Mediator
```python
class FormMediator:
    def register(self, component: FormComponent): ...
    def notify(self, sender: FormComponent, event: str, data: Any): ...
```

#### Components
```python
class FormComponent(ABC):
    name: str
    mediator: FormMediator
    enabled: bool
    value: Any
    
    def set_value(self, value): ...  # triggers mediator.notify
    def on_event(self, event: str, data: Any): ...  # receives events
```

Concrete:
- `DropdownField(name, options)`
- `TextField(name)`
- `CheckboxField(name)`
- `ComputedField(name)` — read-only, value calculated from other fields

#### Scenario: Shipping Form

| Field | Type | Behavior |
|---|---|---|
| country | Dropdown | When changed → updates state options, recalculates tax |
| state | Dropdown | Options depend on country. Disabled if country not selected. |
| zip_code | TextField | Validates format based on country (US: 5 digits, UK: postcode) |
| same_as_billing | Checkbox | When checked → copies billing address, disables address fields |
| shipping_address | TextField | Disabled when same_as_billing is checked |
| shipping_cost | ComputedField | Calculated from country + weight |
| tax | ComputedField | Calculated from country + state + subtotal |
| total | ComputedField | subtotal + shipping_cost + tax |

### Expected Usage

```python
mediator = FormMediator()
country = DropdownField("country", ["US", "UK", "IN"], mediator)
state = DropdownField("state", [], mediator)
zip_code = TextField("zip_code", mediator)
same_as_billing = CheckboxField("same_as_billing", mediator)
shipping_address = TextField("shipping_address", mediator)
shipping_cost = ComputedField("shipping_cost", mediator)
tax = ComputedField("tax", mediator)
total = ComputedField("total", mediator)

country.set_value("US")
# → state enabled, options updated to US states
# → zip_code validation rule changed to "5 digits"
# → shipping_cost recalculated
# → tax recalculated
# → total recalculated

same_as_billing.set_value(True)
# → shipping_address disabled, value copied from billing
```

### Constraints

- Components NEVER reference each other directly — all through the mediator.
- The mediator contains all cross-field coordination logic.
- Events: `"value_changed"`, `"validation_failed"`, `"enabled_changed"`.
- Prevent infinite event loops (field A changes → updates field B → which changes A...).
- Write tests that verify the cascading behavior.

### Think About

- How does this compare to React's state management or Vue's reactivity system?
- What if the form rules come from a configuration file instead of hardcoded in the mediator?
- Could you combine this with Observer pattern? What's the difference?
