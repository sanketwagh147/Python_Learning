# Orchestrator Pattern — Question 1 (Easy)

## Problem: User Registration Orchestrator

Coordinate multiple services during user registration: create account, send welcome email, assign default role.

### Requirements

- `UserService`: `create_user(name, email) -> user_id`
- `EmailService`: `send_welcome_email(email, name)`
- `RoleService`: `assign_role(user_id, role)`
- `RegistrationOrchestrator`: coordinates the three services in order

### Expected Usage

```python
orchestrator = RegistrationOrchestrator(
    user_service=UserService(),
    email_service=EmailService(),
    role_service=RoleService(),
)

result = orchestrator.register("Alice", "alice@example.com")
# → Creating user Alice...
# → Sending welcome email to alice@example.com...
# → Assigning role 'member' to user U-001...
# → Registration complete!

print(result)
# → RegistrationResult(user_id="U-001", email_sent=True, role="member")
```

### Constraints

- The orchestrator controls the ORDER of operations.
- Individual services don't know about each other.
- If any step fails, return a partial result indicating which steps succeeded.
