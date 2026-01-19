from django.shortcuts import render
from .models import Book, Library
from django.views.generic import DetailView

# Create your views here.
def list_books(request):
    books = Book.objects.all()
    context = {'books': books}

    return render(request, 'relationship_app/list_books.html', context)


class LibraryDetailedView(DetailView):
    model = Library
    template_name = 'library/library_detail.html'
    context_object_name = 'library'