from flask import Flask, request, jsonify
from core.library import DigitalLibrary, Book, BookNotAvailable

app = Flask(__name__)
library = DigitalLibrary()

@app.route('/books', methods=['GET'])
def get_books():
    return jsonify([
        {
            'title': book.title,
            'author': book.author,
            'isbn': book.isbn,
            'available': book.available
        }
        for book in library.books
    ])

@app.route('/books/<isbn>', methods=['GET'])
def get_book(isbn):
    for book in library.books:
        if book.isbn == isbn:
            return jsonify({
                'title': book.title,
                'author': book.author,
                'isbn': book.isbn,
                'available': book.available
            })
    return jsonify({'error': 'Book not found'}), 404

@app.route('/books', methods=['POST'])
def add_book():
    data = request.get_json()
    title = data.get('title')
    author = data.get('author')
    isbn = data.get('isbn')
    is_ebook = data.get('is_ebook', False)
    size = data.get('size')

    book = Book(title, author, isbn)
    if is_ebook and size:
        library.add_ebook(book, float(size))
    else:
        library.add_book(book)

    return jsonify({'message': 'Book added'}), 201

@app.route('/books/<isbn>', methods=['PUT'])
def update_book(isbn):
    data = request.get_json()
    for book in library.books:
        if book.isbn == isbn:
            book.title = data.get('title', book.title)
            book.author = data.get('author', book.author)
            return jsonify({'message': 'Book updated'})
    return jsonify({'error': 'Book not found'}), 404

@app.route('/books/<isbn>', methods=['DELETE'])
def delete_book(isbn):
    library.remove_book(isbn)
    return jsonify({'message': 'Book deleted'})

@app.route('/lend/<isbn>', methods=['POST'])
def lend_book(isbn):
    try:
        library.lend_book(isbn)
        return jsonify({'message': 'Book lent'})
    except BookNotAvailable as e:
        return jsonify({'error': str(e)}), 400

@app.route('/return/<isbn>', methods=['POST'])
def return_book(isbn):
    try:
        library.return_book(isbn)
        return jsonify({'message': 'Book returned'})
    except BookNotAvailable as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)
