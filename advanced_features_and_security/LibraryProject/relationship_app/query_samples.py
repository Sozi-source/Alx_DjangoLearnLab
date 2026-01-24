from relationship_app.models import Book, Author, Library, Librarian

# Query all books by a specific author.
def book_by_author(author_name):
    try:
        author = Author.objects.get(name=author_name)
        books = Book.objects.filter(author=author)
        print(f"Books by {author_name}:")

        for book in books:
            print(f"- {book.title}")
    except Author.DoesNotExist:
        print(f"No author found by name {author_name}")


        # List all books in a library.

def books_in_library(library_name):
    try:
        library = Library.objects.get(name=library_name)
        books = library.books.all()
        print(f"Books in {library_name} library")
        
        for book in books:
            print(f"- {book.title}")

    except Library.DoesNotExist:
        print(f"No library found with the name {library_name}")



def librarian_for_library(library_name):
    
    try:
        library = Library.objects.get(name = library_name)
        try:
       
            librarian = Librarian.objects.get(library=library)
            print(f"Librarian for {library_name}- {librarian}")
            return librarian
    
        except Librarian.DoesNotExist:
            print(f"No librarian librarian assigned to -{library_name}")
            return None
    except Library.DoesNotExist:
         print(f"{library_name} does not exist")
         return None
