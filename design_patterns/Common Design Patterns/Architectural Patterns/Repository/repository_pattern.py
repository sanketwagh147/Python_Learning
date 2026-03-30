"""
Repository Pattern — Real-World Example
========================================
Product catalog with multiple storage backends.

The ProductService never knows whether products come from
a database, an API, or a dict in memory.
"""

from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass


# ── Domain Model ────────────────────────────────────────────

@dataclass
class Product:
    id: int
    name: str
    price: float
    category: str


# ── Repository Abstraction ──────────────────────────────────

class ProductRepository(ABC):
    @abstractmethod
    def find_by_id(self, product_id: int) -> Product | None: ...

    @abstractmethod
    def find_by_category(self, category: str) -> list[Product]: ...

    @abstractmethod
    def save(self, product: Product) -> Product: ...

    @abstractmethod
    def delete(self, product_id: int) -> bool: ...


# ── Concrete: In-Memory ────────────────────────────────────

class InMemoryProductRepository(ProductRepository):
    def __init__(self, initial: list[Product] | None = None):
        self._store: dict[int, Product] = {}
        for p in (initial or []):
            self._store[p.id] = p

    def find_by_id(self, product_id: int) -> Product | None:
        return self._store.get(product_id)

    def find_by_category(self, category: str) -> list[Product]:
        return [p for p in self._store.values() if p.category == category]

    def save(self, product: Product) -> Product:
        self._store[product.id] = product
        return product

    def delete(self, product_id: int) -> bool:
        return self._store.pop(product_id, None) is not None


# ── Service Layer (depends on abstraction) ──────────────────

class ProductService:
    """Business logic — has no idea where data comes from."""

    def __init__(self, repo: ProductRepository):
        self._repo = repo

    def get_product(self, product_id: int) -> Product | None:
        return self._repo.find_by_id(product_id)

    def list_by_category(self, category: str) -> list[Product]:
        return self._repo.find_by_category(category)

    def create_product(self, product: Product) -> Product:
        return self._repo.save(product)

    def remove_product(self, product_id: int) -> bool:
        return self._repo.delete(product_id)


# ── Demo ────────────────────────────────────────────────────

if __name__ == "__main__":
    seed = [
        Product(1, "MacBook Pro", 2499.00, "electronics"),
        Product(2, "Python Crash Course", 39.99, "books"),
        Product(3, "Mechanical Keyboard", 149.99, "electronics"),
        Product(4, "Clean Code", 44.99, "books"),
    ]

    # In production: repo = PostgresProductRepository(session)
    repo = InMemoryProductRepository(seed)
    service = ProductService(repo)

    print("=== Find by ID ===")
    print(service.get_product(1))

    print("\n=== Electronics ===")
    for p in service.list_by_category("electronics"):
        print(f"  {p.name} — ${p.price}")

    print("\n=== Create new product ===")
    new = service.create_product(Product(5, "Standing Desk", 599.00, "furniture"))
    print(f"  Created: {new}")

    print("\n=== Delete product 2 ===")
    print(f"  Deleted: {service.remove_product(2)}")
    print(f"  Lookup after delete: {service.get_product(2)}")
