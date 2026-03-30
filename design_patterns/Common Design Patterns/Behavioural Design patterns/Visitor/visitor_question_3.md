# Visitor Pattern — Question 3 (Hard)

## Problem: Document Export System with Composite + Visitor

A document has a composite tree structure (sections, paragraphs, tables, images). Multiple export visitors render the tree into different formats WITHOUT modifying the document classes.

### Requirements

#### Document Nodes (Composite)
```python
class DocumentNode(ABC):
    def accept(self, visitor: DocumentVisitor): ...

class Document(DocumentNode):         # root, contains sections
class Section(DocumentNode):          # title + children (paragraphs, tables, subsections)
class Paragraph(DocumentNode):        # text content with inline formatting
class Table(DocumentNode):            # headers + rows
class Image(DocumentNode):            # src, alt_text, width, height
class CodeBlock(DocumentNode):        # code + language
```

#### Visitors
1. **HTMLExportVisitor**: renders to HTML with proper tags
2. **MarkdownExportVisitor**: renders to Markdown
3. **LaTeXExportVisitor**: renders to LaTeX
4. **TableOfContentsVisitor**: extracts section titles + nesting into a TOC
5. **WordCountVisitor**: counts words in paragraphs + code blocks
6. **LinkExtractorVisitor**: finds all URLs in paragraphs

#### Sample Document
```
Document: "Design Patterns Guide"
├── Section: "Introduction"
│   ├── Paragraph: "Design patterns are..."
│   └── Image: "patterns-overview.png"
├── Section: "Creational Patterns"
│   ├── Paragraph: "These patterns deal with..."
│   ├── Table: [["Pattern", "Use Case"], ["Singleton", "Global state"], ...]
│   ├── CodeBlock: (Python, "class Singleton: ...")
│   └── Section: "Factory Method"
│       └── Paragraph: "The factory method..."
└── Section: "Summary"
    └── Paragraph: "In conclusion, visit https://refactoring.guru..."
```

### Expected Usage

```python
doc = build_sample_document()

# Export to HTML
html_visitor = HTMLExportVisitor()
doc.accept(html_visitor)
print(html_visitor.output())
# → <html><body><h1>Design Patterns Guide</h1>
# → <h2>Introduction</h2><p>Design patterns are...</p>
# → <img src="patterns-overview.png" alt="...">
# → ...

# Table of Contents
toc = TableOfContentsVisitor()
doc.accept(toc)
print(toc.output())
# → 1. Introduction
# → 2. Creational Patterns
# →    2.1. Factory Method
# → 3. Summary

# Word count
wc = WordCountVisitor()
doc.accept(wc)
print(wc.total_words())  # → 42

# Link extraction
links = LinkExtractorVisitor()
doc.accept(links)
print(links.urls())  # → ["https://refactoring.guru"]
```

### Constraints

- Document tree is a Composite — sections contain other sections recursively.
- Each visitor traverses the entire tree via `accept()` chain.
- `HTMLExportVisitor` must handle nested sections as `<h2>`, `<h3>`, `<h4>` etc. based on depth.
- `TableOfContentsVisitor` must track section numbering (1, 1.1, 1.2, 2, etc.).
- Adding a new visitor (e.g., PDFExportVisitor) requires ZERO changes to document classes.
- Adding a new node type (e.g., `Footnote`) requires updating ALL visitors.

### Think About

- This is the classic Visitor trade-off: easy to add operations, hard to add node types. When is this the right choice?
- How does Python's `ast.NodeVisitor` implement this pattern?
- Could you use `@singledispatch` instead of the traditional Visitor? What are the trade-offs?
