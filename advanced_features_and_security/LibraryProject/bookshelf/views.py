from django.contrib.auth.decorators import permission_required
from django.shortcuts import render
from bookshelf.models import Book
from django.contrib.auth import forms
from .forms import ExampleForm

@permission_required('bookshelf.can_view', raise_exception=True)
def book_list(request):
    books = Book.objects.all()
    return render(request, 'bookshelf/book_list.html', {'books': books})

def search_books(request):
    form = ExampleForm(request.GET or None)
    results = []

    if form.is_valid():
        query = form.cleaned_data['query']
        results = Book.objects.filter(title__icontains=query)

    return render(request, 'books/search_results.html', {'form': form, 'results': results})
