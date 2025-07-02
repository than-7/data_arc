from flask import Flask, request, jsonify, render_template, redirect

app = Flask(__name__)

books = []

# HTML Home
@app.route('/')
def index():
    return render_template('index.html')

# HTML Form for adding book
@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        book = {
            "id": len(books) + 1,
            "title": title,
            "author": author
        }
        books.append(book)
        return redirect('/view')
    return render_template('add_book.html')

# HTML Table View
@app.route('/view')
def view():
    return render_template('view_books.html', books=books)

# JSON API: GET all books
@app.route('/api/books', methods=['GET'])
def get_books():
    return jsonify({"books": books}), 200

# JSON API: POST new book
@app.route('/api/books', methods=['POST'])
def post_book():
    data = request.json
    if not data or 'title' not in data or 'author' not in data:
        return jsonify({"error": "Missing title or author"}), 400
    book = {
        "id": len(books) + 1,
        "title": data['title'],
        "author": data['author']
    }
    books.append(book)
    return jsonify(book), 201

if __name__ == '__main__':
    app.run(debug=True)
