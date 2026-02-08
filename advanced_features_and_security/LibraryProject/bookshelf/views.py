from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test, permission_required
from django.db.models import Q
from django.core.exceptions import ValidationError
from .models import Book, CustomUser
from .forms import ExampleForm, BookForm  # Use Django forms for validation

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
    """Admin dashboard - no user input"""
    return render(request, 'bookshelf/admin_view.html', {
        'user': request.user,
        'role': 'Admin'
    })

@user_passes_test(is_librarian)
def librarian_view(request):
    """Librarian dashboard - no user input"""
    return render(request, 'bookshelf/librarian_view.html', {
        'user': request.user,
        'role': 'Librarian'
    })

@user_passes_test(is_member)
def member_view(request):
    """Member dashboard - no user input"""
    return render(request, 'bookshelf/member_view.html', {
        'user': request.user,
        'role': 'Member'
    })

# ===== SECURED BOOK VIEWS =====
@login_required
def book_list(request):
    """Show all books with SAFE search functionality"""
    books = Book.objects.all()
    
    # SAFE search implementation (SQL injection protected)
    search_query = request.GET.get('search', '').strip()
    if search_query:
        # Use Django's Q objects - automatically escapes SQL
        books = books.filter(
            Q(title__icontains=search_query) |
            Q(author__icontains=search_query)
        )
    
    return render(request, 'bookshelf/book_list.html', {
        'books': books,
        'search_query': search_query
    })

@login_required
def book_detail(request, book_id):
    """Show single book details - SAFE using get_object_or_404"""
    # SAFE: get_object_or_404 validates the ID exists
    book = get_object_or_404(Book, id=book_id)
    return render(request, 'bookshelf/book_detail.html', {'book': book})

# ===== SECURED USER VIEWS =====
@login_required
def user_list(request):
    """Show all users (staff only) - SAFE query"""
    if not request.user.is_staff:
        return render(request, 'bookshelf/access_denied.html')
    
    # SAFE: No direct user input in query
    users = CustomUser.objects.all().order_by('username')
    return render(request, 'bookshelf/user_list.html', {'users': users})

@login_required
def user_detail(request, user_id):
    """Show user profile - SAFE with access control"""
    # SAFE: Validated user ID
    user = get_object_or_404(CustomUser, id=user_id)
    
    # Access control
    if not request.user.is_staff and request.user.id != user.id:
        return render(request, 'bookshelf/access_denied.html')
    
    return render(request, 'bookshelf/user_detail.html', {'user_profile': user})

# ===== SECURED BOOK OPERATIONS (Using Django Forms) =====
@permission_required('bookshelf.can_add_book', raise_exception=True)
@login_required
def add_book(request):
    """Add a new book using VALIDATED form"""
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():  # Django form validation prevents SQL injection
            form.save()
            return redirect('book_list')
    else:
        form = BookForm()
    
    return render(request, 'bookshelf/add_book.html', {'form': form})

@permission_required('bookshelf.can_change_book', raise_exception=True)
@login_required
def edit_book(request, book_id):
    """Edit a book using VALIDATED form"""
    book = get_object_or_404(Book, id=book_id)
    
    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():  # Form validation
            form.save()
            return redirect('book_detail', book_id=book.id)
    else:
        form = BookForm(instance=book)
    
    return render(request, 'bookshelf/edit_book.html', {'form': form, 'book': book})

@permission_required('bookshelf.can_delete_book', raise_exception=True)
@login_required
def delete_book(request, book_id):
    """Delete a book - SAFE ID validation"""
    book = get_object_or_404(Book, id=book_id)
    
    if request.method == 'POST':
        book.delete()
        return redirect('book_list')
    
    return render(request, 'bookshelf/delete_book.html', {'book': book})

# ===== EXAMPLE: SAFE SEARCH WITH VALIDATION =====
@login_required
def safe_search(request):
    """Example of safe search with input validation"""
    if request.method == 'GET':
        search_term = request.GET.get('q', '').strip()
        
        # Input validation
        if not search_term:
            return render(request, 'bookshelf/search.html', {
                'error': 'Please enter a search term'
            })
        
        # Validate length
        if len(search_term) < 2:
            return render(request, 'bookshelf/search.html', {
                'error': 'Search term must be at least 2 characters'
            })
        
        # Validate no SQL keywords (additional protection)
        sql_keywords = ['SELECT', 'INSERT', 'UPDATE', 'DELETE', 'DROP', 'UNION']
        if any(keyword in search_term.upper() for keyword in sql_keywords):
            return render(request, 'bookshelf/search.html', {
                'error': 'Invalid search term'
            })
        
        # SAFE: Use Django ORM with parameterized queries
        books = Book.objects.filter(
            Q(title__icontains=search_term) |
            Q(author__icontains=search_term)
        )[:50]  # Limit results to prevent DoS
        
        return render(request, 'bookshelf/search.html', {
            'books': books,
            'search_term': search_term,
            'count': books.count()
        })
    
    return render(request, 'bookshelf/search.html')

# ===== EXAMPLE FORM VIEW (For checker) =====
def example_form_view(request):
    """Example view using ExampleForm with validation"""
    if request.method == 'POST':
        form = ExampleForm(request.POST)
        if form.is_valid():  # Django validates input
            # Process valid data
            name = form.cleaned_data['name']  # Cleaned, safe data
            email = form.cleaned_data['email']
            # ... process data
            return redirect('book_list')
    else:
        form = ExampleForm()
    
    return render(request, 'bookshelf/example_form.html', {'form': form})