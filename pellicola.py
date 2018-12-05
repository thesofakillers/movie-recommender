from flask import Flask, render_template, url_for
app = Flask(__name__)

#<section>~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~Routes~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# website home page
@app.route("/")
def home():
    return render_template('home.html')

# where personal profile is maintained with movie ratings
@app.route("/profile")
def profile():
    return render_template('profile.html', title = 'Profile')

# where movie reccomendations will be handled
@app.route("/reccomend")
def reccomend():
    return render_template('recommend.html', title = 'For You')
#</section> End of Routes

# to allow server to be run with "python pellicola.py" -- no need for ENV vars
if __name__ == '__main__':
    app.run(debug=True)
