#Import CSV file using ORM instead of SQL queries in the codes

from flask import Flask
from models import *
import csv

import os

#------------NEW--------------
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

#engine = create_engine(os.getenv("DATABASE_URL")) # database engine object from SQLAlchemy that manages connections to the database
                                                # DATABASE_URL is an environment variable that indicates where the database lives
#db = scoped_session(sessionmaker(bind=engine))    # create a 'scoped session' that ensures different users' interactions with the
                                                # database are kept separate
#--------------------------
#db.query_property
#----------From INIT



app = Flask(__name__)

print(os.getenv("DATABASE_URL"))
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

#db = SQLAlchemy(app)

#Link the Flask app with the db
db.init_app(app)
    #----------------------------------

def create_app():
    #from models import Book
    f = open("books.csv")
    books = csv.reader(f)
    next(books) #skip header

    #book = Book()
    id = 0
    
    for isbn, title, author, year in books:
        id+=1
        # db.execute("INSERT INTO BOOKS (isbn, title, author, year) VALUES(:isbn, :title, :author, :year)",
        # {"isbn": isbn, "title": title, "author": author, "year": year})
        # print(f"Added book '{title}' into the books table")
        book = Book(isbn=isbn, title=title, author=author, year=year)
        db.session.add(book)
    db.session.commit()

    return app
    #print(isbn, title, author, year)

if __name__ == "__main__":
    with app.app_context():
        create_app()
    #app.run()







#From documentation:
#     db = SQLAlchemy()

# def create_app():
#     app = Flask(__name__)
#     db.init_app(app)
#     return app