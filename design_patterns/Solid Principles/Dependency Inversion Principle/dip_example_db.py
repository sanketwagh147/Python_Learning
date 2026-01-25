"""DIP Example"""

from abc import ABC, abstractmethod
from typing import Callable


class Database(ABC):

    def __init__(self,name) -> None:
        print(f"Name of Database is {name}")
        self.name = name
        super().__init__()
    
    @abstractmethod
    def connect(self):
        ...

    @abstractmethod
    def fetch(self,query):
        ...

        
class PostgresDatabase(Database):

    
    def connect(self)->Callable:
        print(f"Connected to {self.name}")
        return print

    def fetch(self, query):
        return self.connect()(query)

class MySQLDatabase(Database):

    
    def connect(self)->Callable:
        print(f"Connected to {self.name}")
        return print

    def fetch(self, query):
        return self.connect()(query)

class DataService:
    
    def __init__(self,db:Database) -> None: ## Dependency Injection helps to follow DIP
        self.db = db
        # self.db = PostgresDatabase('postgres')  Violation of DIP as DataService is dependent on concrete class

    def fetch(self,query):
        return self.db.fetch(query)
        

        
if __name__ == "__main__":

    db = PostgresDatabase('postgres')
    data1 = DataService(db)
    data1.fetch("SELECT * FROM users")      
    
    db2 = MySQLDatabase('mysql')
    data2 = DataService(db2)
    data2.fetch("SELECT * FROM products")