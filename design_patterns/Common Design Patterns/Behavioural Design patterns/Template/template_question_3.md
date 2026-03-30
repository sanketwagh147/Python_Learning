# Template Method Pattern — Question 3 (Hard)

## Problem: Authentication Flow with Multi-Factor and External Providers

Build an authentication system where the overall flow is fixed but specific steps vary by provider (local, OAuth, SAML) and MFA method.

### Requirements

#### Template
```python
class AuthenticationFlow(ABC):
    def authenticate(self, credentials: dict) -> AuthResult:
        """Fixed authentication sequence."""
        self.validate_input(credentials)
        identity = self.verify_identity(credentials)  # abstract
        if self.requires_mfa(identity):
            self.send_mfa_challenge(identity)          # abstract
            mfa_code = credentials.get("mfa_code")
            self.verify_mfa(identity, mfa_code)        # abstract
        self.check_account_status(identity)            # concrete (locked? disabled?)
        session = self.create_session(identity)        # abstract
        self.on_login_success(identity, session)       # hook
        return AuthResult(session)
```

#### Concrete Flows
1. **LocalAuthFlow**: username/password from DB, TOTP-based MFA, session stored in DB
2. **OAuthFlow**: redirect to Google/GitHub, verify OAuth token, JWT session
3. **SAMLFlow**: parse SAML assertion, verify signature, create SAML session

#### MFA Strategies (within the template)
- `TOTPVerification`: time-based one-time password
- `SMSVerification`: send code via SMS
- `EmailVerification`: send code via email

### Expected Usage

```python
# Local auth with TOTP
flow = LocalAuthFlow(user_store=db, mfa_method=TOTPVerification())
result = flow.authenticate({
    "username": "alice",
    "password": "secret123",
    "mfa_code": "482910"
})
# → Verifying password for alice... ✓
# → MFA required. Verifying TOTP code... ✓
# → Account status: active ✓
# → Session created: sess_abc123
# → Login event logged


# OAuth with no MFA
flow = OAuthFlow(provider="google")
result = flow.authenticate({"oauth_token": "ya29.xxx"})
# → Verifying Google OAuth token... ✓
# → MFA not required for OAuth
# → Session created: jwt_xyz789
```

### Constraints

- The `authenticate()` sequence NEVER changes — new providers only implement the abstract steps.
- MFA is injected via composition (Strategy inside Template Method).
- `check_account_status()` is concrete in base — checks for locked, disabled, expired. Subclasses inherit it.
- Failed authentication at any step raises `AuthenticationError` with specific details.
- Track login attempts — lock account after 5 consecutive failures.

### Think About

- This combines Template Method + Strategy (for MFA). Why is this better than a single Template for each combination?
- How does this compare to Django's authentication backends?
- Could you add a new step (e.g., CAPTCHA verification) without changing subclasses?
