from flask import Flask, render_template, request, redirect, url_for, flash, get_flashed_messages
from data_models import db, Author, Book
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = r'sqlite:///C:\Users\schro\Book-Alchemy\data\library.sqlite'
app.secret_key = 'yes_sir'
db.init_app(app)


@app.route('/add_author', methods=['GET', 'POST'])
def add_author():
    if request.method == 'POST':
        name = request.form.get('name')
        birth_date_str = request.form.get('birth_date')
        birth_date = datetime.strptime(birth_date_str, '%Y-%m-%d').date() if birth_date_str else None
        date_of_death_str = request.form.get('date_of_death')
        date_of_death = datetime.strptime(date_of_death_str, '%Y-%m-%d').date() if date_of_death_str else None
        new_author = Author(name=name, birth_date=birth_date, date_of_death=date_of_death)
        db.session.add(new_author)
        db.session.commit()
        flash('Author added successfully!', 'success')
        return redirect(url_for('add_author'))
    return render_template('add_author.html')


@app.route('/add_book', methods=['GET', 'POST'])
def add_book():
    if request.method == 'POST':
        title = request.form.get('title')
        isbn = request.form.get('isbn')
        publication_year = request.form.get('publication_year')
        author_id = request.form.get('author_id')
        new_book = Book(title=title, isbn=isbn, publication_year=publication_year, author_id=author_id)
        db.session.add(new_book)
        db.session.commit()
        flash('Book added successfully!', 'success')
        return redirect(url_for('add_book'))
    authors = Author.query.all()
    return render_template('add_book.html', authors=authors)


@app.route('/', methods=['GET'])
def home():
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
    book = Book.query.get_or_404(book_id)
    if not book:
        flash('Book not found!', 'error')
        return redirect(url_for('home'))
    db.session.delete(book)
    db.session.commit()
    flash('Book deleted successfully!', 'success')
    return redirect(url_for('home'))


@app.route('/book/<int:book_id>/confirm_delete', methods=['GET', 'POST'])
def confirm_delete(book_id):
    book = Book.query.get_or_404(book_id)
    if request.method == 'POST':
        db.session.delete(book)
        db.session.commit()
        flash('Book deleted successfully!', 'success')
        return redirect(url_for('home'))
    return render_template('confirm_delete.html', book=book)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
