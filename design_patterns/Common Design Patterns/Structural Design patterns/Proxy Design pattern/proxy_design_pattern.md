# Proxy Design pattern

Proxy is a structural design pattern that lets you provide a substitute/placeholder for another object. It controls the access to original object, allowing us to perform something after or before the requests gets through the original object

## Key Concepts

**Proxy**: A stand-in or placeholder for another object.  
**Real Subject**: The actual object that performs the operations.  
**Client**: The user that interacts with the proxy instead of the real object.

## Types of Proxy Patterns

**Virtual Proxy** – Creates expensive objects on demand (lazy loading).  
**Protection Proxy** – Controls access based on permissions.  
**Remote Proxy** – Represents an object in a different address space (e.g., network communication).  
**Cache Proxy** – Stores frequently used results to improve performance.  
**Logging Proxy** – Logs operations performed on the real object.

## Example 1 (Virtual proxy)

```python

from abc import ABC, abstractmethod
import time

# 1️⃣ subject onf interface
Class Image(abc):

    @abstractmethod
    def display(self):
        image

class RealImage(Image):
    def __init__(self, filename):
        self.filename = filename
        self.load_from_disk()  # Expensive operation

    def load_from_disk(self):
        print(f"Loading image from disk: {self.filename}")
        time.sleep(2)  # Simulating a delay

    def display(self):
        print(f"Displaying image: {self.filename}")

# Step 3: Create the Proxy class
class ProxyImage(Image):
    def __init__(self, filename):
        self.filename = filename
        self.real_image = None  # Lazy initialization

    def display(self):
        if self.real_image is None:
            self.real_image = RealImage(self.filename)  # Load only when needed
        self.real_image.display(

# Step 4: Client Code
print("Client wants to display an image.")
image = ProxyImage("photo.jpg")  # No loading yet
print("Doing other work...")
time.sleep(1)
print("Now displaying the image:")
image.display()  # Loads and displays the image
print("Displaying again:")
image.display()  # No loading, directly displays

```

## Example 2 ( Cache proxy)

```python
import time

# Step 1: Real Subject (Expensive Operation)
class RealAPI:
    def fetch_data(self, query):
        print(f"Fetching data for: {query} from API...")
        time.sleep(2)  # Simulate network delay
        return f"Results for {query}"

# Step 2: Proxy with Caching
class CacheProxy:
    def __init__(self):
        self.real_api = RealAPI()
        self.cache = {}  # Dictionary to store cached results

    def fetch_data(self, query):
        if query in self.cache:
            print(f"Returning cached result for: {query}")
            return self.cache[query]
        else:
            result = self.real_api.fetch_data(query)
            self.cache[query] = result  # Store in cache
            return result

# Step 3: Client Code
api = CacheProxy()
print(api.fetch_data("Python Books"))  # Fetches from API
print(api.fetch_data("Python Books"))  # Returns cached result
print(api.fetch_data("Java Books"))  # Fetches from API
```

## Example 3 (Protection proxy)

```python
from abc import ABC, abstractmethod

# Step 1: Define the Subject interface
class DataAccess(ABC):
    @abstractmethod
    def get_sensitive_data(self):
        pass

# Step 2: Real Subject (Actual Data Access)
class RealDataAccess(DataAccess):
    def get_sensitive_data(self):
        return "Sensitive Data: [User Details, Transactions, etc.]"

# Step 3: Proxy with Access Control
class ProtectionProxy(DataAccess):
    def __init__(self, user_role):
        self.user_role = user_role
        self.real_data_access = RealDataAccess()  # Actual data access

    def get_sensitive_data(self):
        if self.user_role.lower() == "admin":
            return self.real_data_access.get_sensitive_data()
        else:
            return "Access Denied: You do not have permission to view this data."

# Step 4: Client Code
admin_access = ProtectionProxy("admin")
print("Admin Request:", admin_access.get_sensitive_data())

user_access = ProtectionProxy("guest")
print("Guest Request:", user_access.get_sensitive_data())
```

## When to Use the Proxy Pattern?

✔ When object creation is costly and can be delayed (lazy initialization).  
✔ When access to the object needs to be controlled (security).  
✔ When logging, caching, or performance optimizations are required.  
✔ When working with remote objects (e.g., network communication).  
