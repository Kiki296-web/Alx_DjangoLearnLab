#Creating a new book

**Command:**

```python
from bookshelf.models import Book

new_book = Book (title = '1984', author = 'George Orwell', publication_year ='1949')
new_book.save()

#Printing the output

print(new_book)
# Output:
<Book: 1984>
```
