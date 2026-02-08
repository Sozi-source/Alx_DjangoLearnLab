"""
URL configuration for Book API endpoints
Step 2: Define URL Patterns
"""
from django.urls import path
from . import views

urlpatterns = [
    # Step 2: Define URL patterns for each view
    path('books/', views.BookListView.as_view(), name='book-list'),           # ListView
    path('books/<int:pk>/', views.BookDetailView.as_view(), name='book-detail'),  # DetailView
    path('books/create/', views.BookCreateView.as_view(), name='book-create'),    # CreateView
    path('books/update/<int:pk>/', views.BookUpdateView.as_view(), name='book-update'),  # UpdateView
    path('books/delete/<int:pk>/', views.BookDeleteView.as_view(), name='book-delete'),  # DeleteView
]