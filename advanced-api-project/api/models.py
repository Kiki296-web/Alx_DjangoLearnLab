from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
import datetime

# Author model represents a book author with a name.
class Author(models.Model):
    name = models.CharField(max_length=100)  # Stores the author's full name.

    def __str__(self):
        return self.name  # Returns the author's name when printed or displayed in admin.

# Book model represents a book written by an author.
class Book(models.Model):
    title = models.CharField(max_length=200)  # Title of the book.
    publication_year = models.IntegerField(
        validators=[
            MinValueValidator(1400),
            MaxValueValidator(datetime.datetime.now().year)
        ]
    )  # Stores the year the book was published. Limited between 1400 and current year.
    
    author = models.ForeignKey(
        Author,
        on_delete=models.CASCADE,
        related_name='books'  # Enables reverse lookup from Author to all their books.
    )

    def __str__(self):
        return self.title  # Returns the book title when printed or shown in admin.

