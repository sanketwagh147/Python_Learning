# 03. Python Web Frameworks (Deep Dive)

## 🚀 1. FastAPI (Primary Focus)

### Core Philosophy
Built on top of **Starlette** (web parts) and **Pydantic** (data parts). It is "Fast" (comparable to NodeJS/Go) because it uses AsyncIO.
- **Dependency Injection:** First-class citizen tailored for cleaner code and testing.
- **Type Hints:** Drive validation AND documentation automatically.

### Key Deep-Dive Topics

#### 1.1 Dependency Injection System
It's a hierarchical system. Dependencies can rely on other dependencies.
```python
from fastapi import Depends, FastAPI

async def common_parameters(q: str | None = None, skip: int = 0, limit: int = 100):
    return {"q": q, "skip": skip, "limit": limit}

@app.get("/items/")
async def read_items(commons: dict = Depends(common_parameters)):
    return commons
```
- **Scope:** Request scope by default, but you can create Singletons.
- **Use Cases:** DB sessions, Auth validation, Rate limiting.

#### 1.2 Pydantic Models & Validation
Pydantic does **Data Parsing**, not just validation. It coerces types.
- **Validators:** `@field_validator` and `@model_validator`.
- **Serialization:** `model_dump()`, `model_dump_json()`.

#### 1.3 Asynchronous Endpoints vs Synchronous
- Use `async def` when your code awaits something (DB, API).
- Use `def` (standard) for CPU-bound tasks. FastAPI runs `def` endpoints in a thread pool to avoid blocking the event loop.

#### 1.4 Middleware
Code that runs **before** and **after** each request.
- **CORS Middleware:** Essential for frontend communication.
- **Authentication Middleware:** Validating JWT tokens globally.

#### 1.5 Background Tasks
Execute tasks **after** returning a response (non-blocking).
```python
from fastapi import BackgroundTasks

def send_email(email: str, message: str):
    # Simulate slow email sending
    time.sleep(5)
    print(f"Email sent to {email}")

@app.post("/send-notification")
async def send_notification(email: str, background_tasks: BackgroundTasks):
    background_tasks.add_task(send_email, email, "Welcome!")
    return {"message": "Notification will be sent in the background"}
```
**Use Case:** Sending emails, writing logs, post-processing after response.

#### 1.6 Security (OAuth2 & JWT)
FastAPI has built-in OAuth2 support.
```python
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@app.get("/users/me")
async def read_users_me(token: str = Depends(oauth2_scheme)):
    user = decode_jwt(token)  # Your logic to decode JWT
    return user
```
- **OAuth2PasswordBearer:** Extracts token from `Authorization: Bearer <token>` header.
- **JWT Flow:** Client gets token from `/token` endpoint. Sends token with each request.

---

## 🎸 2. Django (The Batteries-Included Framework)

### Core Philosophy
Don't Repeat Yourself (DRY). Explicit is better than implicit.
- **MVT Architecture:** Model - View - Template (Standard MVC variation).

### Key Deep-Dive Topics

#### 2.1 The ORM (Object-Relational Mapper)
- **Migrations:** How Django version controls DB schema (`makemigrations`, `migrate`).
- **QuerySet Optimization:**
  - `select_related()` (SQL JOIN) for foreign keys (Forward relationship).
  - `prefetch_related()` (Python-level Join) for Many-to-Many or reverse foreign keys.
  - **N+1 Problem:** A classic performance killer where fetching N objects results in N+1 queries.

#### 2.2 Middleware
Layered system (`process_request`, `process_view`, `process_exception`, `process_response`).
- **Order matters:** Request goes Top -> Bottom. Response goes Bottom -> Top.

#### 2.3 Signals
Decoupled notifications. Send a signal when an event occurs (e.g., `post_save`, `pre_delete`).
- **Warning:** Can make code flow hard to trace. Use sparingly.

#### 2.4 Django REST Framework (DRF)
A powerful toolkit for building Web APIs.
- **Serializers:** Convert model instances to JSON (like Pydantic for Django).
  - `ModelSerializer`: Auto-generates fields from model.
- **ViewSets & Routers:** Reduce boilerplate for CRUD endpoints.
```python
from rest_framework import viewsets
from .models import Product
from .serializers import ProductSerializer

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
```
- **Authentication:** Token, Session, JWT (via `djangorestframework-simplejwt`).
- **Permissions:** `IsAuthenticated`, `IsAdminUser`, custom permissions.

---

## 🧪 3. Flask (The Microframework)

### Core Philosophy
Minimalistic. You choose the tools (ORM, Auth, etc.).

### Key Deep-Dive Topics

#### 3.1 Application Context vs Request Context
- **Application Context (`current_app`):** Keeps track of application-level data (e.g., config, logging).
- **Request Context (`request`, `session`):** Keeps track of request-level data (e.g., URL parameters, user input).
- **"The Stack":** Flask uses thread-locals to push contexts so global proxies work.

#### 3.2 Blueprints
Organizing a large application into components (modules).
- Allows registering views, templates, and static files separately for each component.

---

## ❓ Interview Questions & Answers

**Q1: In FastAPI, what is the difference between `Depends()` and standard function calls?**
> **A:** `Depends` is managed by FastAPI. It handles errors, sub-dependencies, caching (can reuse the same result for the same request), and testing overrides. Standard function calls don't offer these framework integrations.

**Q2: What is the N+1 problem in Django and how do you fix it?**
> **A:** It happens when you access a related object in a loop, causing 1 query for the list and N queries for the items. Fix: Use `select_related` or `prefetch_related` to load everything in 1 or 2 queries.

**Q3: How does Flask handle concurrent requests if it's single-threaded during development?**
> **A:** The Werkzeug dev server spawns threads/processes. In production, you use a WSGI server like Gunicorn/uWSGI with multiple workers/threads to handle concurrency.

**Q4: Compare Django ORM vs SQLAlchemy (often used with FastAPI/Flask).**
> **A:** Django ORM uses the 'Active Record' pattern (methods on model instances). SQLAlchemy uses the 'Data Mapper' pattern (separate session manages persistence). SQLAlchemy is more explicit and powerful for complex queries; Django ORM is faster for standard CRUD.

---

## 🔗 Recommended Resources

- **FastAPI:** [Tiangolo's Official Documentation (It's excellent)](https://fastapi.tiangolo.com/tutorial/)
- **Django:** [Django Project - Topic Guides](https://docs.djangoproject.com/en/stable/topics/)
- **Flask:** [The Flask Mega-Tutorial by Miguel Grinberg](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world)
