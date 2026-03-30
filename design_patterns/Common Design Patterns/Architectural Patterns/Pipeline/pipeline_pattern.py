"""
Pipeline Pattern — Real-World Example
========================================
Text Processing Pipeline that cleans and transforms raw HTML
content through a sequence of independent, reusable stages.

Stages
------
1. StripHTMLStage       — Remove all HTML tags
2. NormalizeWhitespaceStage — Collapse whitespace, trim
3. CensorStage          — Replace banned words with ***
4. MarkdownifyStage     — Wrap *bold* markers in <b> tags
5. TruncateStage        — Limit output to N characters + "..."
"""

from __future__ import annotations
import re
from abc import ABC, abstractmethod


# ── Stage Interface ─────────────────────────────────────────

class Stage(ABC):
    """A single transformation unit in the pipeline."""

    @abstractmethod
    def process(self, data: str) -> str:
        """Transform data and return the result."""


# ── Concrete Stages ─────────────────────────────────────────

class StripHTMLStage(Stage):
    """Remove all HTML tags from the input."""

    def process(self, data: str) -> str:
        cleaned = re.sub(r"<[^>]+>", "", data)
        print(f"  [StripHTML]       → {cleaned[:60]}...")
        return cleaned


class NormalizeWhitespaceStage(Stage):
    """Collapse consecutive whitespace into a single space and trim."""

    def process(self, data: str) -> str:
        cleaned = re.sub(r"\s+", " ", data).strip()
        print(f"  [NormalizeWS]     → {cleaned[:60]}...")
        return cleaned


class CensorStage(Stage):
    """Replace banned words with '***'."""

    def __init__(self, banned_words: list[str]):
        self._pattern = re.compile(
            "|".join(re.escape(w) for w in banned_words),
            re.IGNORECASE,
        )

    def process(self, data: str) -> str:
        censored = self._pattern.sub("***", data)
        print(f"  [Censor]          → {censored[:60]}...")
        return censored


class MarkdownifyStage(Stage):
    """Convert *bold* markers into <b>bold</b> HTML."""

    def process(self, data: str) -> str:
        converted = re.sub(r"\*(.+?)\*", r"<b>\1</b>", data)
        print(f"  [Markdownify]     → {converted[:60]}...")
        return converted


class TruncateStage(Stage):
    """Truncate output to max_length characters, append '...' if needed."""

    def __init__(self, max_length: int = 80):
        self._max = max_length

    def process(self, data: str) -> str:
        if len(data) <= self._max:
            print(f"  [Truncate({self._max})]   → {data}")
            return data
        truncated = data[: self._max] + "..."
        print(f"  [Truncate({self._max})]   → {truncated}")
        return truncated


# ── Pipeline ────────────────────────────────────────────────

class Pipeline:
    """Composes multiple stages; data flows through each in order."""

    def __init__(self):
        self._stages: list[Stage] = []

    def add_stage(self, stage: Stage) -> Pipeline:
        """Fluent API — returns self so you can chain calls."""
        self._stages.append(stage)
        return self

    def execute(self, data: str) -> str:
        result = data
        for stage in self._stages:
            result = stage.process(result)
        return result


# ── Demo ────────────────────────────────────────────────────

if __name__ == "__main__":
    raw_html = """
    <html>
        <body>
            <h1>Welcome to  the   Blog!</h1>
            <p>This is a *great* post about <b>Python</b>.
               Some spam content here.
               Visit our  site for  more   *awesome* tips.</p>
            <footer>Copyright 2024</footer>
        </body>
    </html>
    """

    banned = ["spam", "visit"]

    pipeline = (
        Pipeline()
        .add_stage(StripHTMLStage())
        .add_stage(NormalizeWhitespaceStage())
        .add_stage(CensorStage(banned))
        .add_stage(MarkdownifyStage())
        .add_stage(TruncateStage(100))
    )

    print("=== Text Processing Pipeline ===\n")
    print(f"  Input ({len(raw_html)} chars):\n    {raw_html.strip()[:80]}...\n")
    result = pipeline.execute(raw_html)
    print(f"\n  Final output:\n    {result}")

    # ── Second run: different pipeline config ──

    print("\n\n=== Minimal Pipeline (strip + truncate only) ===\n")
    mini = (
        Pipeline()
        .add_stage(StripHTMLStage())
        .add_stage(TruncateStage(50))
    )
    result2 = mini.execute(raw_html)
    print(f"\n  Final output:\n    {result2}")
