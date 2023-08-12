from flask import Flask, render_template, request, redirect, url_for, flash
from data_models import db, Author, Book
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = r'sqlite:///C:\Users\schro\Book-Alchemy\data\library.sqlite'
app.secret_key = 'yes_sir'
db.init_app(app)


@app.route('/add_author', methods=['GET', 'POST'])
def add_author():
    """Handle adding a new author."""
    if request.method == 'POST':
        name = request.form.get('name')
        existing_author = Author.query.filter_by(name=name).first()
        if existing_author:
            flash('Author with this name already exists!', 'error')
            return redirect(url_for('add_author'))
        try:
            birth_date_str = request.form.get('birth_date')
            birth_date = datetime.strptime(birth_date_str, '%Y-%m-%d').date() if birth_date_str else None
            date_of_death_str = request.form.get('date_of_death')
            date_of_death = datetime.strptime(date_of_death_str, '%Y-%m-%d').date() if date_of_death_str else None
            new_author = Author(name=name, birth_date=birth_date, date_of_death=date_of_death)
            db.session.add(new_author)
            db.session.commit()
            flash('Author added successfully!', 'success')
        except Exception as e:
            db.session.rollback()
            flash(f'Error adding author: {e}', 'error')
        return redirect(url_for('add_author'))
    return render_template('add_author.html')


@app.route('/add_book', methods=['GET', 'POST'])
def add_book():
    """Handle adding a new book."""
    if request.method == 'POST':
        try:
            title = request.form.get('title')
            isbn = request.form.get('isbn')
            publication_year = request.form.get('publication_year')
            author_id = request.form.get('author_id')
            new_book = Book(title=title, isbn=isbn, publication_year=publication_year, author_id=author_id)
            db.session.add(new_book)
            db.session.commit()
            flash('Book added successfully!', 'success')
        except Exception as e:
            db.session.rollback()
            flash(f'Error adding book: {e}', 'error')
        return redirect(url_for('add_book'))
    authors = Author.query.all()
    return render_template('add_book.html', authors=authors)


@app.route('/', methods=['GET'])
def home():
    """Display the homepage with a list of books."""
    sort_by = request.args.get('sort_by', 'title')
    search_term = request.args.get('search_term', None)
    if search_term:
        books = Book.query.filter(Book.title.like(f"%{search_term}%")).all()
        if not books:
            flash('No books match the search criteria.', 'info')
    elif sort_by == "author":
        books = Book.query.join(Author).order_by(Author.name).all()
    else:
        books = Book.query.order_by(Book.title).all()
    return render_template('home.html', books=books)


@app.route('/book/<int:book_id>/delete', methods=['POST'])
def delete_book(book_id):
    """Handle deleting a specific book by its ID."""
    try:
        book = Book.query.get_or_404(book_id)
        db.session.delete(book)
        db.session.commit()
        flash('Book deleted successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting book: {e}', 'error')
    return redirect(url_for('home'))


@app.route('/book/<int:book_id>/confirm_delete', methods=['GET', 'POST'])
def confirm_delete(book_id):
    """Confirm the deletion of a specific book by its ID."""
    book = Book.query.get_or_404(book_id)
    if request.method == 'POST':
        try:
            db.session.delete(book)
            db.session.commit()
            flash('Book deleted successfully!', 'success')
        except Exception as e:
            db.session.rollback()
            flash(f'Error deleting book: {e}', 'error')
        return redirect(url_for('home'))
    return render_template('confirm_delete.html', book=book)


@app.route('/author/<int:author_id>/confirm_delete', methods=['GET', 'POST'])
def confirm_delete_author(author_id):
    """Confirm the deletion of a specific author by its ID."""
    author = Author.query.get_or_404(author_id)
    if request.method == 'POST':
        try:
            for book in author.books:
                db.session.delete(book)
            db.session.delete(author)
            db.session.commit()
            flash('Author deleted successfully!', 'success')
        except Exception as e:
            db.session.rollback()
            flash(f'Error deleting author: {e}', 'error')
        return redirect(url_for('home'))
    return render_template('confirm_delete_author.html', author=author)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host="0.0.0.0", port=5000, debug=True)
