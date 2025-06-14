from flask import Flask, request, jsonify
from core.library import DigitalLibrary, Book, BookNotAvailable

app = Flask(__name__)
library = DigitalLibrary()

@app.route('/books', methods=['GET'])
def get_books():
    all_books = library.books
    books_data = []
    for book in all_books:
        book_info = {
            "title": book.title,
            "author": book.author,
            "isbn": book.isbn,
            "available": book.available
        }
        if book.isbn in library.download_sizes:
            book_info["download_size"] = library.download_sizes[book.isbn]
        books_data.append(book_info)
    return jsonify(books_data)

@app.route('/books', methods=['POST'])
def add_book():
    data = request.get_json()
    if not all(k in data for k in ("title", "author", "isbn")):
        return {"error": "Missing fields"}, 400

    book = Book(data["title"], data["author"], data["isbn"])
    if "download_size" in data:
        library.add_ebook(book, float(data["download_size"]))
    else:
        library.add_book(book)
    return {"message": "Book added successfully"}, 201

@app.route('/books/<isbn>/lend', methods=['PUT'])
def lend_book(isbn):
    try:
        library.lend_book(isbn)
        return {"message": f"Book {isbn} lent successfully."}
    except BookNotAvailable as e:
        return {"error": str(e)}, 400

@app.route('/books/<isbn>/return', methods=['PUT'])
def return_book(isbn):
    try:
        library.return_book(isbn)
        return {"message": f"Book {isbn} returned successfully."}
    except BookNotAvailable as e:
        return {"error": str(e)}, 400

@app.route('/books/<isbn>', methods=['DELETE'])
def remove_book(isbn):
    library.remove_book(isbn)
    return {"message": f"Book {isbn} removed successfully."}

@app.route('/books/author/<author>', methods=['GET'])
def search_by_author(author):
    books = list(library.books_by_author(author))
    return jsonify([
        {
            "title": book.title,
            "author": book.author,
            "isbn": book.isbn,
            "available": book.available
        } for book in books
    ])

if __name__ == '__main__':
    app.run(debug=True)
