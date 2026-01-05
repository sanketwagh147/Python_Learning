# 04. API Design & Database Optimization

## 🌐 1. RESTful API Design (Deep Dive)

### Core Principles (Richardson Maturity Model)
- **Level 0:** The Swamp of POX (Plain Old XML/JSON). One endpoint, everything via POST.
- **Level 1:** Resources. Distinct URLs for distinct resources (`/users`, `/products`).
- **Level 2:** HTTP Verbs. Correct usage of GET, POST, PUT, DELETE, PATCH.
- **Level 3:** HATEOAS (Hypermedia As The Engine Of Application State). Responses include links to related actions.

### Idempotency
- **Idempotent:** Making the same request multiple times has the same effect as making it once.
  - **GET, PUT, DELETE** are Idempotent.
  - **POST, PATCH** are usually NOT Idempotent.
  - **Why it matters:** Network retries. If a client retries a `POST /charge` (charge credit card) due to timeout, you need idempotency keys to prevent double billing.

### Versioning Strategies
1. **URI Path:** `/api/v1/users` (Most common, caching friendly).
2. **Query Param:** `/api/users?version=1` (Easy to implement).
3. **Custom Header:** `Accept-Version: v1` (Clean URLs, arguably harder to cache).

### Security
- **Authentication:** Who are you? (OAuth2, API Keys).
- **Authorization:** What can you do? (RBAC - Role Based Access Control, ABAC - Attribute Based).
- **Rate Limiting:** Protect against DDoS. Token Bucket algorithm.

### HTTP Status Codes (Common Ones)
| Code | Meaning | When to Use |
|:---:|:---|:---|
| **200** | OK | Successful GET/PUT/PATCH |
| **201** | Created | Successful POST creating a resource |
| **204** | No Content | Successful DELETE (nothing to return) |
| **400** | Bad Request | Malformed request syntax, invalid data |
| **401** | Unauthorized | Missing or invalid authentication |
| **403** | Forbidden | Authenticated but lacks permission |
| **404** | Not Found | Resource doesn't exist |
| **409** | Conflict | Request conflicts with current state (e.g., duplicate email) |
| **422** | Unprocessable Entity | Valid syntax but semantic error (FastAPI uses this) |
| **429** | Too Many Requests | Rate limit exceeded |
| **500** | Internal Server Error | Server-side bug |
| **502** | Bad Gateway | Upstream server error (common in microservices) |
| **503** | Service Unavailable | Server overloaded or in maintenance |

---

## 🗄️ 2. Database Optimization using SQL (Deep Dive)

### Indexing Strategies
Indexes are "pointers" to data that speed up retrieval but slow down writes (INSERT/UPDATE/DELETE).
- **B-Tree Index:** Default. Good for range queries (`<`, `>`, `=`).
- **Hash Index:** Only for equality checks (`=`). Very fast.
- **Composite Index:** Multi-column index (`CREATE INDEX idx_name_age ON Users (Lastname, Age)`).
  - **Leftmost Prefix Rule:** This index works for querying `Lastname` OR `Lastname + Age`. It usually does **NOT** work for querying just `Age`.

### ACID Properties (Transaction Management)
- **A - Atomicity:** All or nothing. If one part fails, the whole transaction rolls back.
- **C - Consistency:** The DB goes from one valid state to another valid state (constraints respected).
- **I - Isolation:** Concurrent transactions shouldn't interfere.
  - *Isolation Levels:* Read Uncommitted (Dirty reads) -> Read Committed -> Repeatable Read (Phantom reads) -> Serializable (Slowest, safest).
- **D - Durability:** Once committed, it survives power loss (Write-Ahead Logging - WAL).

### Normalization vs Denormalization
- **Normalization (3NF):** Minimize redundancy. Good for write-heavy systems, consistency.
- **Denormalization:** Duplicate data to avoid complex JOINs. Good for read-heavy variants (BI, Analytics).

### Connection Pooling
Opening a DB connection is expensive (TCP handshake + Auth).
- **Solution:** Maintain a pool of active connections. Clients borrow a connection, use it, and return it.
- **Tools:** PgBouncer (PostgreSQL), SQLAlchemy `QueuePool`.

---

## ⚡ 3. GraphQL vs REST (Deep Dive)

### Core Concept
- **REST:** Multiple Endpoints (`/users`, `/posts`). Server defines structure. Over-fetching/Under-fetching is common.
- **GraphQL:** Single Endpoint (`/graphql`). Client defines structure. Exact fetching.

