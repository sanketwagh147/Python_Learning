Below is a **clean, production-grade Markdown requirements document** for your system.

---

````markdown
# JSON Transformation Engine (JMESPath-based)

## 1. Overview

This system transforms an input JSON into a simplified output JSON using:

- A **YAML configuration file**
- :contentReference[oaicite:0]{index=0} for querying
- Custom functions for extended logic

The system supports:
- Field mapping
- Array extraction
- Aggregations
- Reuse of computed fields
- Custom transformations

---

## 2. Goals

- Accept **input JSON**
- Accept a **single YAML transformation file**
- Produce a **transformed JSON output**
- Support **custom functions**
- Support **field dependencies (computed values reuse)**

---

## 3. Non-Goals

- Full scripting engine (no loops, no complex control flow)
- No database or API fetching
- No UI layer

---

## 4. Input / Output

### 4.1 Input JSON
Any valid JSON object.

### 4.2 YAML Config

```yaml
mappings:
  name: user.name
  total: sum_array(orders[].price)
  upperName:
    expr: user.name
    transform: upper
  tax: total * `0.15`
````

### 4.3 Output JSON

```json
{
  "name": "Sanket",
  "total": 300,
  "upperName": "SANKET",
  "tax": 45
}
```

---

## 5. Core Concepts

### 5.1 Mapping

Each key in `mappings` represents an output field.

| Type   | Description                                 |
| ------ | ------------------------------------------- |
| String | Direct JMESPath expression                  |
| Object | Advanced mapping (expr, transform, default) |
| Nested | Recursive mapping                           |

---

### 5.2 Expression Types

#### Simple Expression

```yaml
name: user.name
```

#### Function Expression

```yaml
total: sum_array(orders[].price)
```

#### Object Mapping

```yaml
upperName:
  expr: user.name
  transform: upper
```

---

### 5.3 Constants

JMESPath requires constants to be wrapped:

```yaml
tax: total * `0.15`
```

---

## 6. Execution Model

### 6.1 Context-Based Evaluation

The system maintains a **context object**:

```json
{
  "name": "Sanket",
  "total": 300
}
```

Each mapping:

1. Evaluates expression
2. Stores result in context
3. Makes it available for next mappings

---

### 6.2 Data Merge Strategy

Each evaluation runs against:

```python
merged_data = {
  **input_json,
  **context
}
```

---

### 6.3 Execution Order

Mappings are processed **top-to-bottom**.

Example:

```yaml
mappings:
  total: sum_array(orders[].price)
  tax: total * `0.15`
```

Valid because `total` is already computed.

---

### 6.4 Invalid Case

```yaml
mappings:
  tax: total * `0.15`
  total: sum_array(...)
```

❌ `total` not available yet

---

## 7. Custom Functions

Custom functions extend JMESPath.

### 7.1 Supported Examples

| Function  | Description                 |
| --------- | --------------------------- |
| sum_array | Sum of array                |
| upper     | Convert string to uppercase |

---

### 7.2 Example Usage

```yaml
total: sum_array(orders[].price)
upperName: upper(user.name)
```

---

## 8. Transformation Features

### 8.1 Default Values

```yaml
country:
  expr: user.country
  default: "India"
```

---

### 8.2 Transform Pipeline

```yaml
field:
  expr: user.name
  transform: upper
```

---

### 8.3 Nested Output

```yaml
mappings:
  user:
    name: user.name
    city: user.address.city
```

---

## 9. Engine Design

### 9.1 Components

```text
Input JSON
     ↓
YAML Loader
     ↓
Transformation Engine
     ↓
JMESPath Evaluator (+ Custom Functions)
     ↓
Output JSON
```

---

### 9.2 Core Responsibilities

| Component | Responsibility        |
| --------- | --------------------- |
| Loader    | Parse YAML            |
| Engine    | Traverse mappings     |
| Evaluator | Execute JMESPath      |
| Context   | Store computed values |

---

## 10. Algorithm

1. Load input JSON

2. Load YAML config

3. Initialize empty context `{}`

4. For each mapping (top-to-bottom):

   * Merge input + context
   * Evaluate expression
   * Apply default (if needed)
   * Apply transform (if defined)
   * Store result in:

     * Output JSON
     * Context

5. Return output JSON

---

## 11. Error Handling

### 11.1 Missing Path

* Return `null` OR use default

### 11.2 Invalid Expression

* Raise validation error

### 11.3 Undefined Dependency

* Error if referencing unknown field

---

## 12. Constraints

* Order-dependent execution
* No circular dependency handling (initial version)
* JMESPath limitations apply

---

## 13. Future Enhancements

### 13.1 Dependency Graph

* Auto-resolve execution order

### 13.2 Validation Layer

* Detect missing fields
* Detect invalid expressions

### 13.3 Debug Mode

```json
{
  "field": "tax",
  "expr": "total * 0.15",
  "value": 45
}
```

---

### 13.4 Expression Caching

* Precompile JMESPath expressions

---

## 14. Recommended Tech Stack

* Python
* jmespath
* PyYAML

---

## 15. Summary

This system provides:

* Config-driven JSON transformation
* Reusable computed values via context
* Extensible logic via custom functions
* Clean separation of config and execution

It behaves like a lightweight **Camunda-style mapping engine**, but focused on JSON transformation.

```

---

If you want next step, I can:
- Convert this into a **ready GitHub repo structure**
- Or generate a **plug-and-play FastAPI service using this spec**
```
