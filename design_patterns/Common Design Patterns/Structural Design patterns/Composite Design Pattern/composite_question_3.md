# Composite Pattern — Question 3 (Hard)

## Problem: Permission System with Inherited & Overridden ACLs

Model a permission tree where groups contain users and sub-groups. Permissions **inherit downward** but can be **overridden** at any level.

### Requirements

#### Base
```python
class PermissionNode(ABC):
    name: str
    _local_permissions: dict[str, bool]  # e.g., {"read": True, "write": False}
    
    def set_permission(self, perm: str, allowed: bool): ...
    def has_permission(self, perm: str) -> bool: ...
    def effective_permissions(self) -> dict[str, bool]: ...
```

#### User (Leaf)
- Has local permissions.
- `has_permission(perm)` checks local first, then inherits from parent group.
- `effective_permissions()` merges parent's permissions with own (own overrides parent).

#### Group (Composite)
- Contains Users and sub-Groups.
- Has local permissions that all children inherit.
- `add(node)`, `remove(node)`
- Must set `parent` reference on children for upward lookups.

### Expected Usage

```python
company = Group("Company")
company.set_permission("read", True)
company.set_permission("write", False)
company.set_permission("delete", False)

engineering = Group("Engineering")
engineering.set_permission("write", True)  # Override: engineers CAN write
company.add(engineering)

alice = User("Alice")
engineering.add(alice)

bob = User("Bob")
bob.set_permission("delete", True)  # Override: Bob CAN delete
engineering.add(bob)

guest = User("Guest")
company.add(guest)

# Alice inherits: read=True (Company), write=True (Engineering), delete=False (Company)
print(alice.effective_permissions())
# → {"read": True, "write": True, "delete": False}

# Bob: read=True (Company), write=True (Eng), delete=True (own override)
print(bob.effective_permissions())
# → {"read": True, "write": True, "delete": True}

# Guest: read=True (Company), write=False (Company), delete=False (Company)
print(guest.effective_permissions())
# → {"read": True, "write": False, "delete": False}
```

### Constraints

- Permissions resolve **bottom-up**: local → parent → grandparent → ... 
- The first node in the chain that defines a permission wins.
- `has_permission(perm)` returns `False` if the permission is not defined anywhere in the chain.
- Moving a user to another group updates their effective permissions automatically (parent reference changes).

### Test Cases

```python
# Move Alice from Engineering to Company directly
engineering.remove(alice)
company.add(alice)
# Now Alice loses write=True from Engineering
print(alice.has_permission("write"))  # → False (inherits Company's write=False)
```

### Think About

- How does this combine Composite with the Chain of Responsibility-like lookup?
- How would you cache effective permissions and invalidate on changes?
- How does this compare to how Linux file permissions or RBAC systems work?
