from django.urls import path
from . import views

urlpatterns = [
    path('list_books/', views.list_books, name='list_books'),
    path('libraryDetails/<int:pk>/', views.LibraryDetailedView.as_view(), name='library_details')
]