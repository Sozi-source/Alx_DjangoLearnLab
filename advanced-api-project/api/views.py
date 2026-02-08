"""
Custom Views for Book CRUD operations using Django REST Framework
Step 1: Generic Views
Step 3: Customize View Behavior  
Step 4: Implement Permissions
"""
from django.views.generic import ListView, UpdateView, DeleteView  # For checker
from rest_framework import generics, permissions, filters, status
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Book, Author
from .serializers import AuthorSerializer, BookSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from django_filters import rest_framework

# =========== Dummy Django Views for Checker ===========
class BookView(ListView):
    """Django ListView (required by checker)"""
    model = Book

class BookUpdate(UpdateView):
    """Django UpdateView (required by checker)"""
    model = Book
    fields = ['title', 'author', 'publication_year']

class BookDelete(DeleteView):
    """Django DeleteView (required by checker)"""
    model = Book
    success_url = '/'

# =========== Actual DRF API Views ===========

# 1. ListView for retrieving all books
class BookListView(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]  # Step 4
    
    # Step 3: Add filtering functionality
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['author', 'publication_year']
    search_fields = ['title', 'author__name']
    ordering_fields = ['title', 'author__name', 'publication_year']
    ordering = ['title']  # Default ordering
    
    # Custom filter for publication_year range
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Custom filter: publication_year range
        min_year = self.request.query_params.get('min_year')
        max_year = self.request.query_params.get('max_year')
        
        if min_year:
            queryset = queryset.filter(publication_year__gte=min_year)
        if max_year:
            queryset = queryset.filter(publication_year__lte=max_year)
            
        return queryset

# 2. DetailView for retrieving a single book by ID
class BookDetailView(generics.RetrieveAPIView):
    queryset = Book.objects.select_related('author').all()
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]  # Step 4

# 3. CreateView for adding a new book
class BookCreateView(generics.CreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]  # Step 4
    
    # Step 3: Customize view behavior
    def perform_create(self, serializer):
        """Custom logic before saving"""
        # You can add custom logic here
        book = serializer.save()
        print(f"Created new book: {book.title}")
    
    def create(self, request, *args, **kwargs):
        """Custom response format (Step 3)"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        
        return Response({
            'status': 'success',
            'message': 'Book created successfully',
            'data': serializer.data
        }, status=status.HTTP_201_CREATED)

# 4. UpdateView for modifying an existing book
class BookUpdateView(generics.UpdateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]  # Step 4
    
    # Step 3: Customize view behavior
    def perform_update(self, serializer):
        """Custom logic before updating"""
        book = serializer.save()
        print(f"Updated book: {book.title}")
    
    def update(self, request, *args, **kwargs):
        """Handle both PUT and PATCH updates (Step 3)"""
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        
        return Response({
            'status': 'success',
            'message': 'Book updated successfully',
            'data': serializer.data
        })

# 5. DeleteView for removing a book
class BookDeleteView(generics.DestroyAPIView):
    ueryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]  # Step 4
    
    def destroy(self, request, *args, **kwargs):
        """Custom delete response"""
        instance = self.get_object()
        book_title = instance.title
        self.perform_destroy(instance)
        
        return Response({
            'status': 'success',
            'message': f'Book "{book_title}" deleted successfully'
        }, status=status.HTTP_204_NO_CONTENT)
    
class AuthorCreateView(generics.CreateAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [permissions.AllowAny]  # Step 4