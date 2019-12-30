import json
import os
import requests
from flask import (Flask, g, jsonify, redirect, render_template,
                   request, session, url_for)
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
  g.user_id = None

  if 'user_id' in session:
    g.user_id = session['user_id']

#Login page
@app.route('/', methods=['GET','POST'])
def index():
  if request.method == 'POST':
    session.pop('user_id', None)

    user_id = request.form.get('user_id')
    password = request.form.get('password')
    
    rows = db.execute("SELECT * FROM USERS WHERE USER_ID = :user_id AND password = :password",{"user_id" : user_id, "password" : password}).fetchall()

    if len(rows) != 0:
      session['user_id'] = user_id

      return redirect(url_for('main'))
    else:
      return render_template('index.html', message="Wrong username or password, please try again")
  return render_template('index.html')

#Register a new account
@app.route('/register', methods=['GET', 'POST'])
def register():
    session.pop('user_id', None)
    if request.method == 'POST':
      try:
        user_id = request.form.get('user_id')
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        db.execute("INSERT INTO USERS (user_id, name, email, password) VALUES (:user_id, :name, :email, :password)", {"user_id":user_id, "name":name, "email":email, "password":password})

        db.commit()
      except:
        return render_template('register.html', message="Unable to retrieve the data")
      return render_template('index.html',message="Your account has been created successfully. Please Sign In")
    return render_template('register.html')

#Main page - Search books
@app.route('/main', methods=['GET','POST'])
def main():
  if g.user_id:

    #Verify if search field has been filled up
    if request.form.get("search") != None:
      search = request.form.get("search")
      
      #Return the result of the search - Matches regular expression, case insensitive
      search_res = db.execute("SELECT * FROM books WHERE Author ~* :search OR Title ~* :search OR Isbn ~* :search",{"search": search}).fetchall()
      
      #If books found, return the list of books, otherwise return message 
      if len(search_res) != 0:
        return render_template('main.html', books=search_res,  user_id=session['user_id'])
      else:
        return render_template('main.html', message='No Books found.',  user_id=session['user_id'])
    else:
      return render_template('main.html', user_id=session['user_id'])
  return redirect(url_for('index'))

#Book details
@app.route('/books/<book_id>')
def books(book_id):
  if g.user_id:
    #Get book details
    book = db.execute("SELECT * FROM books WHERE id = :id",{"id":book_id}).fetchone()
    
    #Get book reviews
    reviews = db.execute("SELECT * FROM REVIEWS INNER JOIN USERS ON REVIEWS.USER_ID = USERS.user_id WHERE book_id = :book_id",{"book_id":book_id}).fetchall()

    #Verify if user has already added a veview for the book. Only 1 review per book alowed. 
    my_review = db.execute("SELECT * FROM reviews INNER JOIN users ON reviews.user_id = users.user_id WHERE users.user_id = :g_user_id AND reviews.book_id = :book_id ", {"g_user_id" : g.user_id, "book_id" : book_id}).fetchone()
    
    #GoodReaders API - Get 'average rating' and 'number of reviews' from Goodreaders website
    res = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key":"YnFHygqrnya41GvsYCSmQ","isbns": book.isbn})
    data = res.json()
    average_rating = data['books'][0]['average_rating']
    work_ratings_count = data['books'][0]['work_ratings_count']

    # Flag for enabling and disabling new reviews
    if (my_review) != None:
      enable_review = True
    else:
      enable_review = False
    return render_template("book.html", book=book, reviews=reviews, user_id=g.user_id, enable_review=enable_review, average_rating=average_rating, work_ratings_count=work_ratings_count)
  return redirect(url_for('index'))

#Add a new book review
@app.route('/books/<book_id>', methods=['POST'])
def add_review(book_id):
  if g.user_id:
    rating = request.form.get("rating")
    comments = request.form.get("comments")
    db.execute("INSERT INTO REVIEWS (book_id,user_id,rating,comments) VALUES (:book_id, :user_id, :rating, :comments)", {"book_id":book_id, "user_id":g.user_id, "rating":rating, "comments":comments})
    db.commit()
    return redirect(url_for('books',book_id=book_id))
  return redirect(url_for('index'))

#Delete the book review
@app.route('/books/<book_id>/<review_id>/delete', methods=['GET'])
def delete_review(book_id, review_id):
    if g.user_id:
      db.execute("DELETE FROM REVIEWS WHERE REVIEWS.ID = :review_id", {"review_id" : review_id})
      db.commit()
      return redirect(url_for('books', book_id = book_id))
    return redirect(url_for('index'))

#Log out from the application
@app.route('/dropsession')
def dropsession():
    session.pop('user_id', None)
    return redirect(url_for('index'))

#API - Return details for the book
@app.route('/api/<isbn>')
def isbn_api(isbn):

  #Get Book details
  book_res = db.execute("SELECT * FROM books WHERE Isbn = :isbn",{"isbn": isbn}).fetchone()

  if book_res is None:
    # Return Error if ISBN doens't exist
    return jsonify({"Error":"Error, invalid isbn"}), 422
  else:
    #Get Reviews count
    review_count = db.execute("SELECT COUNT(*) FROM reviews WHERE book_id = :book_id",{"book_id":book_res.id}).fetchone()
  
    #Get Average Score
    average_score = db.execute("SELECT ROUND(AVG(rating),1) FROM reviews WHERE book_id = :book_id GROUP BY book_id",{"book_id":book_res.id}).fetchone()
    
    #Return 0 if the average scope doesn't exist
    if average_score is None:
      average_score = 0,0

    # Create json output
    return jsonify({
      "title": book_res.title,
      "author": book_res.author,
      "year": int(book_res.year),
      "isbn": book_res.isbn,
      "review_count": review_count[0],
      "average_score": float(average_score[0])
    })

if __name__ == '__main__':
  app.run(debug=True)