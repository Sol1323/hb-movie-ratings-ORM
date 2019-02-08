"""Movie Ratings."""

from jinja2 import StrictUndefined

from flask import (Flask, render_template, redirect, request, flash,
                    session)
from flask_debugtoolbar import DebugToolbarExtension

from model import User, Rating, Movie, connect_to_db, db


app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

# Normally, if you use an undefined variable in Jinja2, it fails
# silently. This is horrible. Fix this so that, instead, it raises an
# error.
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    """Homepage."""
    return render_template('homepage.html')


@app.route('/register', methods=['GET'])
def register_form():

    return render_template('register_form.html')


@app.route('/register', methods=['POST'])
def register_process():

    # bracket notation since dictionary format
    # we are not using request.form.get because of the object structure created by model.py (Class objects)
    email = request.form["email"]
    password = request.form["password"]
    # converted to integer for easy addition to our database for that column type (property)
    age = int(request.form["age"])
    zipcode = request.form["zipcode"]

    new_user = User(email=email, password=password, age=age, zipcode=zipcode)

    # similar code as what would be entered into the terminal
    # SQL Alchemy
    new_user_email = User.query.filter(User.email == email).first()

    if new_user_email == None:
        db.session.add(new_user)
        db.session.commit()
        flash(f"User {email} added.")
    else:
        flash(f"{email} is already registered.")

    return redirect('/login')


@app.route('/login', methods=['GET'])
def login_form():

    return render_template('login_form.html')


# @app.route

if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True
    # make sure templates, etc. are not cached in debug mode
    app.jinja_env.auto_reload = app.debug

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(port=5000, host='0.0.0.0')
