from flask import Flask
app = Flask(__name__)

#<section>~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~Routes~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# website home page
@app.route("/")
def home():
    return "Home Page"

# where personal profile is maintained with movie ratings
@app.route("/profile")
def profile():
    return "personal profile"

# where movie reccomendations will be handled
@app.route("/reccomend")
def reccomend():
    return "recommendations page"
#</section> End of Routes

# to allow server to be run with "python pellicola.py" -- no need for ENV vars
if __name__ == '__main__':
    app.run(debug=True)
