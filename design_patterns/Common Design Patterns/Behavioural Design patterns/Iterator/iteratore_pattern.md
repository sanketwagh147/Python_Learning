# Iterator Pattern

Iterator is a behavioral design pattern that lets you traverse elements of a collection without exposing its underlying representation (list, stack, tree, etc.)

## Why Use the Iterator Pattern?

✅ Encapsulation – Hides the internal structure of the collection.  
✅ Consistent Interface – Provides a common way to iterate over different collections.  
✅ Multiple Iterators – Allows different types of iteration (e.g., forward, reverse).a

## Example

```python
class BookCollection:
    def __init__(self):
        self.books = []

    def add_book(self, book):
        self.books.append(book)

    def __iter__(self):
        for book in self.books:
            yield book  # Generator-based iteration

# Usage
library = BookCollection()
library.add_book("Design Patterns")
library.add_book("Refactoring")

for book in library:
    print(book)  # Output: Design Patterns, Refactoring

```

## Example 2

When scraping websites, you don’t want to store all pages in memory at once. Instead, you can iterate over each page using a generator.

```python
import requests
from bs4 import BeautifulSoup

class WebPageIterator:
    def __init__(self, urls):
        self.urls = urls
        self.index = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.index >= len(self.urls):
            raise StopIteration
        url = self.urls[self.index]
        self.index += 1
        response = requests.get(url)
        if response.status_code != 200:
            raise StopIteration
        return BeautifulSoup(response.text, "html.parser").title.string

# List of web pages to scrape
pages = WebPageIterator(["https://www.python.org", "https://www.wikipedia.org"])

for title in pages:
    print(title)  # Output: "Welcome to Python.org", "Wikipedia"
```
