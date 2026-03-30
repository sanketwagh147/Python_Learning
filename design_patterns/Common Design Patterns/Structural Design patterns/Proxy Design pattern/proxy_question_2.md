# Proxy Pattern — Question 2 (Medium)

## Problem: Access Control Proxy for API Service

Wrap an API service with a proxy that enforces role-based access, logging, and rate limiting — without modifying the service itself.

### Requirements

#### Real Service
```python
class UserService:
    def get_user(self, user_id: str) -> dict: ...
    def create_user(self, data: dict) -> dict: ...
    def delete_user(self, user_id: str) -> bool: ...
    def list_users(self) -> list[dict]: ...
```

#### Proxy
```python
class SecureUserServiceProxy:
    """Wraps UserService with access control, logging, and rate limiting."""
    def __init__(self, service: UserService, current_user_role: str): ...
```

Access rules:
| Method | Allowed Roles |
|---|---|
| `get_user` | viewer, editor, admin |
| `create_user` | editor, admin |
| `delete_user` | admin only |
| `list_users` | viewer, editor, admin |

### Expected Usage

```python
service = UserService()

admin_proxy = SecureUserServiceProxy(service, "admin")
admin_proxy.delete_user("U001")  # ✓ Works

viewer_proxy = SecureUserServiceProxy(service, "viewer")
viewer_proxy.delete_user("U001")
# → PermissionError: Role 'viewer' cannot access 'delete_user'

viewer_proxy.get_user("U001")  # ✓ Works
# → [LOG] viewer called get_user('U001') at 2024-01-15T10:30:00
```

### Constraints

- Proxy must implement the exact same interface as `UserService`.
- Log every method call with timestamp, role, method name, and args.
- Add rate limiting: max 10 calls per minute per proxy instance. Return `RateLimitError` if exceeded.

### Think About

- How is this different from the Decorator pattern? (Proxy controls access; Decorator adds behavior.)
- Could you use `__getattr__` to auto-proxy all methods instead of writing each one?
