#<section>~~~~~~~~~~~~~~~~~~~~~~~~~~~~~Imports~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
from flask import Flask, render_template, url_for, flash, redirect
from flask_sqlalchemy import SQLAlchemy
from forms import RegistrationForm, LoginForm
import sys  # for printing
#</section> End of Imports


# create flask app instance
app = Flask(__name__)

# secret key for security -- will change to environment variable approach later
app.config['SECRET_KEY'] = '49771b76aa833ea4d801e6398d51f3b7'
# sets database path
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

# <section>~~~~~~~~~~~~~~~~~~~~~~~~~Database Settings~~~~~~~~~~~~~~~~~~~~~~~~~~~
# creates database instance
db = SQLAlchemy(app)

#   <section>~~~~~~~~~~~~~~~~~~~~~~~Database Tables~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


class User(db.Model):
    """
    Each user will mandatorily have an id and image
    Username/Email/passwords are optional since we are feeding the DB with a
    series of users which are missing this data
    """
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    username = db.Column(db.String(20), unique=True, nullable=True)
    email = db.Column(db.String(254), unique=True, nullable=True)
    image_file = db.Column(db.String(20), unique=False,
                           nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=True)

    def __repr__(self):
        """Define what the class should look like when printing out instance"""
        return "User({})".format(self.id)


class Rating(db.Model):
    """
    Handles the many to many relationship between users and films
    Each rating will mandatorily have
    -a user who has placed the rating (FK) (PK)
    -a movie which is being rated (FK) (PK)
    -a score describing the value of the rating
    """
    user_id = db.Column(db.Integer, db.ForeignKey(
        'user.id'), nullable=False, primary_key=True)
    movie_id = db.Column(db.Integer, db.ForeignKey(
        'movie.id'), nullable=False, primary_key=True)
    score = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        """Define what the class should look like when printing out instance"""
        return "Rating({}, {}, {})".format(self.user_id, self.movie_id, self.score)

class Movie(db.Model):
    """
    Each movie will also also have a title and be part of a genre
    """
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    genre = db.Column(db.String(20), nullable=False)

    def __repr__(self):
        """Define what the class should look like when printing out instance"""
        return "Movie({}, {})".format(self.id, self.title)
#   </section> End of Database Tables
# </section> End of Database Settings


#<section>~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~Routes~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


@app.route("/home")
@app.route("/")
# website home page
def home():
    return render_template('home.html')


@app.route("/profile")
# where personal profile is maintained with movie ratings
def profile():
    return render_template('profile.html', title='Profile')


@app.route("/browse")
# where user may browse movies and rate them
def browse():
    return render_template('browse.html', title='Browse')


@app.route("/recommend")
# where movie reccomendations will be handled
def recommend():
    return render_template('recommend.html', title='For You')


@app.route("/register", methods=['GET', 'POST'])
# where registration will be handled
def register():
    # create form instance
    form = RegistrationForm()
    # if we receive a POST and it passes validations (set in RegistrationForm)
    if form.validate_on_submit():
        # create a succesful alert message
        flash("account created for {}!".format(form.username.data), "success")
        # and redirect the user home
        return redirect(redirect(url_for('home')))
    # render register.html at this particular route (GET)
    return render_template('register.html', title="Register", form=form)


@app.route("/login", methods=['GET', 'POST'])
# where logging in will be handled
def login():
    form = LoginForm()
    if form.validate_on_submit():
        # if username and password match
        #    return(redirect(url_for('home')))
        # else:
        #     flash('unsuccesful login', 'danger')
        pass
    return render_template('login.html', title="Log In", form=form)
#</section> End of Routes


# to allow server to be run with "python pellicola.py" -- no need for ENV vars
if __name__ == '__main__':
    app.run(debug=True)
