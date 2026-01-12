"""
SQLAlchemy models for temp schema tables
"""
import time
from sqlalchemy import create_engine, Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker, scoped_session
import threading

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'
    __table_args__ = {'schema': 'temp'}
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String)
    last_name = Column(String)
    
    # Relationship
    orders = relationship('Order', back_populates='user')
    
    def __repr__(self):
        return f"<User(id={self.id}, first_name='{self.first_name}', last_name='{self.last_name}')>"


class Product(Base):
    __tablename__ = 'products'
    __table_args__ = {'schema': 'temp'}
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    department = Column(String)
    price = Column(Integer)
    weight = Column(Integer)
    
    # Relationship
    orders = relationship('Order', back_populates='product')
    
    def __repr__(self):
        return f"<Product(id={self.id}, name='{self.name}', department='{self.department}', price={self.price})>"


class Order(Base):
    __tablename__ = 'orders'
    __table_args__ = {'schema': 'temp'}
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('temp.users.id'))
    product_id = Column(Integer, ForeignKey('temp.products.id'))
    paid = Column(Boolean)
    
    # Relationships
    user = relationship('User', back_populates='orders')
    product = relationship('Product', back_populates='orders')
    
    def __repr__(self):
        return f"<Order(id={self.id}, user_id={self.user_id}, product_id={self.product_id}, paid={self.paid})>"


# Database connection setup
def get_session(connection_string):
    """Create and return a database session"""
    engine = create_engine(connection_string)
    Session = sessionmaker(bind=engine)
    return Session()


# ==================== SOLID Design Pattern: Repository Pattern ====================
# Following SOLID Principles:
# - Single Responsibility: Each repository handles ONLY one entity
# - Open/Closed: Can add new repositories without modifying existing ones
# - Dependency Inversion: Depend on abstract base class, not concrete implementations
# - Interface Segregation: Each repository has specific methods for its entity

from abc import ABC, abstractmethod
from typing import List, Optional, Generic, TypeVar

T = TypeVar('T')


class BaseRepository(ABC, Generic[T]):
    """
    Abstract base repository following Dependency Inversion Principle.
    All concrete repositories depend on this abstraction.
    """
    
    def __init__(self, session):
        self._session = session
    
    @abstractmethod
    def get_all(self) -> List[T]:
        """Retrieve all records"""
        pass
    
    @abstractmethod
    def get_by_id(self, id: int) -> Optional[T]:
        """Retrieve a single record by ID"""
        pass
    
    @abstractmethod
    def create(self, entity: T) -> T:
        """Create a new record"""
        pass
    
    @abstractmethod
    def delete(self, id: int) -> bool:
        """Delete a record by ID"""
        pass


class UserRepository(BaseRepository[User]):
    """
    Single Responsibility: Handles ONLY User data access operations.
    No business logic, no connection management - just data access.
    """
    
    def get_all(self) -> List[User]:
        """Get all users from the database"""
        return self._session.query(User).all()
    
    def get_by_id(self, id: int) -> Optional[User]:
        """Get a specific user by ID"""
        return self._session.query(User).filter(User.id == id).first()
    
    def get_by_name(self, first_name: str, last_name: str) -> List[User]:
        """Get users by first and last name"""
        return self._session.query(User).filter(
            User.first_name == first_name,
            User.last_name == last_name
        ).all()
    
    def create(self, entity: User) -> User:
        """Create a new user"""
        self._session.add(entity)
        self._session.commit()
        self._session.refresh(entity)
        return entity
    
    def delete(self, id: int) -> bool:
        """Delete a user by ID"""
        user = self.get_by_id(id)
        if user:
            self._session.delete(user)
            self._session.commit()
            return True
        return False


