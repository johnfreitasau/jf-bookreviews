from flask_login import UserMixin

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy.types import DateTime

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
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))
    created_date = db.Column(DateTime(), default=datetime.utcnow) #NEW

class Review(db.Model):
    __tablename__ = 'reviews'
    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey(Book.id), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    comments = db.Column(db.String, nullable=True)
    created_date = db.Column(db.DateTime, server_default=db.func.now())
                             
