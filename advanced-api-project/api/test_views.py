# api/test_views.py
from django.urls import reverse, NoReverseMatch
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from .models import Author, Book


def _url_or_path(name, fallback):
    """
    Helper: try to reverse a named URL, otherwise return fallback path.
    This keeps tests robust if your project's URL names differ slightly.
    """
    try:
        return reverse(name)
    except NoReverseMatch:
        return fallback


class BookAPITests(APITestCase):
    def setUp(self):
        # Create a test user for authenticated endpoints
        self.user = User.objects.create_user(username="tester", password="pass1234")

        # Create authors
        self.author1 = Author.objects.create(name="Author One")
        self.author2 = Author.objects.create(name="Author Two")

        # Create books
        self.book1 = Book.objects.create(title="Alpha Book", publication_year=2000, author=self.author1)
        self.book2 = Book.objects.create(title="Beta Book", publication_year=2010, author=self.author1)
        self.book3 = Book.objects.create(title="Gamma Book", publication_year=2020, author=self.author2)

        # Clients
        self.client = APIClient()
        self.auth_client = APIClient()
        self.auth_client.force_authenticate(user=self.user)

        # Endpoints (try named URLs first; fall back to literal paths)
        # These names should match your api/urls.py name=... values.
        self.books_list_url = _url_or_path('book-list', '/api/books/')
        self.book_detail_url = lambda pk: _url_or_path('book-detail', f'/api/books/{pk}/')
        self.book_create_url = _url_or_path('book-create', '/api/books/create/')
        self.book_update_url = lambda pk: _url_or_path('book-update', f'/api/books/update/{pk}/')
        self.book_delete_url = lambda pk: _url_or_path('book-delete', f'/api/books/delete/{pk}/')

    # -------------------------
    # Basic CRUD tests
    # -------------------------
    def test_list_books_public(self):
        """GET /books/ should return 200 and list all books (public)."""
        resp = self.client.get(self.books_list_url)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        # we expect at least the three books we created
        titles = [item['title'] for item in resp.json()]
        self.assertIn(self.book1.title, titles)
        self.assertIn(self.book2.title, titles)
        self.assertIn(self.book3.title, titles)

    def test_retrieve_book_detail_public(self):
        """GET /books/<pk>/ should return single book data."""
        resp = self.client.get(self.book_detail_url(self.book2.pk))
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.json()
        self.assertEqual(data['title'], self.book2.title)
        self.assertEqual(data['publication_year'], self.book2.publication_year)

    def test_create_book_requires_authentication(self):
        """POST to create book should be forbidden for anonymous users."""
        payload = {
            "title": "New Book",
            "publication_year": 2021,
            "author": self.author1.pk
        }
        resp = self.client.post(self.book_create_url, payload, format='json')
        # Expect 401 Unauthorized (or 403 depending on permission setup)
        self.assertIn(resp.status_code, (status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN))

    def test_create_book_authenticated(self):
        """Authenticated user can create a book."""
        payload = {
            "title": "New Auth Book",
            "publication_year": 2021,
            "author": self.author1.pk
        }
        resp = self.auth_client.post(self.book_create_url, payload, format='json')
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.filter(title="New Auth Book").count(), 1)

    def test_update_book_requires_authentication(self):
        """Anonymous user cannot update a book (should be 401/403)."""
        payload = {"title": "Modified Title"}
        resp = self.client.patch(self.book_update_url(self.book1.pk), payload, format='json')
        self.assertIn(resp.status_code, (status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN))

    def test_update_book_authenticated(self):
        """Authenticated user can update a book."""
        payload = {"title": "Alpha Book (Updated)"}
        resp = self.auth_client.patch(self.book_update_url(self.book1.pk), payload, format='json')
        # UpdateAPIView usually returns 200 OK
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.book1.refresh_from_db()
        self.assertEqual(self.book1.title, "Alpha Book (Updated)")

    def test_delete_book_requires_authentication(self):
        """Anonymous user cannot delete a book."""
        resp = self.client.delete(self.book_delete_url(self.book3.pk))
        self.assertIn(resp.status_code, (status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN))

    def test_delete_book_authenticated(self):
        """Authenticated user can delete a book."""
        resp = self.auth_client.delete(self.book_delete_url(self.book3.pk))
        # DestroyAPIView usually returns 204 NO CONTENT
        self.assertIn(resp.status_code, (status.HTTP_204_NO_CONTENT, status.HTTP_200_OK))
        self.assertFalse(Book.objects.filter(pk=self.book3.pk).exists())

    # -------------------------
    # Filtering / Search / Ordering
    # -------------------------
    def test_filter_by_publication_year(self):
        """Filtering: ?publication_year=2010 should return the matching book(s)."""
        resp = self.client.get(self.books_list_url, {'publication_year': 2010})
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.json()
        self.assertTrue(all(item['publication_year'] == 2010 for item in data))
        self.assertEqual(len(data), 1)

    def test_filter_by_author(self):
        """Filtering: ?author=<pk> returns books by that author."""
        resp = self.client.get(self.books_list_url, {'author': self.author1.pk})
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.json()
        # author field may be returned as ID or nested object depending on serializer;
        # ensure every returned book has author equal to author1.pk in one of the available representations.
        for item in data:
            if isinstance(item.get('author'), dict):
                self.assertEqual(item['author'].get('id'), self.author1.pk)
            else:
                self.assertEqual(item.get('author'), self.author1.pk)

    def test_search_title_or_author(self):
        """Search: ?search=Gamma should return the Gamma Book."""
        resp = self.client.get(self.books_list_url, {'search': 'Gamma'})
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        titles = [b['title'] for b in resp.json()]
        self.assertIn(self.book3.title, titles)

        # Also test searching by author name (partial)
        resp2 = self.client.get(self.books_list_url, {'search': 'Author One'})
        self.assertEqual(resp2.status_code, status.HTTP_200_OK)
        titles2 = [b['title'] for b in resp2.json()]
        # Author One has book1 and book2
        self.assertIn(self.book1.title, titles2)
        self.assertIn(self.book2.title, titles2)

    def test_ordering_by_publication_year(self):
        """Ordering: ?ordering=publication_year should order ascending."""
        resp = self.client.get(self.books_list_url, {'ordering': 'publication_year'})
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.json()
        years = [item['publication_year'] for item in data]
        self.assertEqual(years, sorted(years))

        # Descending
        resp2 = self.client.get(self.books_list_url, {'ordering': '-publication_year'})
        data2 = resp2.json()
        years2 = [item['publication_year'] for item in data2]
        self.assertEqual(years2, sorted(years2, reverse=True))
