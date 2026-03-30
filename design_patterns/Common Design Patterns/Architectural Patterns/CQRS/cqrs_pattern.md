# CQRS — Command Query Responsibility Segregation

Separates **read operations** (Queries) from **write operations** (Commands) into different models/paths.

## Key Concepts

- **Command**: An intent to change state (create, update, delete). Returns nothing or just a status.
- **Query**: A request for data. Never modifies state.
- **Command Handler**: Processes a command, writes to the write store.
- **Query Handler**: Reads from the read store (can be a separate optimized DB/cache).

## Why Separate Reads and Writes?

| Concern | Reads | Writes |
|---|---|---|
| **Optimization** | Denormalized, cached, fast | Normalized, transactional, consistent |
| **Scaling** | Scale read replicas independently | Scale writes separately |
| **Model** | Flat DTOs / view models | Rich domain objects with validation |

## Structure

```
Client
  │
  ├── Command ──→ CommandHandler ──→ Write Store (DB)
  │
  └── Query ───→ QueryHandler ───→ Read Store (cache/view)
```

In simple implementations both handlers share the same DB.
In production, the read store could be a Redis cache,
Elasticsearch index, or a materialized view — optimized
purely for read performance.

## Example

```python
# Commands (write side)
@dataclass
class CreatePostCommand:
    title: str
    content: str
    author: str

class PostCommandHandler:
    def handle_create(self, cmd: CreatePostCommand) -> int:
        post = BlogPost(title=cmd.title, ...)
        self._store.save(post)
        return post.id

# Queries (read side)
@dataclass
class ListPostsQuery:
    author: str | None = None

class PostQueryHandler:
    def handle_list(self, query: ListPostsQuery) -> list[PostSummary]:
        posts = self._store.all()
        return [PostSummary(...) for p in posts]
```

## Relationship to Other Patterns

- **Event Sourcing** — often combined with CQRS; events go to write side, projections to read side
- **Repository** — each side (read/write) can have its own repository
- **Mediator** — commands/queries can be dispatched through a mediator

## When to Use

✅ Read and write workloads have very different scaling needs  
✅ Read models are heavily denormalized / cached  
✅ Complex domain where write validation differs from read shape  
✅ You want independent optimization of read vs write paths  

## When NOT to Use

❌ Simple CRUD where reads/writes are the same shape  
❌ Small apps where the extra complexity isn't justified  
❌ Teams unfamiliar with the pattern (high learning curve)
