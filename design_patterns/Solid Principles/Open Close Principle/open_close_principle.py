"""
Open-Close Principle (OCP) - SOLID Principles

Key Concept: Classes should be OPEN for EXTENSION but CLOSED for MODIFICATION

What this means:
- OPEN for extension: You can add new functionality by creating new classes
- CLOSED for modification: You don't need to change existing, tested code

This example demonstrates the Specification Pattern - a powerful way to
build flexible filtering systems without violating OCP.
"""

from abc import ABC, abstractmethod
from enum import Enum, auto


# ============================================================================
# STEP 1: Define Product Attributes (Enums)
# ============================================================================
# These enums define the possible values for product characteristics


class Color(Enum):
    RED = auto()
    GREEN = auto()
    BLUE = auto()


class Size(Enum):
    SMALL = auto()
    MEDIUM = auto()
    LARGE = auto()


class Quality(Enum):
    ECONOMY = auto()
    MEDIUM = auto()
    PREMIUM = auto()


# ============================================================================
# STEP 2: Define Product Class
# ============================================================================


class Product:
    """Represents a product with multiple attributes that can be filtered"""

    def __init__(self, name: str, color: Color, size: Size, quality: Quality):
        self.name = name
        self.color = color
        self.size = size
        self.quality = quality


# ============================================================================
# STEP 3: Define Specification Pattern (The Core of OCP)
# ============================================================================


class Specification(ABC):
    """
    Abstract base class for all specifications (filtering rules).

    This is the KEY to OCP: Instead of modifying a filter class every time
    we need a new filter, we CREATE a new Specification subclass!
    """

    @abstractmethod
    def is_satisfied(self, item: Product):
        """
        Check if the given item satisfies this specification.
        Each subclass implements its own logic.

        Returns: bool - True if item meets the specification
        """
        pass

    def __and__(self, other):
        """
        Overload the & operator to combine specifications with AND logic.

        Example: color_spec & size_spec creates an AndSpecification

        ⚠️ Important: Use & (bitwise AND), NOT 'and' (logical AND)!
        """
        return AndSpecification(self, other)


# ============================================================================
# STEP 4: Create Concrete Specifications (EXTENSION without MODIFICATION!)
# ============================================================================
# Notice: We're ADDING new classes, not MODIFYING existing ones!


class ColorSpecification(Specification):
    """Filter products by color"""

    def __init__(self, color):
        self.color = color

    def is_satisfied(self, item):
        return item.color == self.color


class SizeSpecification(Specification):
    """Filter products by size"""

    def __init__(self, size):
        self.size = size

    def is_satisfied(self, item):
        return item.size == self.size


class QualitySpecification(Specification):
    """Filter products by quality"""

    def __init__(self, quality):
        self.quality = quality

    def is_satisfied(self, item):
        return item.quality == self.quality


# ============================================================================
# STEP 5: Composite Specifications (Combine multiple rules)
# ============================================================================


class AndSpecification(Specification):
    """
    Combine multiple specifications with AND logic.
    ALL specifications must be satisfied.

    Example: AndSpecification(color_spec, size_spec, quality_spec)
    Returns True only if ALL three specs are satisfied.
    """

    def __init__(self, *args):
        self.args = args

    def is_satisfied(self, item):
        # all() returns True if ALL elements are True
        return all(map(lambda spec: spec.is_satisfied(item), self.args))


class OrSpecification(Specification):
    """
    Combine multiple specifications with OR logic.
    ANY specification must be satisfied.

    Example: OrSpecification(color_spec, size_spec)
    Returns True if EITHER spec is satisfied.
    """

    def __init__(self, *args):
        self.args = args

    def is_satisfied(self, item):
        # any() returns True if ANY element is True
        return any(map(lambda spec: spec.is_satisfied(item), self.args))


# ============================================================================
# STEP 6: The Filter Class (NEVER needs modification! 🎉)
# ============================================================================


class _Filter(ABC):
    """Abstract base class for filters"""

    @abstractmethod
    def filter(self, items, spec):
        pass


class Filter(_Filter):
    """
    Generic filter that works with ANY specification.

    This is the beauty of OCP:
    - This class is CLOSED for modification (we never change it)
    - But OPEN for extension (works with any new Specification we create)

    No matter how many new filter types we add, this class stays the same!
    """

    def filter(self, items, spec):
        """
        Filter items based on a specification.

        Args:
            items: Collection of items to filter
            spec: A Specification object defining the filter criteria

        Yields: Items that satisfy the specification
        """
        for item in items:
            if spec.is_satisfied(item):
                yield item


# ============================================================================
# STEP 7: Usage Examples - See OCP in Action!
# ============================================================================

# Create sample products
apple = Product("Apple", Color.GREEN, Size.SMALL, Quality.ECONOMY)
apple2 = Product("Apple2", Color.GREEN, Size.SMALL, Quality.MEDIUM)
tree = Product("Tree", Color.GREEN, Size.LARGE, Quality.MEDIUM)
tree2 = Product("Tree2", Color.GREEN, Size.LARGE, Quality.ECONOMY)
house = Product("House", Color.BLUE, Size.LARGE, Quality.ECONOMY)
house2 = Product("House2", Color.BLUE, Size.LARGE, Quality.PREMIUM)

products = [apple, apple2, tree2, house2, tree, house]

# Create the filter (only once, never needs modification!)
filter = Filter()

# ===== Example 1: Simple filter - Find all green products =====
print("\n===== Example 1: All GREEN products =====")
green = ColorSpecification(Color.GREEN)
for p in filter.filter(products, green):
    print(f" ✓ {p.name} is green")

# ===== Example 2: Find all large products =====
print("\n===== Example 2: All LARGE products =====")
large = SizeSpecification(Size.LARGE)
for p in filter.filter(products, large):
    print(f" ✓ {p.name} is large")

# ===== Example 3: Combined filter - Large AND Blue AND Premium =====
print("\n===== Example 3: LARGE + BLUE + PREMIUM products =====")
# Notice how we use & operator to combine specifications!
large_blue_premium = (
    large & ColorSpecification(Color.BLUE) & QualitySpecification(Quality.PREMIUM)
)
for p in filter.filter(products, large_blue_premium):
    print(f" ✓ {p.name} is large and blue and premium")

# ===== Example 4: OR logic - Small OR Economy =====
print("\n===== Example 4: SMALL OR ECONOMY products =====")
small_or_economy = OrSpecification(
    SizeSpecification(Size.SMALL), QualitySpecification(Quality.ECONOMY)
)
for p in filter.filter(products, small_or_economy):
    print(f" ✓ {p.name} is small or economy quality")

# ===== Example 5: Complex combination =====
print("\n===== Example 5: (GREEN AND LARGE) OR (BLUE AND PREMIUM) =====")
complex_spec = OrSpecification(
    AndSpecification(ColorSpecification(Color.GREEN), SizeSpecification(Size.LARGE)),
    AndSpecification(
        ColorSpecification(Color.BLUE), QualitySpecification(Quality.PREMIUM)
    ),
)
for p in filter.filter(products, complex_spec):
    print(f" ✓ {p.name} matches the complex criteria")

print("\n" + "=" * 60)
print("🎉 Notice: We never modified the Filter class!")
print("We extended functionality by creating new Specifications!")
print("=" * 60)
