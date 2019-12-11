from flask import Flask
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from models import *

import csv
import os

# database engine object from SQLAlchemy that manages connections to the database
engine = create_engine(os.getenv("DATABASE_URL")) 

# create a 'scoped session'
db = scoped_session(sessionmaker(bind=engine))    

app = Flask(__name__)

def create_app():
    
    f = open("books.csv")
    books = csv.reader(f)
    next(books) #skip header

    id = 0
    
    for isbn, title, author, year in books:
        id+=1
        db.execute("INSERT INTO BOOKS (isbn, title, author, year) VALUES(:isbn, :title, :author, :year)",
        {"isbn": isbn, "title": title, "author": author, "year": year})
    db.commit()

    return app

if __name__ == "__main__":
    with app.app_context():
        create_app()