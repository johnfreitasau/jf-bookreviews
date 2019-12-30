import os
from flask import Flask, render_template, request

#import table definitions
from models import *

app = Flask(__name__)

print(os.getenv("DATABASE_URL"))
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

#Link the Flask app with the db
db.init_app(app)

def main():
    #Create tables based on each table definition in 'models'
    db.create_all()

if __name__ == "__main__":
    #Allow for command line interaction with Flask app
    with app.app_context():
        main()
