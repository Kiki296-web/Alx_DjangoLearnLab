#Creating a new book

**Command:**

````python
from bookshelf.models import Book

new_book = Book (title = '1984', author = 'George Orwell', publication_year ='1949')
new_book.save()

#Printing the output

print(new_book)
# Output:
<Book: 1984>


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
````
