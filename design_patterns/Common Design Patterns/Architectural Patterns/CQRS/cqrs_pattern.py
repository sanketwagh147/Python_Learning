"""
CQRS Pattern — Real-World Example
===================================
Blog Post system with separate command and query paths.

Commands (write): CreatePost, PublishPost, DeletePost
Queries  (read):  GetPost, ListPosts

The write side validates and stores rich domain objects.
The read side returns lightweight view models (PostSummary).
They could use entirely different databases in production.
"""

from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime


# ── Domain Model (Write Side) ──────────────────────────────

@dataclass
class BlogPost:
    id: int
    title: str
    content: str
    author: str
    created_at: datetime = field(default_factory=datetime.now)
    published: bool = False


# ── View Model (Read Side) ─────────────────────────────────

@dataclass
class PostSummary:
    """Lightweight read-optimized view — no content body."""
    id: int
    title: str
    author: str
    published: bool


# ── Commands ────────────────────────────────────────────────

@dataclass
class CreatePostCommand:
    title: str
    content: str
    author: str


@dataclass
class PublishPostCommand:
    post_id: int


@dataclass
class DeletePostCommand:
    post_id: int


# ── Queries ─────────────────────────────────────────────────

@dataclass
class GetPostQuery:
    post_id: int


@dataclass
class ListPostsQuery:
    author: str | None = None


# ── Storage (shared for demo; separate DBs in production) ──

class PostStore:
    def __init__(self):
        self._posts: dict[int, BlogPost] = {}
        self._next_id = 1

    def save(self, post: BlogPost) -> BlogPost:
        if post.id == 0:
            post.id = self._next_id
            self._next_id += 1
        self._posts[post.id] = post
        return post

    def get(self, post_id: int) -> BlogPost | None:
        return self._posts.get(post_id)

    def delete(self, post_id: int) -> bool:
        return self._posts.pop(post_id, None) is not None

    def all(self) -> list[BlogPost]:
        return list(self._posts.values())


# ── Command Handler (Write Side) ───────────────────────────

class PostCommandHandler:
    """Handles all write operations.
    Validates and mutates state."""

    def __init__(self, store: PostStore):
        self._store = store

    def handle_create(self, cmd: CreatePostCommand) -> int:
        post = BlogPost(
            id=0, title=cmd.title,
            content=cmd.content, author=cmd.author,
        )
        saved = self._store.save(post)
        print(f"  [WRITE] Created post #{saved.id}: '{saved.title}'")
        return saved.id

    def handle_publish(self, cmd: PublishPostCommand) -> bool:
        post = self._store.get(cmd.post_id)
        if not post:
            print(f"  [WRITE] Post #{cmd.post_id} not found")
            return False
        post.published = True
        self._store.save(post)
        print(f"  [WRITE] Published post #{post.id}")
        return True

    def handle_delete(self, cmd: DeletePostCommand) -> bool:
        deleted = self._store.delete(cmd.post_id)
        label = "Deleted" if deleted else "Not found"
        print(f"  [WRITE] {label} post #{cmd.post_id}")
        return deleted


# ── Query Handler (Read Side) ──────────────────────────────

class PostQueryHandler:
    """Handles all read operations.
    Returns lightweight view models, never mutates state."""

    def __init__(self, store: PostStore):
        self._store = store

    def handle_get(self, query: GetPostQuery) -> BlogPost | None:
        return self._store.get(query.post_id)

    def handle_list(self, query: ListPostsQuery) -> list[PostSummary]:
        posts = self._store.all()
        if query.author:
            posts = [p for p in posts if p.author == query.author]
        return [
            PostSummary(
                id=p.id, title=p.title,
                author=p.author, published=p.published,
            )
            for p in posts
        ]


# ── Demo ────────────────────────────────────────────────────

if __name__ == "__main__":
    store = PostStore()
    commands = PostCommandHandler(store)
    queries = PostQueryHandler(store)

    print("=== COMMANDS (Write Side) ===")
    id1 = commands.handle_create(
        CreatePostCommand("CQRS Explained", "Full article...", "Alice"))
    id2 = commands.handle_create(
        CreatePostCommand("Saga Pattern", "Full article...", "Bob"))
    id3 = commands.handle_create(
        CreatePostCommand("Python Tips", "Full article...", "Alice"))
    commands.handle_publish(PublishPostCommand(id1))
    commands.handle_publish(PublishPostCommand(id2))

    print("\n=== QUERIES (Read Side) ===")
    print("  All posts:")
    for s in queries.handle_list(ListPostsQuery()):
        status = "published" if s.published else "draft"
        print(f"    #{s.id} '{s.title}' by {s.author} [{status}]")

    print("\n  Alice's posts:")
    for s in queries.handle_list(ListPostsQuery(author="Alice")):
        status = "published" if s.published else "draft"
        print(f"    #{s.id} '{s.title}' [{status}]")

    print("\n  Single post lookup:")
    post = queries.handle_get(GetPostQuery(id1))
    if post:
        print(f"    #{post.id} '{post.title}' — {post.content[:30]}...")

    print("\n=== DELETE (Write) then READ ===")
    commands.handle_delete(DeletePostCommand(id2))
    print(f"  Post #{id2} after delete: {queries.handle_get(GetPostQuery(id2))}")
