<!-- create a book instance -->
book = Book.objects.create(
    title = '1984',
    author = 'George Orwell',
    publication_year = 1949
)

<!-- Output -->
<!-- Title -->
book.title
1984