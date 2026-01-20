from django.shortcuts import render
from .models import Library, Book
from django.views.generic.detail import DetailView
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth import login
from django.shortcuts import render, redirect
from django.contrib import messages
from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test

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
    return render (request, 'admin_view.html')

# librarian
def is_librarian(user):
    return user.is_authenticated and user.profile.role =='LIBRARIAN'

@user_passes_test(is_librarian)
def librarian_view(request):
    return render(request, 'librarian_view.html')

# member
def is_member(user):
    return user.is_authenticated and user.profile.role =='MEMBER'

@user_passes_test(is_member)
def member_view(request):
    return render(request, 'member_view.html ')