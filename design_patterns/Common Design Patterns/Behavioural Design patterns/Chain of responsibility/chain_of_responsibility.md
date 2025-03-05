# chain_of_responsibility

Chain of Responsibility is a behavioral design pattern that lets you pass requests along a chain of handlers. Upon receiving a request, each handler decides either to process the request or to pass it to the next handler in the chain.

## Key Concepts

**Handler**: An interface or abstract class that defines a method for handling requests.  
**Concrete Handlers**: Implement the handler interface and decide whether to process the request or pass it to the next handler.  
**Client**: Initiates the request, which is processed by one or more handlers in the chain.

## Example

```python
class Handler:
    """Base handler class that defines the chain behavior."""
    def __init__(self, successor=None):
        self.successor = successor

    def handle_request(self, request):
        if self.successor:
            return self.successor.handle_request(request)
        return f"No handler available for {request}"

class BasicSupport(Handler):
    """Handles basic issues."""
    def handle_request(self, request):
        if request == "basic":
            return "BasicSupport: Resolved the issue!"
        return super().handle_request(request)

class TechnicalSupport(Handler):
    """Handles technical issues."""
    def handle_request(self, request):
        if request == "technical":
            return "TechnicalSupport: Resolved the issue!"
        return super().handle_request(request)

class Manager(Handler):
    """Handles urgent or complex issues."""
    def handle_request(self, request):
        if request == "urgent":
            return "Manager: Resolved the issue!"
        return super().handle_request(request)

# Build the chain: Basic -> Technical -> Manager
support_chain = BasicSupport(TechnicalSupport(Manager()))

# Test requests
print(support_chain.handle_request("basic"))       # Output: BasicSupport: Resolved the issue!
print(support_chain.handle_request("technical"))   # Output: TechnicalSupport: Resolved the issue!
print(support_chain.handle_request("urgent"))      # Output: Manager: Resolved the issue!
print(support_chain.handle_request("billing"))     # Output: No handler available for billing


```

## Example 2

```python
class Handler:
    """Base handler class"""
    def __init__(self, successor=None):
        self.successor = successor

    def handle_request(self, request):
        if self.successor:
            return self.successor.handle_request(request)
        return "Request approved"

class AuthenticationHandler(Handler):
    def handle_request(self, request):
        if not request.get("authenticated", False):
            return "Authentication failed"
        return super().handle_request(request)

class AuthorizationHandler(Handler):
    def handle_request(self, request):
        if request.get("role") != "admin":
            return "Authorization failed"
        return super().handle_request(request)

class DataValidationHandler(Handler):
    def handle_request(self, request):
        if "data" not in request:
            return "Invalid request data"
        return super().handle_request(request)

# Build the chain: Authentication -> Authorization -> Data Validation
handler_chain = AuthenticationHandler(AuthorizationHandler(DataValidationHandler()))

# Test Cases
request1 = {"authenticated": True, "role": "admin", "data": "Valid"}  
print(handler_chain.handle_request(request1))  # ✅ "Request approved"

request2 = {"authenticated": False, "role": "admin", "data": "Valid"}  
print(handler_chain.handle_request(request2))  # ❌ "Authentication failed"

request3 = {"authenticated": True, "role": "user", "data": "Valid"}  
print(handler_chain.handle_request(request3))  # ❌ "Authorization failed"

request4 = {"authenticated": True, "role": "admin"}  
print(handler_chain.handle_request(request4))  # ❌ "Invalid request data"

```

## Notes

✔ Real-world scenario (Customer support system)  
✔ Clear chain structure (Each handler either processes or passes the request)  
✔ Proper method naming (handle_request instead of just handle)  
✔ Graceful fallback if no handler is available
