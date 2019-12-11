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
    
    f = open("users.csv")
    users = csv.reader(f)
    next(users) #skip header

    id = 0
    
    for email, password, name in users:
        id+=1
        db.execute("INSERT INTO USERS (email, password, name) VALUES(:email, :password, :name)",
        {"email": email, "password": password, "name": name})
    db.commit()

    return app

if __name__ == "__main__":
    with app.app_context():
        create_app()