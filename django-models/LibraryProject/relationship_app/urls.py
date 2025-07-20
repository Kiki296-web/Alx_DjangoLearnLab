from .views import list_books, LibraryDetailView
from django.contrib.auth.views import LoginView, LogoutView
from . import admin_view, librarian_view, member_view
from django.urls import path
from . import views


app_name = "relationship_app"

urlpatterns = [
    path("books/", views.book_list_view, name="book-list"),
    path("libraries/<int:pk>/", views.LibraryDetailView.as_view(), name="library-detail"),
    path('login/', LoginView.as_view(template_name='relationship_app/login.html'), name='login'),
    path('logout/', LogoutView.as_view(template_name='relationship_app/logout.html'), name='logout'),
    path('register/', views.register, name='register'),
    path('admin-dashboard/', admin_view.admin_view, name='admin_view'),
    path('librarian-dashboard/', librarian_view.librarian_view, name='librarian_view'),
    path('member-dashboard/', member_view.member_view, name='member_view'),
    path('add_book/', views.add_book, name='add_book'),
    path('edit_book/<int:book_id>/', views.edit_book, name='edit_book'),
    path('delete_book/<int:book_id>/', views.delete_book, name='delete_book'),
]