# Template Design pattern

The Template Method pattern defines the skeleton of an algorithm in a superclass while allowing subclasses to customize specific steps without altering the overall structure.

## Key Concepts

**Defines an Algorithm Template**: The base class provides a step-by-step process with some steps marked as abstract or default implementations.  
**Encapsulates Common Behavior**: Common steps are implemented in the base class, avoiding code duplication.  
Allows Customization: Subclasses override specific steps without modifying the base structure.

## Real-Life Example

Think of making tea or coffee:

1. The overall process is the same: boil water, brew, pour into a cup, add condiments.  
2. The brewing step is different (tea leaves vs. coffee grounds).
3. The condiments step can vary (milk, sugar, lemon, etc.).
