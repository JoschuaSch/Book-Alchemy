from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Author(db.Model):
    """A model representing an author."""
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(80), nullable=False)
    birth_date = db.Column(db.Date, nullable=True)
    date_of_death = db.Column(db.Date, nullable=True)

    def __repr__(self):
        """Return a representative string of the author."""
        return f'<Author {self.name}>'

    def __str__(self):
        """Return the author's name as a string."""
        return self.name


class Book(db.Model):
    """A model representing a book."""
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    isbn = db.Column(db.String(13), nullable=False, unique=True)
    title = db.Column(db.String(200), nullable=False)
    publication_year = db.Column(db.Integer, nullable=True)
    author_id = db.Column(db.Integer, db.ForeignKey('author.id'), nullable=False)
    author = db.relationship('Author', backref=db.backref('books', lazy=True))

    def __repr__(self):
        """Return a representative string of the book."""
        return f'<Book {self.title}>'

    def __str__(self):
        """Return the book's title as a string."""
        return self.title
