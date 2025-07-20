from django.contrib import admin
from django.urls import path
from . import views

app_name = "relationship_app"

urlpatterns = [
    path("books/", views.book_list_view, name="book-list"),
    path("libraries/<int:pk>/", views.LibraryDetailView.as_view(), name="library-detail"),
    
]