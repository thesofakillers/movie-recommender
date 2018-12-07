#<section>~~~~~~~~~~~~~~~~~~~~~~~~~~~~~Imports~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
from flask import Flask, render_template, url_for, flash, redirect
from forms import RegistrationForm, LoginForm
import sys #for printing
#</section> End of Imports


# create flask app instance
app = Flask(__name__)

# secret key for security -- will change to environment variable approach later
app.config['SECRET_KEY'] = '49771b76aa833ea4d801e6398d51f3b7'

#<section>~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~Routes~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# website home page
@app.route("/home")
@app.route("/")
def home():
    return render_template('home.html')

# where personal profile is maintained with movie ratings
@app.route("/profile")
def profile():
    return render_template('profile.html', title = 'Profile')

# where user may browse movies and rate them
@app.route("/browse")
def browse():
    return render_template('browse.html', title = 'Browse')

# where movie reccomendations will be handled
@app.route("/recommend")
def reccomend():
    return render_template('recommend.html', title = 'For You')

# where registration will be handled
@app.route("/register", methods =['GET', 'POST'])
def register():
    # create form instance
    form = RegistrationForm()
    # if we receive a POST and it passes validations (set in RegistrationForm)
    if form.validate_on_submit():
        # create a succesful alert message
        flash("account created for {}!".format(form.username.data), "success")
        # and redirect the user home
        return redirect("/")
    # render register.html at this particular route (GET)
    return render_template('register.html',title="Register", form = form)

# where logging in will be handled
@app.route("/login")
def login():
    form = LoginForm()
    return render_template('login.html',title="Log In", form = form)
#</section> End of Routes

# to allow server to be run with "python pellicola.py" -- no need for ENV vars
if __name__ == '__main__':
    app.run(debug=True)
