# Delete a Book

**Command:**

```python
from bookshelf.models import Book

# Retrieve and delete the book
book = Book.objects.get(title='Nineteen Eighty-Four')
book.delete()

#Expected Output:

python
Copy
Edit
# Book deleted successfully.
# Trying to retrieve it again will raise:
Book.DoesNotExist
```
