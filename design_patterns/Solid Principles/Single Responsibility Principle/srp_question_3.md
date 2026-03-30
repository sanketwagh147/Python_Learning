# Single Responsibility Principle — Question 3 (Hard)

## Problem: Identify and Fix SRP Violations in a Real Application

You're given a "kitchen sink" class that handles HTTP requests for a REST API. Find ALL SRP violations, explain why each is a violation, and refactor into clean, focused classes.

### The Violating Code

```python
class OrderController:
    def __init__(self, db_connection):
        self.db = db_connection
    
    def handle_request(self, request):
        # 1. Authentication
        token = request.headers.get("Authorization")
        if not token or not token.startswith("Bearer "):
            return {"status": 401, "error": "Unauthorized"}
        payload = jwt.decode(token[7:], "secret_key", algorithms=["HS256"])
        user_id = payload["user_id"]
        
        # 2. Input validation
        body = request.json
        if not body.get("items") or not isinstance(body["items"], list):
            return {"status": 400, "error": "Items required"}
        for item in body["items"]:
            if item["quantity"] < 1:
                return {"status": 400, "error": "Invalid quantity"}
        
        # 3. Business logic — pricing
        total = 0
        for item in body["items"]:
            product = self.db.query(f"SELECT price FROM products WHERE id = '{item['product_id']}'")
            if not product:
                return {"status": 404, "error": f"Product {item['product_id']} not found"}
            total += product["price"] * item["quantity"]
        
        # Apply discount
        if total > 100:
            total *= 0.9  # 10% discount
        
        # 4. Payment processing
        import stripe
        charge = stripe.Charge.create(amount=int(total * 100), currency="usd", source=body.get("payment_token"))
        
        # 5. Persistence
        order_id = str(uuid.uuid4())
        self.db.execute(f"INSERT INTO orders VALUES ('{order_id}', '{user_id}', {total}, 'paid')")
        for item in body["items"]:
            self.db.execute(
                f"INSERT INTO order_items VALUES ('{order_id}', '{item['product_id']}', {item['quantity']})"
            )
        
        # 6. Send confirmation
        email = self.db.query(f"SELECT email FROM users WHERE id = '{user_id}'")
        import smtplib
        server = smtplib.SMTP("smtp.example.com")
        server.sendmail("orders@example.com", email, f"Order {order_id} confirmed!")
        
        # 7. Logging
        with open("orders.log", "a") as f:
            f.write(f"{datetime.now()} - Order {order_id} placed by {user_id} for ${total}\n")
        
        # 8. Analytics
        import requests
        requests.post("https://analytics.example.com/events", 
                      json={"event": "order_placed", "total": total, "user": user_id})
        
        return {"status": 201, "order_id": order_id, "total": total}
```

### Task

1. **Identify ALL violations** — list at least 8 distinct responsibilities crammed into this class.
2. **Identify security issues** beyond SRP (there are at least 3).
3. **Refactor** into separate classes:
   - `Authenticator`
   - `OrderValidator`
   - `PricingService`
   - `PaymentGateway`
   - `OrderRepository`
   - `NotificationService`
   - `OrderLogger`
   - `AnalyticsClient`
   - `OrderController` (thin — only routes requests to services)

4. Each service should use dependency injection and be independently testable.

### Constraints

- The refactored `OrderController.handle_request()` should be ~15-20 lines: authenticate → validate → price → pay → persist → notify → log → respond.
- Fix the SQL injection vulnerabilities (use parameterized queries).
- Fix the hardcoded JWT secret.
- Each class must be unit-testable in isolation.

### Think About

- How many of these 8 responsibilities could independently change for different business reasons?
- If the analytics provider changes from HTTP to Kafka, how many classes change? (Just 1.)
- Is there a point where too many tiny classes becomes a problem? What's the balance?
