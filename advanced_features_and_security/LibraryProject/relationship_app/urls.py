from django.urls import path
from . import views
from .views import list_books, LibraryDetailView, register
from django.contrib.auth.views import LoginView, LogoutView
from .admin_view import admin_view
from .librarian_view import librarian_view
from .member_view import member_view

urlpatterns = [
    path(
        'list_books/', 
         views.list_books, 
         name='list_books'
         ),

    path(
        'libraryDetails/<int:pk>/', 
        views.LibraryDetailView.as_view(), 
        name='library_details'
        ),

    path(
        'login/', 
        LoginView.as_view(template_name='relationship_app/login.html'),
        name='login'
        ),

    path(
        'register/', 
        views.register,
        name = 'register'
        
        ),

    path('logout/', LogoutView.as_view(template_name='relationship_app/logout.html'), name='logout'),


    path('admin/', admin_view, name='admin_view'),
    path('librarian/', librarian_view, name='librarian_view'),
    path('member/', member_view, name='member_view'),

    # Add a new book (requires permission)
    path('add_book/', views.add_book, name='add_book'),

    # Edit an existing book (requires permission)
    path('edit_book/', views.edit_book, name='edit_book'),

    # Delete a book (requires permission)
    path('delete_book/', views.delete_book, name='delete_book'),
]