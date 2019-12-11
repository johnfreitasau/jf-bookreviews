from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy import create_engine

from flask import Blueprint, render_template, Flask, request, redirect, url_for, session, g
from flask_login import login_required, LoginManager
import os
from models import Book

engine = create_engine(os.getenv("DATABASE_URL"))

db = scoped_session(sessionmaker(bind=engine))

# Instantiate a new web application called `app`, with `__name__` representing the current file
app = Flask(__name__) 

#Creates the secret key
app.secret_key = os.urandom(24)

#Login
@app.route('/', methods=['GET','POST'])
def index():
  if request.method == 'POST':
    session.pop('user', None)

    if request.form['password'] == 'password':
      session['user'] = request.form['username']
      return redirect(url_for('protected'))
    else:
      return render_template('index.html',message="Wrong username or password, please try again")
  return render_template('index.html')

#Protected route
@app.route('/protected')
def protected():
  if g.user:
    return render_template('protected.html', user=session['user'])
  return redirect(url_for('index'))

#Reset global variable before loads the page
@app.before_request
def before_request():
  g.user = None

  if 'user' in session:
    g.user = session['user']

#Log out
@app.route('/dropsession')
def dropsession():
  session.pop('user', None)
  return render_template('index.html')

#End Login part----------------------------------

search = ''

@app.route('/main', methods=['GET','POST'])
def main():
  
  # if search field is filled up
  if request.form.get("search") != None:
    search = request.form.get("search")
    search = "%" + search + "%"
    
    # execute this SQL command and return the result of the search
    #search_res = db.execute("SELECT * FROM books WHERE Author = :search OR Title = :search OR Isbn = :search",{"search": search}).fetchall()
    search_res = db.execute("SELECT * FROM books WHERE Author LIKE :search OR Title LIKE :search OR Isbn LIKE :search",{"search": search}).fetchall()
    
    # if result exists, shows in the page, otherwise return message 
    if len(search_res) != 0:
      return render_template('main.html', books=search_res)
    else:
      return render_template('main.html', message='No Books found.')
  else:
    return render_template('main.html')


@app.route('/books/<book_id>')
def books(book_id):
  book = db.execute("SELECT * FROM books WHERE id = :id",{"id":book_id}).fetchone()
  
  reviews = db.execute("SELECT * FROM REVIEWS WHERE book_id = :book_id",{"book_id":book_id}).fetchall()

  return render_template("book.html", book=book, reviews=reviews)


# Add book review
@app.route('/books/<book_id>', methods=['POST'])
def add_review(book_id):
  
  user_id=2
  rating = request.form.get("rating")
  comments = request.form.get("comments")
  db.execute("INSERT INTO REVIEWS (book_id,user_id,rating,comments) VALUES (:book_id, :user_id, :rating, :comments)", {"book_id":book_id, "user_id":user_id, "rating":rating, "comments":comments})
  db.commit()

  return redirect(url_for('books',book_id=book_id))

@app.route('/books/<book_id>/delete', methods=['POST'])
def delete_review():
    if request.method == 'POST':
        return redirect(url_for('delete_review'))

if __name__ == '__main__':
  app.run(debug=True)
# @app.route('/profile')
# @login_required
# def profile():
#   return render_template('profile.html', name=current_user.name)

