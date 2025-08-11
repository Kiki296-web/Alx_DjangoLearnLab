# api/test_views.py
from django.urls import reverse, NoReverseMatch
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from .models import Author, Book
from django.test import TestCase


class BookAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        
        # Create a test user
        self.user = User.objects.create_user(username='testuser', password='testpass')

        # Login the test user
        self.client.login(username='testuser', password='testpass')
        
        self.book = Book.objects.create(
            title="Test Book",
            author="Test Author",
            publication_year=2024
        )
        self.valid_payload = {
            "title": "New Book",
            "author": "New Author",
            "publication_year": 2025
        }
        self.update_payload = {
            "title": "Updated Book",
            "author": "Updated Author",
            "publication_year": 2023
        }

    def test_create_book(self):
        response = self.client.post('/books/create/', self.valid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("title", response.data)
        self.assertEqual(response.data["title"], self.valid_payload["title"])

    def test_get_books_list(self):
        response = self.client.get('/books/', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, list)  # Check if the response is a list

    def test_update_book(self):
        response = self.client.put(f'/books/update/{self.book.id}/', self.update_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], self.update_payload["title"])

    def test_delete_book(self):
        response = self.client.delete(f'/books/delete/{self.book.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
