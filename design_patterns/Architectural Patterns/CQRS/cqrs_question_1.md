# CQRS Pattern — Question 1 (Easy)

## Problem: Blog Post Read/Write Separation

Separate the read and write operations for a blog post system into distinct models.

### Requirements

#### Write Side (Commands)
```python
class CreatePostCommand:
    title: str
    content: str
    author: str

class UpdatePostCommand:
    post_id: str
    title: str | None
    content: str | None

class CommandHandler:
    def handle_create(self, cmd: CreatePostCommand) -> str: ...  # returns post_id
    def handle_update(self, cmd: UpdatePostCommand) -> None: ...
```

#### Read Side (Queries)
```python
class PostSummaryQuery:
    """Returns list of posts with title + author only (no content)."""

class PostDetailQuery:
    post_id: str
    """Returns full post with title, content, author, created_at."""

class QueryHandler:
    def get_summaries(self) -> list[PostSummary]: ...
    def get_detail(self, query: PostDetailQuery) -> PostDetail: ...
```

### Expected Usage

```python
cmd_handler = CommandHandler(store)
query_handler = QueryHandler(store)

post_id = cmd_handler.handle_create(CreatePostCommand("Hello", "World content", "Alice"))

summaries = query_handler.get_summaries()
# → [PostSummary(id="...", title="Hello", author="Alice")]

detail = query_handler.get_detail(PostDetailQuery(post_id))
# → PostDetail(title="Hello", content="World content", author="Alice", created_at=...)
```

### Constraints

- Commands do NOT return query data (only confirmation/ID).
- Queries are STRICTLY read-only — never modify state.
- Both use the same underlying store (simple CQRS — separate models, shared store).
