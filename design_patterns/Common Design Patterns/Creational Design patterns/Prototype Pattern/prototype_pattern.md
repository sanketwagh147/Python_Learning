# Prototype Pattern

## **Prototype Design Pattern Summary**  

| Aspect         | Description |
|---------------|------------|
| **Type**      | Creational Pattern |
| **Purpose**   | Creates new objects by copying an existing object (prototype) instead of constructing from scratch. |
| **Key Concept** | Uses cloning (shallow or deep copy) to create object instances efficiently. |
| **When to Use** | When object creation is expensive or complex. |
| **Pros**      | Reduces creation cost, avoids subclassing, simplifies instantiation. |
| **Cons**      | Cloning deep hierarchies can be complex, managing cyclic references is tricky. |

```python
import copy

class Prototype:
    def clone(self):
        return copy.copy(self)  # Shallow copy

class Document(Prototype):
    def __init__(self, title, content):
        self.title = title
        self.content = content

    def __str__(self):
        return f"Document: {self.title}, Content: {self.content}"

# Create an original object
doc1 = Document("Original", "This is the original document.")

# Clone the object
doc2 = doc1.clone()
doc2.title = "Cloned"

print(doc1)  # Document: Original, Content: This is the original document.
print(doc2)  # Document: Cloned, Content: This is the original document.

```
