# CREATE
book = Book.objects.create(
    title='1984',
    author='George Orwell',
    publication_year=1949
)

# Output
book.title
# '1984'

# RETRIEVE
book = Book.objects.get(id=1)
book.title
# '1984'
book.author
# 'George Orwell'
book.publication_year
# 1949

# UPDATE
book.title = "Nineteen Eighty-Four"
book.save()

# Output
book.title
# 'Nineteen Eighty-Four'

# DELETE
book.delete()

# Confirm deletion by checking if the book exists
Book.objects.all()
# (1, {'bookshelf.Book': 1})
# <QuerySet []>