class ProductRepository(BaseRepository[Product]):
    """
    Single Responsibility: Handles ONLY Product data access operations.
    """
    
    def get_all(self) -> List[Product]:
        """Get all products from the database"""
        return self._session.query(Product).all()
    
    def get_by_id(self, id: int) -> Optional[Product]:
        """Get a specific product by ID"""
        return self._session.query(Product).filter(Product.id == id).first()
    
    def get_by_department(self, department: str) -> List[Product]:
        """Get all products in a specific department"""
        return self._session.query(Product).filter(
            Product.department == department
        ).all()
    
    def get_by_price_range(self, min_price: int, max_price: int) -> List[Product]:
        """Get products within a price range"""
        return self._session.query(Product).filter(
            Product.price >= min_price,
            Product.price <= max_price
        ).all()
    
    def create(self, entity: Product) -> Product:
        """Create a new product"""
        self._session.add(entity)
        self._session.commit()
        self._session.refresh(entity)
        return entity
    
    def delete(self, id: int) -> bool:
        """Delete a product by ID"""
        product = self.get_by_id(id)
        if product:
            self._session.delete(product)
            self._session.commit()
            return True
        return False


class OrderRepository(BaseRepository[Order]):
    """
    Single Responsibility: Handles ONLY Order data access operations.
    """
    
    def get_all(self) -> List[Order]:
        """Get all orders from the database"""
        return self._session.query(Order).all()
    
    def get_by_id(self, id: int) -> Optional[Order]:
        """Get a specific order by ID"""
        return self._session.query(Order).filter(Order.id == id).first()
    
    def get_by_user(self, user_id: int) -> List[Order]:
        """Get all orders for a specific user"""
        return self._session.query(Order).filter(Order.user_id == user_id).all()
    
    def get_by_product(self, product_id: int) -> List[Order]:
        """Get all orders for a specific product"""
        return self._session.query(Order).filter(Order.product_id == product_id).all()
    
    def get_paid_orders(self) -> List[Order]:
        """Get all paid orders"""
        return self._session.query(Order).filter(Order.paid == True).all()
    
    def get_unpaid_orders(self) -> List[Order]:
        """Get all unpaid orders"""
        return self._session.query(Order).filter(Order.paid == False).all()
    
    def create(self, entity: Order) -> Order:
        """Create a new order"""
        self._session.add(entity)
        self._session.commit()
        self._session.refresh(entity)
        return entity
    
    def delete(self, id: int) -> bool:
        """Delete an order by ID"""
        order = self.get_by_id(id)
        if order:
            self._session.delete(order)
            self._session.commit()
            return True
        return False


class DatabaseSession:
    """
    ⚠️ NOT THREAD-SAFE! Use ThreadSafeDatabaseSession for multithreading.
    Single Responsibility: Manages database connection lifecycle.
    Separate from repositories - follows SRP.
    """
    
    def __init__(self, connection_string: str):
        self.engine = create_engine(connection_string)
        self.Session = sessionmaker(bind=self.engine)
    
    def __enter__(self):
        """Context manager entry - creates session"""
        self.session = self.Session()
        return self.session
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit - closes session"""
        if exc_type:
            self.session.rollback()
        self.session.close()


class ThreadSafeDatabaseSession:
    """
    ✅ THREAD-SAFE: Uses scoped_session for thread-local sessions.
    Each thread automatically gets its own session.
    
    Key features:
    - Thread-local storage: Each thread gets isolated session
    - Automatic cleanup: Sessions are removed after use
    - Connection pooling: Engine is shared (thread-safe)
    """
    
    def __init__(self, connection_string: str, pool_size: int = 5, max_overflow: int = 10):
        """
        Args:
            connection_string: Database connection URL
            pool_size: Number of persistent connections in pool
            max_overflow: Max temporary connections beyond pool_size
        """
        self.engine = create_engine(
            connection_string,
            pool_size=pool_size,
            max_overflow=max_overflow,
            pool_pre_ping=True  # Verify connections before use
        )
        # scoped_session provides thread-local sessions
        self.Session = scoped_session(sessionmaker(bind=self.engine))
        self._local = threading.local()
    
    def get_session(self):
        """
        Get a thread-local session. Each thread gets its own session.
        Safe to call from multiple threads simultaneously.
        """
        return self.Session()
    
    def __enter__(self):
        """Context manager entry - creates thread-local session"""
        self._local.session = self.Session()
        return self._local.session
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit - closes and removes thread-local session"""
        if exc_type:
            self._local.session.rollback()
        self._local.session.close()
        self.Session.remove()  # Remove thread-local session
    
    def close_all(self):
        """Close all thread-local sessions and dispose engine"""
        self.Session.remove()
        self.engine.dispose()


