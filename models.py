from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()

class Book(db.Model):
    __tablename__ = 'books'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(1000), nullable=False)
    author = db.Column(db.String(1000), nullable=True)
    year = db.Column(db.Integer, nullable=False)
    isbn = db.Column(db.String(10), nullable=False)

class User(db.Model):
    __tablename__ = 'users'
    user_id = db.Column(db.String(100), primary_key=True)
    name = db.Column(db.String(1000), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)

class Review(db.Model):
    __tablename__ = 'reviews'
    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey(Book.id), nullable=False)
    user_id = db.Column(db.String, db.ForeignKey(User.user_id), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    comments = db.Column(db.String(1000), nullable=True)
                             