### The Problem it Solves
- **Over-fetching:** Getting more data than needed. (e.g., getting whole User object when you just need the name).
- **Under-fetching:** Needing to make N+1 API calls to get related data (e.g., getUser -> getPosts for user).
- **GraphQL Solution:** One query. `query { user(id: 1) { name, posts { title } } }`.

### Pros & Cons
- **Pros:** Efficient for mobile (bandwidth), Strongly typed schema (Schema First Design), Great tooling (GraphiQL).
- **Cons:** Complex Caching (HTTP caching doesn't work well), Complexity (Resolvers needing optimizations like DataLoader to fix N+1), Security (Deep query attacks).

---

## 🗃️ 4. SQL Fundamentals (Quick Reference)

### Common Query Patterns
```sql
-- Filtering with WHERE
SELECT * FROM orders WHERE status = 'pending' AND total > 100;

-- Aggregation with GROUP BY + HAVING
SELECT customer_id, COUNT(*) as order_count
FROM orders
GROUP BY customer_id
HAVING COUNT(*) > 5;

-- JOINs
SELECT u.name, o.total
FROM users u
INNER JOIN orders o ON u.id = o.user_id;

-- Subqueries
SELECT * FROM products
WHERE price > (SELECT AVG(price) FROM products);
```

---

## 🔗 5. ORM: SQLAlchemy (Deep Dive)

### Core Concept
SQLAlchemy uses the **Data Mapper** pattern (vs Django's Active Record).
- **Engine:** Connection pool to the database.
- **Session:** Unit of work (transaction boundary).
- **Declarative Base:** Maps Python classes to tables.

```python
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String)

engine = create_engine('postgresql://user:pass@localhost/db')
Session = sessionmaker(bind=engine)
session = Session()

# Create
session.add(User(name="Sanket"))
session.commit()

# Query
users = session.query(User).filter(User.name == "Sanket").all()
```

---

## 📦 6. NoSQL Databases (Awareness)

### Redis
**Type:** In-memory Key-Value store.
**Use Cases:** Caching, Session storage, Rate limiting, Pub/Sub.
```python
import redis
r = redis.Redis()
r.set("user:1:name", "Sanket", ex=3600)  # Expires in 1 hour
r.get("user:1:name")  # b'Sanket'
```

### MongoDB
**Type:** Document-oriented NoSQL (JSON-like documents).
**Use Cases:** Flexible schemas, Prototyping, Content management.
```python
from pymongo import MongoClient
client = MongoClient()
db = client["mydb"]
db.users.insert_one({"name": "Sanket", "age": 30})
db.users.find_one({"name": "Sanket"})
```

---

## ❓ Interview Questions & Answers

**Q1: PUT vs PATCH?**
> **A:** `PUT` replaces the *entire* resource. If fields are missing in the payload, they should be nulled/removed. `PATCH` applies a *partial* update to only the fields specified.

**Q2: How do you handle pagination efficiently for millions of rows?**
> **A:** Avoid **Offset Pagination** (`LIMIT 10 OFFSET 1000000`) because the DB still scans 1,000,010 rows. Use **Cursor/Keyset Pagination** (`WHERE id > last_seen_id LIMIT 10`), which leverages the index on `id`.

**Q3: Explain "Dirty Read" vs "Phantom Read".**
> **A:**
> - **Dirty Read:** Reading uncommitted data from another transaction (that might roll back).
> - **Phantom Read:** A transaction reads a set of rows. Another transaction inserts a new row that matches the criteria. The first transaction re-runs the query and sees the "phantom" new row.

**Q4: When should you NOT use an index?**
> **A:**
> 1. On small tables (Seq scan is faster).
> 2. On columns with low cardinality (e.g., Boolean, Gender) - the index doesn't filter enough to justify the lookup overhead.
> 3. On columns frequently updated (index maintenance cost).

---

## 🔗 Recommended Resources

- **Guide:** [Best Practices for REST API Design](https://stackoverflow.blog/2020/03/02/best-practices-for-rest-api-design/)
- **Visuals:** [Use The Index, Luke! - SQL Tuning Guide](https://use-the-index-luke.com/)
- **Deep Dive:** [Database Isolation Levels Explained](https://vladmihalcea.com/a-beginners-guide-to-database-locking-and-the-lost-update-phenomena/)
