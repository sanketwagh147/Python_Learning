# Cohesion and Coupling in Software Design (with Examples)

## Cohesion

Cohesion refers to how closely related the responsibilities and functions within a single module, class, or service are. High cohesion means that the elements inside a module belong together and serve a single, well-defined purpose.

### Example: High Cohesion

Suppose you have a microservice responsible only for user authentication:

```python
# user_auth_service.py
class UserAuthService:
    def login(self, username, password):
        # logic for user login
        pass
    def logout(self, user_id):
        # logic for user logout
        pass
    def reset_password(self, email):
        # logic for password reset
        pass
```

All methods are related to authentication, making the service highly cohesive.

### Example: Low Cohesion

A service that handles unrelated tasks:

```python
# mixed_service.py
class MixedService:
    def login(self, username, password):
        pass
    def send_email(self, to, subject, body):
        pass
    def generate_report(self):
        pass
```

Here, the service mixes authentication, email, and reporting—showing low cohesion.

---

## Coupling

Coupling is the degree of interdependence between software modules. Low (loose) coupling is desirable, as it means modules can be changed independently. High (tight) coupling means modules are highly dependent on each other, making changes risky and difficult.

### Example: Loose Coupling

Services communicate via well-defined APIs:

```python
# user_service.py
class UserService:
    def get_user(self, user_id):
        # returns user data
        pass

# order_service.py
class OrderService:
    def create_order(self, user_id, item):
        # calls UserService API to get user info
        pass
```

The services interact only through APIs, so changes in one service have minimal impact on the other.

### Example: Tight Coupling

Services directly depend on each other's internal details:

```python
# order_service.py
from user_service import UserService  # Direct import

class OrderService:
    def create_order(self, user_id, item):
        user_service = UserService()
        user = user_service._get_user_from_db(user_id)  # Accessing internal method
        # ...
```

Here, `OrderService` depends on the internal implementation of `UserService`, making the system tightly coupled.

---

## Summary Table

| Concept  | High/Loose (Good) | Low/Tight (Bad) |
| -------- | ----------------- | --------------- |
| Cohesion | Single purpose    | Unrelated tasks |
| Coupling | Independent       | Interdependent  |

**Best Practice:**

- Aim for high cohesion within modules/services.
- Aim for low (loose) coupling between modules/services.
