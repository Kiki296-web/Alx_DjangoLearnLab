from .views import list_books, LibraryDetailView
from django.urls import path
from . import views
from .views import CustomLoginView, CustomLogoutView, RegisterView

app_name = "relationship_app"

urlpatterns = [
    path("books/", views.book_list_view, name="book-list"),
    path("libraries/<int:pk>/", views.LibraryDetailView.as_view(), name="library-detail"),
     path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
]