from .book import Book, BookNotAvailable

class Library:
    def __init__(self):
        self.books = []

    def add_book(self, book):
        self.books.append(book)

    def remove_book(self, isbn):
        self.books = [book for book in self.books if book.isbn != isbn]

    def lend_book(self, isbn):
        for book in self.books:
            if book.isbn == isbn:
                if book.available:
                    book.available = False
                    return
                else:
                    raise BookNotAvailable("Book already lent.")
        raise BookNotAvailable("Book not found.")

    def return_book(self, isbn):
        for book in self.books:
            if book.isbn == isbn:
                book.available = True
                return
        raise BookNotAvailable("Book not found.")

    def __iter__(self):
        self.available_books = [b for b in self.books if b.available]
        self.index = 0
        return self

    def __next__(self):
        if self.index < len(self.available_books):
            book = self.available_books[self.index]
            self.index += 1
            return book
        raise StopIteration

    def books_by_author(self, author):
        return (book for book in self.books if book.author.lower() == author.lower())

class DigitalLibrary(Library):
    def __init__(self):
        super().__init__()
        self.download_sizes = {}

    def add_ebook(self, book, size):
        self.add_book(book)
        self.download_sizes[book.isbn] = size

    def get_download_size(self, isbn):
        return self.download_sizes.get(isbn, "Unknown")
