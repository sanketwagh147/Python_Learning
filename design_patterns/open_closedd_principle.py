"""
To understand Open Close principle
1 . Any code block should be open for extension but closed for modification
"""

from abc import ABC, abstractmethod
from enum import Enum, auto


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


class Specification(ABC):

    @abstractmethod
    def is_satisfied(self, item):
        """
        This would be an abstract method which should be overwritten
        """
        pass

    def __and__(self, other):
        """
        This over loads the binary & operator
        use & and not `and`

        """
        return AndSpecification(self, other)


class ColorSpecification(Specification):
    def __init__(self, color):
        self.color = color

    def is_satisfied(self, item):
        return item.color == self.color


class SizeSpecification(Specification):
    def __init__(self, size):
        self.size = size

    def is_satisfied(self, item):
        return item.size == self.size


class QualitySpecification(Specification):
    def __init__(self, quality):
        self.quality = quality

    def is_satisfied(self, item):
        return item.quality == self.quality


class AndSpecification(Specification):
    def __init__(self, *args):
        self.args = args

    def is_satisfied(self, item):
        return all(map(lambda spec: spec.is_satisfied(item), self.args))


class OrSpecification(Specification):
    def __init__(self, *args):
        self.args = args

    def is_satisfied(self, item):
        return any(map(lambda spec: spec.is_satisfied(item), self.args))


class _Filter(ABC):

    @abstractmethod
    def filter(self, items, spec):
        pass


class Filter(_Filter):

    def filter(self, items, spec):
        for item in items:
            if spec.is_satisfied(item):
                yield item


class Product:
    def __init__(self, name, color, size, quality):
        self.name = name
        self.color = color
        self.size = size
        self.quality = quality


apple = Product("Apple", Color.GREEN, Size.SMALL, Quality.ECONOMY)
apple2 = Product("Apple2", Color.GREEN, Size.SMALL, Quality.MEDIUM)
tree = Product("Tree", Color.GREEN, Size.LARGE, Quality.MEDIUM)
tree2 = Product("Tree2", Color.GREEN, Size.LARGE, Quality.ECONOMY)
house = Product("House", Color.BLUE, Size.LARGE, Quality.ECONOMY)
house2 = Product("House2", Color.BLUE, Size.LARGE, Quality.PREMIUM)

products = [apple, apple2, tree2, house2, tree, house]
filter = Filter()

# print("Green products (new):")
# green = ColorSpecification(Color.GREEN)
# for p in filter.filter(products, green):
#     print(f" - {p.name} is green")

# print("Large products:")
large = SizeSpecification(Size.LARGE)
# for p in filter.filter(products, large):
#     print(f" - {p.name} is large")

# print("Large blue items:")
# large_blue = AndSpecification(large, ColorSpecification(Color.BLUE))
large_blue = (
    large & ColorSpecification(Color.BLUE) & QualitySpecification(Quality.PREMIUM)
)
for p in filter.filter(products, large_blue):
    print(f" - {p.name} is large and blue and premium")
