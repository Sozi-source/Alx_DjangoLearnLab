from django.urls import path
from . import views


urlpatterns = [
    path('books/', views.BookCreateView.as_view(), name='books-list'),
    path('books/<int:pk>/', views.BookDetailView.as_view(), name='book-details'),

    path('authors/', views.AuthorCreateView.as_view(), name='create-author'),
    path('authors/', views.AuthorDetailView.as_view(), name='author-details')
]