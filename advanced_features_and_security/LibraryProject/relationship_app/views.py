from django.shortcuts import render
from .models import Library, Book, Author
from django.views.generic.detail import DetailView
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth import login
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.decorators import permission_required


# Create your views here.
def list_books(request):
    books = Book.objects.all()
    context = {'books': books}

    return render(request, 'relationship_app/list_books.html', context)


class LibraryDetailView(DetailView):
    model = Library
    template_name = 'relationship_app/library_detail.html'
    context_object_name = 'library'


# user registration
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Registration successful! You can now log in.')
            login(request, user)
            return redirect('list_books')
    else:
        form = UserCreationForm()
    return render (request, 'relationship_app/register.html', {'form':form})


# admin
def is_admin(user):
    return user.is_authenticated and user.profile.role =='ADMIN'

@user_passes_test(is_admin)
def admin_view(request):
    return render (request, 'relationship_app/admin_view.html')

# librarian
def is_librarian(user):
    return user.is_authenticated and user.profile.role =='LIBRARIAN'

@user_passes_test(is_librarian)
def librarian_view(request):
    return render(request, 'relationship_app/librarian_view.html')

# member
def is_member(user):
    return user.is_authenticated and user.profile.role =='MEMBER'

@user_passes_test(is_member)
def member_view(request):
    return render(request, 'relationship_app/member_view.html ')

# permission check
# add a new book
@permission_required('relationship_app.can_add_book', raise_exception=True)
def add_book(request):
    authors = Author.objects.all()
    if request.method == 'POST':
        title = request.POST.get('title')
        author_id = request.POST.get('author')
        author = get_object_or_404(Author, id=author_id)
        Book.objects.create(title=title, author=author)
        messages.success(request, 'Book added successfully!')
        return redirect('list_books')
    return render(request, 'relationship_app/add_book.html', {'authors': authors})

@permission_required('relationship_app.can_change_book', raise_exception=True)
def edit_book(request, pk):
    book = get_object_or_404(Book, id=pk)
    authors = Author.objects.all()
    if request.method == 'POST':
        book.title = request.POST.get('title')
        author_id = request.POST.get('author')
        book.author = get_object_or_404(Author, id=author_id)
        book.save()
        messages.success(request, 'Book updated successfully!')
        return redirect('list_books')
    return render(request, 'relationship_app/edit_book.html', {'book': book, 'authors': authors})

# Delete a book
@permission_required('relationship_app.can_delete_book', raise_exception=True)
def delete_book(request, pk):
    book = get_object_or_404(Book, id=pk)
    if request.method == 'POST':
        book.delete()
        messages.success(request, 'Book deleted successfully!')
        return redirect('list_books')
    return render(request, 'relationship_app/delete_book.html', {'book': book})