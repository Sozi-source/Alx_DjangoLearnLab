from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test, permission_required
from .models import Book, CustomUser
from django.shortcuts import redirect
from forms import ExampleForm

# ===== ROLE CHECK FUNCTIONS =====
def is_admin(user):
    """Check if user is admin via role field"""
    return user.is_authenticated and user.role == 'Admin'

def is_librarian(user):
    """Check if user is librarian via role field"""
    return user.is_authenticated and user.role == 'Librarian'

def is_member(user):
    """Check if user is member via role field"""
    return user.is_authenticated and user.role == 'Member'

# ===== ROLE-BASED VIEWS =====
@user_passes_test(is_admin)
def admin_view(request):
    """Admin dashboard"""
    return render(request, 'bookshelf/admin_view.html', {
        'user': request.user,
        'role': 'Admin'
    })

@user_passes_test(is_librarian)
def librarian_view(request):
    """Librarian dashboard"""
    return render(request, 'bookshelf/librarian_view.html', {
        'user': request.user,
        'role': 'Librarian'
    })

@user_passes_test(is_member)
def member_view(request):
    """Member dashboard"""
    return render(request, 'bookshelf/member_view.html', {
        'user': request.user,
        'role': 'Member'
    })

# ===== SIMPLE BOOK VIEWS =====
@login_required
def book_list(request):
    """Show all books"""
    books = Book.objects.all()
    return render(request, 'bookshelf/book_list.html', {'books': books})

@login_required
def book_detail(request, book_id):
    """Show single book details"""
    book = get_object_or_404(Book, id=book_id)
    return render(request, 'bookshelf/book_detail.html', {'book': book})

@login_required
def user_list(request):
    """Show all users (staff only)"""
    if not request.user.is_staff:
        return render(request, 'bookshelf/access_denied.html')
    
    users = CustomUser.objects.all()
    return render(request, 'bookshelf/user_list.html', {'users': users})

@login_required
def user_detail(request, user_id):
    """Show user profile"""
    user = get_object_or_404(CustomUser, id=user_id)
    
    # Users can only view their own profile unless staff
    if not request.user.is_staff and request.user.id != user.id:
        return render(request, 'bookshelf/access_denied.html')
    
    return render(request, 'bookshelf/user_detail.html', {'user_profile': user})

# ===== PERMISSION-BASED BOOK OPERATIONS =====
from django.contrib.auth.decorators import permission_required

@permission_required('bookshelf.can_add_book', raise_exception=True)
@login_required
def add_book(request):
    """Add a new book"""
    if request.method == 'POST':
        title = request.POST.get('title')
        author = request.POST.get('author')
        publication_year = request.POST.get('publication_year')
        
        Book.objects.create(
            title=title,
            author=author,
            publication_year=publication_year
        )
        return redirect('book_list')
    
    return render(request, 'bookshelf/add_book.html')

@permission_required('bookshelf.can_change_book', raise_exception=True)
@login_required
def edit_book(request, book_id):
    """Edit a book"""
    book = get_object_or_404(Book, id=book_id)
    
    if request.method == 'POST':
        book.title = request.POST.get('title')
        book.author = request.POST.get('author')
        book.publication_year = request.POST.get('publication_year')
        book.save()
        return redirect('book_detail', book_id=book.id)
    
    return render(request, 'bookshelf/edit_book.html', {'book': book})

@permission_required('bookshelf.can_delete_book', raise_exception=True)
@login_required
def delete_book(request, book_id):
    """Delete a book"""
    book = get_object_or_404(Book, id=book_id)
    
    if request.method == 'POST':
        book.delete()
        return redirect('book_list')
    
    return render(request, 'bookshelf/delete_book.html', {'book': book})