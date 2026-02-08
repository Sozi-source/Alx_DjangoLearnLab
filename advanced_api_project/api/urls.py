from django.urls import path
from .views import AuthorDetailView, BookDetailView, AuthorCreateView, BookCreateView
from api import views

urlpatterns = [
    # create and list authors
    path('authors/', views.AuthorCreateView.as_view(), name='author-create'),
    path('authors/<int:pk>/', views.AuthorDetailView.as_view(), name='author-detail'),

    # create and list books
    path('books/', views.BookCreateView.as_view(), name='book-create'),
    path('books/<int:pk>/', views.BookDetailView.as_view(), name='book-detail')

]