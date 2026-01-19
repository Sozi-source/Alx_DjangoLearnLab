from django.urls import path
from . import views
from .views import list_books, LibraryDetailedView

urlpatterns = [
    path('list_books/', views.list_books, name='list_books'),
    path('libraryDetails/<int:pk>/', views.LibraryDetailView.as_view(), name='library_details')
]