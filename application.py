import os

from flask import (Blueprint, Flask, g, redirect, render_template, request,
                   session, url_for)
from flask_login import LoginManager, login_required
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from models import Book

engine = create_engine(os.getenv("DATABASE_URL"))

db = scoped_session(sessionmaker(bind=engine))

# Instantiate a new web application called `app`, with `__name__` representing the current file
app = Flask(__name__) 

#Creates the secret key
app.secret_key = os.urandom(24)

#Reset global variable before loads the page
@app.before_request
def before_request():
  g.user = None

  if 'user' in session:
    g.user = session['user']

#Login route
@app.route('/', methods=['GET','POST'])
def index():
  if request.method == 'POST':
    session.pop('user', None)

    email = request.form.get('email')
    password = request.form.get('password')
    
    rows = db.execute("SELECT * FROM USERS WHERE EMAIL = :email AND password = :password",{"email" : email, "password" : password}).fetchall()

    if len(rows) != 0:
      session['user'] = email

      return redirect(url_for('main'))
    else:
      return render_template('index.html', message="Wrong username or password, please try again")
  return render_template('index.html')

#Main route - Search books
@app.route('/main', methods=['GET','POST'])
def main():
  if g.user:
    # if search field is filled up
    if request.form.get("search") != None:
      search = request.form.get("search")
      search = "%" + search + "%"
      
      # execute this SQL command and return the result of the search
      search_res = db.execute("SELECT * FROM books WHERE Author LIKE :search OR Title LIKE :search OR Isbn LIKE :search",{"search": search}).fetchall()
      
      # if result exists, shows in the page, otherwise return message 
      if len(search_res) != 0:
        return render_template('main.html', books=search_res,  user=session['user'])
      else:
        return render_template('main.html', message='No Books found.',  user=session['user'])
    else:
      return render_template('main.html', user=session['user'])
  return redirect(url_for('index'))

#Book details page
@app.route('/books/<book_id>')
def books(book_id):
  if g.user:
    book = db.execute("SELECT * FROM books WHERE id = :id",{"id":book_id}).fetchone()
    
    #reviews = db.execute("SELECT * FROM REVIEWS WHERE book_id = :book_id",{"book_id":book_id}).fetchall()
    reviews = db.execute("SELECT * FROM REVIEWS INNER JOIN USERS ON REVIEWS.USER_ID = USERS.ID WHERE book_id = :book_id",{"book_id":book_id}).fetchall()
    print(f"g.user:{reviews}")
    print(f"g.user:{g.user}")

    #Checks if user has already added a review for the book
    my_review = db.execute("SELECT * FROM reviews INNER JOIN users ON reviews.user_id = users.id WHERE users.email = :g_user AND reviews.book_id = :book_id ", {"g_user" : g.user, "book_id" : book_id}).fetchone()
    
    print(my_review)

    ############################################ CHECKING ISSUE BELOW
    if (my_review) != None:
    #if len(my_review) != 0:
      enable_review = True
    else:
      enable_review = False

    #return render_template("book.html", book=book, reviews=reviews, user=g.user, enable_review=enable_review)
    return render_template("book.html", book=book, reviews=reviews, user=g.user, enable_review=enable_review)
  return redirect(url_for('index'))

#book review
@app.route('/books/<book_id>', methods=['POST'])
def add_review(book_id):
  if g.user:
    print(f"user:{g.user}")
    rating = request.form.get("rating")
    comments = request.form.get("comments")
    db.execute("INSERT INTO REVIEWS (book_id,email,rating,comments) VALUES (:book_id, :email, :rating, :comments)", {"book_id":book_id, "email":g.user, "rating":rating, "comments":comments})
    db.commit()
    return redirect(url_for('books',book_id=book_id))
  return redirect(url_for('index'))

#Register route
@app.route('/register', methods=['GET', 'POST'])
def register():
    session.pop('user', None)
    try:
      if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        db.execute("INSERT INTO USERS (name, email, password) VALUES (:name, :email, :password)", {"name":name, "email":email, "password":password})
        db.commit()
        print('Database has been updated with a new user.')
    except:
      return render_template('register.html', message="Unable to retrieve the data")
    return render_template('register.html')

#Delete route
@app.route('/books/<book_id>/<review_id>/delete', methods=['GET'])
def delete_review(book_id, review_id):
    print(book_id)
    print(review_id)
    print("Chegou aqui0!")
    if g.user:
      print("Chegou aqui1!")
      db.execute("DELETE FROM REVIEWS WHERE REVIEWS.ID = :review_id", {"review_id" : review_id})
      db.commit()
      print("Chegou aqui2!")
      return redirect(url_for('books', book_id = book_id))
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)

#Log out
@app.route('/dropsession')
def dropsession():
    session.pop('user', None)
    return redirect(url_for('index'))
