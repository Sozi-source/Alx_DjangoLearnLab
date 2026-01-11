from bookshelf.models import Book
# Delete the book instance
book.delete()

# Confirm deletion by checking if the book exists
Book.objects.all()

# output
(1, {'bookshelf.Book': 1}) 
<QuerySet []> 
