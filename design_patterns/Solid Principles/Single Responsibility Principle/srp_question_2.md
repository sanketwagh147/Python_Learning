# Single Responsibility Principle — Question 2 (Medium)

## Problem: User Registration with Logging, Validation, and Event Publishing

A `UserService` is responsible for too many things. Break it apart.

### The Violating Code

```python
class UserService:
    def register(self, name, email, password):
        # Validation
        if not name or len(name) < 2:
            raise ValueError("Invalid name")
        if "@" not in email:
            raise ValueError("Invalid email")
        if len(password) < 8:
            raise ValueError("Weak password")
        
        # Password hashing
        import hashlib
        hashed = hashlib.sha256(password.encode()).hexdigest()
        
        # Save to database
        user = {"name": name, "email": email, "password": hashed}
        self.db.insert("users", user)
        
        # Logging
        with open("app.log", "a") as f:
            f.write(f"User registered: {email}\n")
        
        # Send welcome email
        import smtplib
        server = smtplib.SMTP("localhost")
        server.sendmail("app@example.com", email, "Welcome!")
        
        # Publish event
        self.event_bus.publish("user_registered", {"email": email})
        
        return user
```

### Requirements

Refactor into:
- `UserValidator`: validates name, email, password
- `PasswordHasher`: hashes passwords (strategy pattern potential)
- `UserRepository`: database operations
- `Logger`: logging operations
- `EmailService`: sends emails
- `EventPublisher`: publishes domain events
- `UserRegistrationService`: **orchestrates** all the above

### Expected Usage After Refactor

```python
service = UserRegistrationService(
    validator=UserValidator(),
    hasher=PasswordHasher(),
    repo=UserRepository(db),
    logger=Logger("app.log"),
    email=EmailService(smtp),
    events=EventPublisher(bus),
)

user = service.register("Alice", "alice@example.com", "secure_pass_123")
```

### Constraints

- Each class has ONE responsibility — if requirements change for email sending, ONLY `EmailService` changes.
- `UserRegistrationService` depends on abstractions (interfaces), not concrete implementations.
- Write unit tests for `UserValidator` in isolation (no DB, no email, no logging needed).

### Think About

- Does the `UserRegistrationService` violate SRP by wiring everything together? (No — its single responsibility IS orchestration.)
- How does SRP relate to DIP (Dependency Inversion)?
