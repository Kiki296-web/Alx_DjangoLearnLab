# Update a Book

**Command:**

```python
from bookshelf.models import Book

# Retrieve and update the book title
book = Book.objects.get(title='1984')
book.title = 'Nineteen Eighty-Four'
book.save()

#Expected Output:

python
Copy
Edit
# Book title is updated successfully.
# Output from print(book.title):
Nineteen Eighty-Four
```
