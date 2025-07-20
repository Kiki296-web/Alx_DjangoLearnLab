# Retrieve a Book

**Command:**

```python
from bookshelf.models import Book

# Retrieve the book by title
book = Book.objects.get(title='1984')
print(book.title)
print(book.author)
print(book.published_year)

#Expected Output:

1984
George Orwell
1949
```
