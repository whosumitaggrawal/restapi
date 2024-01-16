from flask import Flask, jsonify, request
app = Flask(__name__)

books_list = [
    {
        "id": 1,
        "author": "Hans Christian Andersen",
        "language": "Danish",
        "title": "Fairy tales"
    },
    {
        "id": 2,
        "author": "Dante Alighieri",
        "language": "Italian",
        "title": "The Divine Comedy"
    },
    {
        "id": 3,
        "author": "Walt Whitman",
        "language": "English",
        "title": "Leaves of Grass"
    },
    {
        "id": 4,
        "author": "Virginia Woolf",
        "language": "English",
        "title": "Mrs Dalloway"
    },
    {
        "id": 5,
        "author": "Other Woolf",
        "language": "English",
        "title": "To the Lighthouse"
    },
    {
        "id": 6,
        "author": "Marguerite Yourcenar",
        "language": "French",
        "title": "Memoirs of Hadrian"
    },
    {
        "id": 7,
        "author": "Chinua Achebe",
        "language": "English",
        "title": "Things Fall Apart"
    }
]

def get_book_by_id(book_id):
    return next((book for book in books_list if book['id'] == book_id), None)

@app.route('/books', methods=['GET'])
def get_books():
    return jsonify({'books': books_list})

@app.route('/books/<int:book_id>', methods=['GET'])
def get_book(book_id):
    book = next((book for book in books_list if book['id'] == book_id), None)
    if book is None:
        return jsonify({'error': 'Book not found'}), 404
    return jsonify({'book': book})

@app.route('/books', methods=['POST'])
def create_book_form_data():
    author = request.form.get('author')
    language = request.form.get('language')
    title = request.form.get('title')

    if not author or not language or not title:
        return jsonify({'error': 'Author, Language, and Title are required'}), 400

    new_book = {
        'id': len(books_list) + 1,
        'author': author,
        'language': language,
        'title': title
    }
    books_list.append(new_book)
    return jsonify({'book': new_book}), 201

@app.route('/books/<int:book_id>', methods=['PUT'])
def update_book_form_data(book_id):
    book = next((book for book in books_list if book['id'] == book_id), None)
    if book is None:
        return jsonify({'error': 'Book not found'}), 404

    author = request.form.get('author', book['author'])
    language = request.form.get('language', book['language'])
    title = request.form.get('title', book['title'])

    book['author'] = author
    book['language'] = language
    book['title'] = title

    return jsonify({'book': book})

@app.route('/books/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    book = get_book_by_id(book_id)
    if book is None:
        return jsonify({'error': 'Book not found'}), 404
    global books_list
    books_list = [b for b in books_list if b['id'] != book_id]
    return jsonify({'result': True, 'message': f'Book with ID {book_id} deleted successfully'})


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')