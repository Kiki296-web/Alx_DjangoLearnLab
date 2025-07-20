from django.shortcuts import render
from django.views.generic.detail import DetailView

from .models import Book
from .models import Library

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
        
        try:
            books = library.books.all() 
        except AttributeError:
            books = library.book_set.all()

        context["books"] = books
        return context
  
