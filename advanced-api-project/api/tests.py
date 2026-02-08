"""
Unit tests for Book API endpoints.
Tests CRUD operations, filtering, permissions, and authentication.
"""
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APIClient
from .models import Author, Book
import json

class BookAPITests(TestCase):
    """Test suite for Book API endpoints."""
    
    def setUp(self):
        """Set up test data and client."""
        # Create test users
        self.normal_user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            email='user@test.com'
        )
        self.admin_user = User.objects.create_superuser(
            username='admin',
            password='adminpass123',
            email='admin@test.com'
        )
        
        # Create test authors
        self.author1 = Author.objects.create(name='J.K. Rowling')
        self.author2 = Author.objects.create(name='George Orwell')
        
        # Create test books
        self.book1 = Book.objects.create(
            title='Harry Potter and the Philosopher\'s Stone',
            author=self.author1,
            publication_year=1997
        )
        self.book2 = Book.objects.create(
            title='1984',
            author=self.author2,
            publication_year=1949
        )
        self.book3 = Book.objects.create(
            title='Animal Farm',
            author=self.author2,
            publication_year=1945
        )
        
        # Initialize API client
        self.client = APIClient()
    
    # ==================== LIST VIEW TESTS ====================
    
    def test_list_books_unauthenticated(self):
        """Test that anyone can list books (AllowAny permission)."""
        url = reverse('book-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)
        self.assertEqual(response.data[0]['title'], self.book1.title)
    
    def test_filter_books_by_author(self):
        """Test filtering books by author ID."""
        url = reverse('book-list')
        response = self.client.get(url, {'author': self.author2.id})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)  # Should return 2 books by author2
        self.assertEqual(response.data[0]['author'], self.author2.id)
    
    def test_filter_books_by_publication_year(self):
        """Test filtering books by publication year."""
        url = reverse('book-list')
        response = self.client.get(url, {'publication_year': 1997})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['publication_year'], 1997)
    
    def test_filter_books_by_year_range(self):
        """Test custom filtering by year range."""
        url = reverse('book-list')
        response = self.client.get(url, {'min_year': 1940, 'max_year': 1950})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)  # 1984 and Animal Farm
    
    def test_search_books_by_title(self):
        """Test searching books by title."""
        url = reverse('book-list')
        response = self.client.get(url, {'search': 'Harry'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertIn('Harry', response.data[0]['title'])
    
    def test_search_books_by_author_name(self):
        """Test searching books by author name."""
        url = reverse('book-list')
        response = self.client.get(url, {'search': 'Orwell'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)  # Both Orwell books
    
    def test_order_books_by_title(self):
        """Test ordering books by title."""
        url = reverse('book-list')
        response = self.client.get(url, {'ordering': 'title'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Should be alphabetical: 1984, Animal Farm, Harry Potter
        self.assertEqual(response.data[0]['title'], '1984')
        self.assertEqual(response.data[1]['title'], 'Animal Farm')
    
    def test_order_books_by_publication_year_desc(self):
        """Test ordering books by publication year (descending)."""
        url = reverse('book-list')
        response = self.client.get(url, {'ordering': '-publication_year'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['publication_year'], 1997)  # Most recent
    
    # ==================== DETAIL VIEW TESTS ====================
    
    def test_retrieve_book_unauthenticated(self):
        """Test that anyone can retrieve a single book."""
        url = reverse('book-detail', kwargs={'pk': self.book1.id})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], self.book1.title)
        self.assertEqual(response.data['author'], self.author1.id)
    
    def test_retrieve_nonexistent_book(self):
        """Test retrieving a book that doesn't exist."""
        url = reverse('book-detail', kwargs={'pk': 999})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    # ==================== CREATE VIEW TESTS ====================
    
    def test_create_book_unauthenticated(self):
        """Test that unauthenticated users cannot create books."""
        url = reverse('book-create')
        data = {
            'title': 'New Book',
            'author': self.author1.id,
            'publication_year': 2024
        }
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_create_book_authenticated(self):
        """Test that authenticated users can create books."""
        self.client.force_authenticate(user=self.normal_user)
        url = reverse('book-create')
        data = {
            'title': 'The Great Gatsby',
            'author': self.author1.id,
            'publication_year': 1925
        }
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['status'], 'success')
        self.assertEqual(response.data['data']['title'], 'The Great Gatsby')
        self.assertEqual(Book.objects.count(), 4)  # 3 original + 1 new
    
    def test_create_book_with_future_publication_year(self):
        """Test validation for future publication year."""
        self.client.force_authenticate(user=self.normal_user)
        url = reverse('book-create')
        data = {
            'title': 'Future Book',
            'author': self.author1.id,
            'publication_year': 2030  # Future year should fail validation
        }
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('publication_year', response.data)
    
    def test_create_book_with_invalid_data(self):
        """Test creating a book with missing required fields."""
        self.client.force_authenticate(user=self.normal_user)
        url = reverse('book-create')
        data = {
            'title': '',  # Empty title should fail
            'author': self.author1.id,
            'publication_year': 2000
        }
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('title', response.data)
    
    # ==================== UPDATE VIEW TESTS ====================
    
    def test_update_book_unauthenticated(self):
        """Test that unauthenticated users cannot update books."""
        url = reverse('book-update', kwargs={'pk': self.book1.id})
        data = {'title': 'Updated Title'}
        response = self.client.put(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_update_book_authenticated(self):
        """Test that authenticated users can update books."""
        self.client.force_authenticate(user=self.normal_user)
        url = reverse('book-update', kwargs={'pk': self.book1.id})
        data = {
            'title': 'Harry Potter - Updated',
            'author': self.author1.id,
            'publication_year': 1997
        }
        response = self.client.put(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], 'success')
        self.book1.refresh_from_db()
        self.assertEqual(self.book1.title, 'Harry Potter - Updated')
    
    def test_partial_update_book(self):
        """Test partial update (PATCH) of a book."""
        self.client.force_authenticate(user=self.normal_user)
        url = reverse('book-update', kwargs={'pk': self.book1.id})
        data = {'title': 'Partially Updated'}
        response = self.client.patch(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book1.refresh_from_db()
        self.assertEqual(self.book1.title, 'Partially Updated')
    
    # ==================== DELETE VIEW TESTS ====================
    
    def test_delete_book_unauthenticated(self):
        """Test that unauthenticated users cannot delete books."""
        url = reverse('book-delete', kwargs={'pk': self.book1.id})
        response = self.client.delete(url)
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_delete_book_non_admin(self):
        """Test that non-admin users cannot delete books."""
        self.client.force_authenticate(user=self.normal_user)
        url = reverse('book-delete', kwargs={'pk': self.book1.id})
        response = self.client.delete(url)
        
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_delete_book_admin(self):
        """Test that admin users can delete books."""
        self.client.force_authenticate(user=self.admin_user)
        url = reverse('book-delete', kwargs={'pk': self.book1.id})
        response = self.client.delete(url)
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Book.objects.count(), 2)  # Should be 2 books left
        self.assertFalse(Book.objects.filter(id=self.book1.id).exists())
    
    # ==================== PERMISSIONS TESTS ====================
    
    def test_permissions_summary(self):
        """Test that permissions are correctly applied."""
        # List and detail - should work for anyone
        list_response = self.client.get(reverse('book-list'))
        detail_response = self.client.get(
            reverse('book-detail', kwargs={'pk': self.book1.id})
        )
        
        # Create - should require authentication
        create_response = self.client.post(reverse('book-create'), {}, format='json')
        
        # Update - should require authentication
        update_response = self.client.put(
            reverse('book-update', kwargs={'pk': self.book1.id}), 
            {}, 
            format='json'
        )
        
        # Delete - should require admin
        delete_response = self.client.delete(
            reverse('book-delete', kwargs={'pk': self.book1.id})
        )
        
        self.assertEqual(list_response.status_code, status.HTTP_200_OK)
        self.assertEqual(detail_response.status_code, status.HTTP_200_OK)
        self.assertEqual(create_response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(update_response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(delete_response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_authentication_workflow(self):
        """Test complete authentication workflow."""
        # Step 1: Try to create without auth (should fail)
        data = {
            'title': 'Auth Test Book',
            'author': self.author1.id,
            'publication_year': 2023
        }
        create_response = self.client.post(
            reverse('book-create'), data, format='json'
        )
        self.assertEqual(create_response.status_code, status.HTTP_401_UNAUTHORIZED)
        
        # Step 2: Authenticate and create (should succeed)
        self.client.force_authenticate(user=self.normal_user)
        create_response = self.client.post(
            reverse('book-create'), data, format='json'
        )
        self.assertEqual(create_response.status_code, status.HTTP_201_CREATED)
        
        # Get the new book ID
        new_book_id = create_response.data['data']['id']
        
        # Step 3: Update the book (should succeed)
        update_data = {'title': 'Updated Auth Book'}
        update_response = self.client.patch(
            reverse('book-update', kwargs={'pk': new_book_id}),
            update_data,
            format='json'
        )
        self.assertEqual(update_response.status_code, status.HTTP_200_OK)
        
        # Step 4: Try to delete as non-admin (should fail)
        delete_response = self.client.delete(
            reverse('book-delete', kwargs={'pk': new_book_id})
        )
        self.assertEqual(delete_response.status_code, status.HTTP_403_FORBIDDEN)
        
        # Step 5: Authenticate as admin and delete (should succeed)
        self.client.force_authenticate(user=self.admin_user)
        delete_response = self.client.delete(
            reverse('book-delete', kwargs={'pk': new_book_id})
        )
        self.assertEqual(delete_response.status_code, status.HTTP_204_NO_CONTENT)


class AuthorModelTests(TestCase):
    """Test suite for Author model."""
    
    def setUp(self):
        self.author = Author.objects.create(name='Test Author')
    
    def test_author_str_method(self):
        """Test Author model string representation."""
        self.assertEqual(str(self.author), 'Test Author')
    
    def test_author_books_relationship(self):
        """Test Author-Book relationship."""
        book = Book.objects.create(
            title='Test Book',
            author=self.author,
            publication_year=2023
        )
        
        self.assertEqual(self.author.books.count(), 1)
        self.assertEqual(self.author.books.first(), book)


class BookModelTests(TestCase):
    """Test suite for Book model."""
    
    def setUp(self):
        self.author = Author.objects.create(name='Test Author')
        self.book = Book.objects.create(
            title='Test Book',
            author=self.author,
            publication_year=2023
        )
    
    def test_book_str_method(self):
        """Test Book model string representation."""
        expected_str = f"Test Book (2023)"
        self.assertEqual(str(self.book), expected_str)
    
    def test_book_author_relationship(self):
        """Test Book-Author relationship."""
        self.assertEqual(self.book.author, self.author)
        self.assertEqual(self.book.author.name, 'Test Author')