# Example usage following Dependency Injection (DIP):
if __name__ == "__main__":
    # Connection string
    conn_string = "postgresql://sanket:test@localhost:5432/local_db"
    
    # ========== Single-threaded example ==========
    print("=== Single-threaded example ===")
    with DatabaseSession(conn_string) as session:
        start_time = time.perf_counter()
        user_repo = UserRepository(session)
        product_repo = ProductRepository(session)
        order_repo = OrderRepository(session)
        
        all_users = user_repo.get_all()
        all_products = product_repo.get_all()
        all_orders = order_repo.get_all()
        
        print(f"Users: {len(all_users)}")
        print(f"Products: {len(all_products)}")
        print(f"Orders: {len(all_orders)}")
        print(f"Time: {time.perf_counter() - start_time:.4f}s\n")
    
    # ========== Multi-threaded example (THREAD-SAFE) ==========
    print("=== Multi-threaded example (Thread-Safe) ===")
    print("Each thread fetches data from ONE table only\n")
    db_manager = ThreadSafeDatabaseSession(conn_string)
    
    # Shared storage for results
    results = {}
    
    def fetch_users():
        """Thread 1: Fetch users only"""
        with db_manager as session:
            print(f"Thread-Users: Starting... Session ID: {id(session)}")
            user_repo = UserRepository(session)
            users = user_repo.get_all()
            results['users'] = users
            print(f"Thread-Users: Fetched {len(users)} users")
            time.sleep(0.1)  # Simulate processing
            print(f"Thread-Users: Done!")
    
    def fetch_products():
        """Thread 2: Fetch products only"""
        with db_manager as session:
            print(f"Thread-Products: Starting... Session ID: {id(session)}")
            product_repo = ProductRepository(session)
            products = product_repo.get_all()
            results['products'] = products
            print(f"Thread-Products: Fetched {len(products)} products")
            time.sleep(0.1)  # Simulate processing
            print(f"Thread-Products: Done!")
    
    def fetch_orders():
        """Thread 3: Fetch orders only"""
        with db_manager as session:
            print(f"Thread-Orders: Starting... Session ID: {id(session)}")
            order_repo = OrderRepository(session)
            orders = order_repo.get_all()
            results['orders'] = orders
            print(f"Thread-Orders: Fetched {len(orders)} orders")
            time.sleep(0.1)  # Simulate processing
            print(f"Thread-Orders: Done!")
    
    # Create threads - each responsible for ONE table
    start_time = time.perf_counter()
    
    thread_users = threading.Thread(target=fetch_users, name="UserThread")
    thread_products = threading.Thread(target=fetch_products, name="ProductThread")
    thread_orders = threading.Thread(target=fetch_orders, name="OrderThread")
    
    # Start all threads
    thread_users.start()
    thread_products.start()
    thread_orders.start()
    
    # Wait for all threads to complete
    thread_users.join()
    thread_products.join()
    thread_orders.join()
    
    print(f"\n✅ All threads completed!")
    print(f"Total results: Users={len(results['users'])}, Products={len(results['products'])}, Orders={len(results['orders'])}")
    print(f"Total time (3 parallel threads): {time.perf_counter() - start_time:.4f}s")
    
    # Cleanup
    db_manager.close_all()


