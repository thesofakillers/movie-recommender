# Movie Reccomender
The website has 3 main sections: Browse, Profile and Recommendations, in addition to Login/out functionality.
- Browse: presents table of all database movies which user can interact with by submitting ratings.
- Profile: maintains user profile wherein a table containing movies rated by user is presented. User may amend or delete previous ratings.
- Recommendations: provides user with movie recommendations via singular value decomposition of all user ratings. Also provides personalized messages based on username and preferred genres (inferred from ratings).

Database is utilized as this was seen as better suited for reading and writing to tables as it is not done in memory.

Pandas and numpy are instead utilized for data manipulation.

## Pre-Requisites
This work is made for [Python 3.5](https://www.python.org/downloads/release/python-350/) and up.

The following packages should be installed:
- [NumPy](http://www.numpy.org/)
- [Pandas](https://pandas.pydata.org/)
- [Flask](http://flask.pocoo.org/)
- [flask_sqlalchemy](http://flask-sqlalchemy.pocoo.org/2.3/)
- [flask_bcrypt](https://flask-bcrypt.readthedocs.io/en/latest/)
- [flask_login](https://flask-login.readthedocs.io/en/latest/)
- [flask_wtf](https://flask-wtf.readthedocs.io/en/stable/)

These can all be installed via [pip](https://pypi.org/project/pip/) with `pip3 install --user <package_name>`.

## Usage
1. In a shell, ensure you are in [movie-recommender/](/../../).
2. Enter `python3 run.py`.
3. In a browser, navigate to the address shown in the terminal, usually `http://127.0.0.1:5000/`
4. The website itself has the rest of the instructions
5. NB, you need to create an account to access most features.
