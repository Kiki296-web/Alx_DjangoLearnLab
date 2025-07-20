from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.views.generic import DetailView
from .models import Book, Library

# Create your views here.
def book_list_view(request):
    books = Book.objects.all() 
    return render(request, "relationship_app/list_books.html", {"books": books})
    
# Class-Based View: show a specific Library + its books
class LibraryDetailView(DetailView):
    model = Library
    template_name = "relationship_app/library_detail.html"  
    context_object_name = "library" 
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        library = self.object


        if hasattr(library, "books"):
            books_qs = library.books.all()
        elif hasattr(library, "book_set"):  
            books_qs = library.book_set.all()
        else:
            books_qs = Book.objects.none()

    
        books_qs = books_qs.select_related("author")

        context["books"] = books_qs
        return context
  
