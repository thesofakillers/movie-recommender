"""
Handles the routing of the web app
"""


from flask import render_template, url_for, flash, redirect, request
from pellicola import app, db, bcrypt
from pellicola.forms import RegistrationForm, LoginForm
from pellicola.models import ratings, User, Movie, MovieGenre
from flask_login import login_user, current_user, logout_user, login_required

@app.route("/home")
@app.route("/")
# website home page
def home():
    return render_template('home.html')


@app.route("/profile")
@login_required
# where personal profile is maintained with movie ratings
def profile():
    return render_template('profile.html', title='Profile')


@app.route("/browse")
@login_required
# where user may browse movies and rate them
def browse():
    return render_template('browse.html', title='Browse')


@app.route("/recommend")
@login_required
# where movie reccomendations will be handled
def recommend():
    return render_template('recommend.html', title='For You')


@app.route("/register", methods=['GET', 'POST'])
# where registration will be handled
def register():
    # check if user is already logged in
    if current_user.is_authenticated:
        return(redirect(url_for('home')))
    # create form instance
    form = RegistrationForm()
    # if we receive a POST and it passes validations (set in RegistrationForm)
    if form.validate_on_submit():
        # hash password
        hashed_password = bcrypt.generate_password_hash(
            form.password.data).decode('utf-8')
        # create user instance with hashed_password
        user = User(username=form.username.data,
                    email=form.email.data, password=hashed_password)
        # add user to database
        db.session.add(user)
        db.session.commit()
        # create a succesful alert message
        flash("Your account has been created, you may now Log In.", "success")
        # and redirect the user to login page
        return redirect(url_for('login'))
    # render register.html at this particular route (GET)
    return render_template('register.html', title="Register", form=form)


@app.route("/login", methods=['GET', 'POST'])
# where logging in will be handled
def login():
    # check if user is already logged in
    if current_user.is_authenticated:
        return(redirect(url_for('home')))
    # create form instance
    form = LoginForm()
    # if we receive a POST and it passes validations (set in LoginForm)
    if form.validate_on_submit():
        # search for email in database
        user = User.query.filter_by(email=form.email.data).first()
        # check if email exists and whether the passwords match
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            # login user
            login_user(user, remember = form.remember.data)
            # redirect back to where user was trying to go
            next_page = request.args.get('next')
            if next_page: # if the user was tryin to go somewhere
                return redirect(next_page)
            else: # if they weren't just go home
                return redirect(url_for("home"))
        else: # if login fails
            # provide feedback
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title="Log In", form=form)


@app.route("/logout")
@login_required
# where logging out will be handled
def logout():
    logout_user()
    return redirect(url_for("home"))
