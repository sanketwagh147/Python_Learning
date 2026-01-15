"""Abstract Base Repository """
from abc import ABC, abstractmethod
from typing import List, Optional, Generic, TypeVar
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession

T = TypeVar('T')


class BaseRepository(ABC, Generic[T]):
    """
    Abstract base repository for synchronous operations.
    Following Dependency Inversion Principle.
    Use this for non-async applications, scripts, or CLI tools.
    """
    
    def __init__(self, session: Session):
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


class AsyncBaseRepository(ABC, Generic[T]):
    """
    Abstract base repository for asynchronous operations.
    Following Dependency Inversion Principle.
    Use this for FastAPI, async web frameworks, or async applications.
    """
    
    def __init__(self, session: AsyncSession):
        self._session = session
    
    @abstractmethod
    async def get_all(self) -> List[T]:
        """Retrieve all records"""
        pass
    
    @abstractmethod
    async def get_by_id(self, id: int) -> Optional[T]:
        """Retrieve a single record by ID"""
        pass
    
    @abstractmethod
    async def create(self, entity: T) -> T:
        """Create a new record"""
        pass
    
    @abstractmethod
    async def delete(self, id: int) -> bool:
        """Delete a record by ID"""
        pass
