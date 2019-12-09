import os
import requests
import json
from helpers import *

from flask import Flask, session, render_template, request, redirect, url_for, Markup, jsonify
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))


@app.route("/", methods=["GET", "POST"])
@login_required
def index():
    username = session['username']
    session["books"] = []
    if request.method == "POST":
        message = ('')
        text = request.form.get('text')
        data = db.execute("SELECT * FROM books WHERE author iLIKE '%"+text +
                          "%' OR title iLIKE '%"+text+"%' OR isbn iLIKE '%"+text+"%'").fetchall()
        for x in data:
            session['books'].append(x)
        if len(session["books"]) == 0:
            message = ('Nothing found. Try again.')
    return render_template("index.html", data=session['books'], username=username)




@app.route("/api/<string:isbn>")
@login_required
def api(isbn):
    data = db.execute(
        "SELECT * FROM books JOIN reviews_games ON books.isbn = :isbn", {"isbn": isbn}).fetchall()
    if len(data) < 1:
        return render_template('404.html')
    return jsonify({
        "title": data[0].title,
        "author": data[0].author,
        "year": data[0].year,
        "isbn": isbn,
        "review_count": len([x.rating for x in data]),
        "average_score": sum([x.rating for x in data])/len([x.rating for x in data])
    })


@app.route("/login", methods=["GET", "POST"])
def login():
    log_in_message = ""
    if request.method == "POST":
        email = request.form.get('email')
        userPassword = request.form.get('userPassword')
        emailLogIn = request.form.get('emailLogIn')
        userPasswordLogIn = request.form.get('userPasswordLogIn')

        # print(email, userPassword, userPasswordLogIn, emailLogIn)
        if emailLogIn == None:  # registration
            data = db.execute("SELECT username FROM users_games").fetchall()
            for i in range(len(data)):
                if data[i]["username"] == email:
                    log_in_message = "Sorry. Username already exist"
                    return render_template('login.html', log_in_message=log_in_message)
            db.execute("INSERT INTO users_games (username,password) VALUES (:a,:b)", {"a": email, "b": userPassword})
            db.commit()
            log_in_message = "Success! You can log in now."
        else:  # registration
            data = db.execute(
                "SELECT * FROM users_games WHERE username = :a", {"a": emailLogIn}).fetchone()
            if data != None:
                if data.username == emailLogIn and data.password == userPasswordLogIn:
                    session["username"] = emailLogIn
                    return redirect(url_for("index"))
                else:
                    log_in_message = "Wrong email or password. Try again."
            else:
                log_in_message = "Wrong email or password. Try again."
    return render_template('login.html', log_in_message=log_in_message)


@app.route("/register", methods=["GET", "POST"])
def register():
    log_in_message = ""
    return render_template('register.html', log_in_message=log_in_message)


@app.route("/games", methods=["GET", "POST"])
def games():
    log_in_message = ""
    if session.get("username") is None:
        username=None
    else:
        username=session['username']
    return render_template('games.html', log_in_message=log_in_message, username=username)


@app.route("/contact", methods=["GET", "POST"])
def contact():
    log_in_message = ""
    if session.get("username") is None:
        username=None
    else:
        username=session['username']
    return render_template('contact.html', log_in_message=log_in_message, username=username)


@app.route("/gamesingle", methods=["GET", "POST"])
def gamesingle():
    warning = ""
    isbn="038079527"
    username = session.get('username')
    session["reviews_games"] = []
    secondreview = db.execute("SELECT * FROM reviews_games WHERE isbn = :isbn AND username= :username", {
                              "username": username, "isbn": isbn}).fetchone()
    if request.method == "POST" and secondreview == None:
        review = request.form.get('textarea')
        rating = request.form.get('stars')
        db.execute("INSERT INTO reviews_games (isbn, review, rating, username) VALUES (:a,:b,:c,:d)", {
                   "a": isbn, "b": review, "c": rating, "d": username})
        db.commit()
    if request.method == "POST" and secondreview != None:
        warning = "Sorry. You cannot add second review."

    reviews_games=db.execute("SELECT * FROM reviews_games WHERE isbn = :isbn",{"isbn":isbn}).fetchall() 
    for y in reviews_games:
        session['reviews_games'].append(y) 
    data = db.execute("SELECT * FROM books WHERE isbn = :isbn",
                      {"isbn": isbn}).fetchone()
    return render_template('gamesingle.html',  data=data,reviews=session['reviews_games'], username=username)

@app.route("/easygame", methods=["GET", "POST"])
def easygame():
    warning = ""
    isbn="1416949658"
    username = session.get('username')
    session["reviews_games"] = []
    secondreview = db.execute("SELECT * FROM reviews_games WHERE isbn = :isbn AND username= :username", {
                              "username": username, "isbn": isbn}).fetchone()
    if request.method == "POST" and secondreview == None:
        review = request.form.get('textarea')
        rating = request.form.get('stars')
        db.execute("INSERT INTO reviews_games (isbn, review, rating, username) VALUES (:a,:b,:c,:d)", {
                   "a": isbn, "b": review, "c": rating, "d": username})
        db.commit()
    if request.method == "POST" and secondreview != None:
        warning = "Sorry. You cannot add second review."

    reviews_games=db.execute("SELECT * FROM reviews_games WHERE isbn = :isbn",{"isbn":isbn}).fetchall() 
    for y in reviews_games:
        session['reviews_games'].append(y) 
    data = db.execute("SELECT * FROM books WHERE isbn = :isbn",
                      {"isbn": isbn}).fetchone()
    return render_template('easygame.html',  data=data,reviews=session['reviews_games'],username=username)


@app.route("/logout")
def logout():
    # global username
    session.clear()
    return redirect(url_for("login", username=None))
