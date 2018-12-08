"""
Packages the web app
"""


from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

# create flask app instance
app = Flask(__name__)

# secret key for security -- will change to environment variable approach later
app.config['SECRET_KEY'] = '49771b76aa833ea4d801e6398d51f3b7'
# sets database path
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

# creates database instance
db = SQLAlchemy(app)

# create Bcrypt instance
bcrypt = Bcrypt(app)

# create LoginManager instance
login_manager = LoginManager(app)


from pellicola import routes
