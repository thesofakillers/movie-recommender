"""
Handles the routing of the web app
"""


from flask import render_template, url_for, flash, redirect
from pellicola import app
from pellicola.forms import RegistrationForm, LoginForm
from pellicola.models import User, Rating, Movie


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
        return redirect(url_for('home'))
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
