from rest_framework import serializers
from .models import Author, Book
import datetime

# BookSerializer is responsible for converting Book instances to/from JSON.
# It includes all model fields and validates publication_year to ensure it is not in the future.
class BookSerializer(serializers.ModelSerializer):

    class Meta:
        model = Book
        fields = '__all__'  # Includes: id, title, publication_year, author

    def validate_publication_year(self, value):
        """
        Ensure that the publication year is not in the future.
        """
        current_year = datetime.datetime.now().year
        if value > current_year:
            raise serializers.ValidationError("Publication year cannot be in the future.")
        return value

# AuthorSerializer serializes the Author model, including the name and related books.
# It uses BookSerializer as a nested serializer to display each author's books.
class AuthorSerializer(serializers.ModelSerializer):
    books = BookSerializer(many=True, read_only=True)  # Uses the 'related_name' from the Book model to access related books.

    class Meta:
        model = Author
        fields = ['id', 'name', 'books']

"""
Relationship Handling:
- Each Book has a ForeignKey to Author, creating a one-to-many relationship.
- The related_name='books' in the Book model allows reverse access from Author to Book.
- In AuthorSerializer, the 'books' field uses BookSerializer to display the author's books as nested data.
- This nested approach supports read-only viewing of related books in API responses.
"""
