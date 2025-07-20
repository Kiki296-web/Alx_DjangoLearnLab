from django.shortcuts import render, redirect
from django.views.generic.detail import DetailView

from .models import Book
from .models import Library

from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.urls import reverse_lazy
from django.views import View

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
  
class CustomLoginView(LoginView):
    template_name = 'relationship_app/login.html'

class CustomLogoutView(LogoutView):
    template_name = 'relationship_app/logout.html'

class RegisterView(View):
    def get(self, request):
        form = UserCreationForm()
        return render(request, 'relationship_app/register.html', {'form': form})
    
    def post(self, request):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')  # Change 'home' to your landing page URL name
        return render(request, 'relationship_app/register.html', {'form': form})