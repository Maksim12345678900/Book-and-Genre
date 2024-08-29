from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///instance/app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Genre(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    books = db.relationship('Book', backref='genre', lazy=True)

    def __repr__(self):
        return f'<Genre {self.name}>'

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    genre_id = db.Column(db.Integer, db.ForeignKey('genre.id'), nullable=False)

    def __repr__(self):
        return f'<Book {self.title} by {self.author}>'

@app.route('/')
def index():
    books = Book.query.order_by(Book.created_at.desc()).limit(15).all()
    return render_template('index.html', books=books)

@app.route('/genre/<int:genre_id>')
def genre(genre_id):
    genre = Genre.query.get_or_404(genre_id)
    books = Book.query.filter_by(genre_id=genre.id).order_by(Book.created_at.desc()).all()
    return render_template('genre.html', genre=genre, books=books)

@app.before_first_request
def create_tables():
    db.create_all()

    if not Genre.query.first():
        # Добавление тестовых жанров
        genre1 = Genre(name='Fantasy')
        genre2 = Genre(name='Science Fiction')
        genre3 = Genre(name='Mystery')
        db.session.add_all([genre1, genre2, genre3])
        db.session.commit()

        # Добавление тестовых книг
        book1 = Book(title='The Hobbit', author='J.R.R. Tolkien', genre_id=genre1.id)
        book2 = Book(title='Dune', author='Frank Herbert', genre_id=genre2.id)
        book3 = Book(title='The Hound of the Baskervilles', author='Arthur Conan Doyle', genre_id=genre3.id)
        db.session.add_all([book1, book2, book3])
        db.session.commit()

if __name__ == '__main__':
    app.run(debug=True)
