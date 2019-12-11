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
    
    f = open("reviews.csv")
    reviews = csv.reader(f)
    next(reviews) #skip header

    id = 0
    
    for book_id, user_id, rating, comments, created_date in reviews:
        id+=1
        db.execute("INSERT INTO REVIEWS (book_id, user_id, rating, comments, created_date) VALUES(:book_id, :user_id, :rating, :comments, :created_date)",
        {"book_id": book_id, "user_id": user_id, "rating": rating, "comments": comments, "created_date": created_date})
    db.commit()

    return app

if __name__ == "__main__":
    with app.app_context():
        create_app()