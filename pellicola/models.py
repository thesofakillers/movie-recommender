"""
Maintains the class definitions (i.e. tables) for the models in the Database
"""
from pellicola import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class Rating(db.Model):
    """
    Handles the many to many relationship between users and films
    Each rating will mandatorily have
    -a user who has placed the rating (FK) (PK)
    -a movie which is being rated (FK) (PK)
    -a score describing the value of the rating
    """
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    movie_id = db.Column(db.Integer, db.ForeignKey(
        'movie.id'), primary_key=True)
    score = db.Column(db.Float)
    user = db.relationship('User', back_populates='movies')
    movie = db.relationship('Movie', back_populates='users')

    def __repr__(self):
        """Define what the class should look like when printing out instance"""
        return "Rating({}, {}, {})".format(self.user_id, self.movie_id, self.score)

class User(db.Model, UserMixin):
    """
    Each user will mandatorily have an id
    Username/Email/passwords are optional since we are feeding the DB with a
    series of users which are missing this data
    Is related to:
    -Movie: Many to Many handled via Rating
    """
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=True)
    email = db.Column(db.String(254), unique=True, nullable=True)
    password = db.Column(db.String(60), nullable=True)
    movies = db.relationship('Rating',
                             back_populates='user', lazy='dynamic')

    def __repr__(self):
        """Define what the class should look like when printing out instance"""
        return "User({})".format(self.id)


class Movie(db.Model):
    """
    Each movie will have a title and be part of one or more genres
    Is related to:
    -MovieGenre: 1 to M
    -User: Many to Many handled via Rating
    """
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    genres = db.relationship('Genre', backref='movie', lazy='dynamic')
    users = db.relationship('Rating',
                             back_populates='movie', lazy = 'dynamic')

    def __repr__(self):
        """Define what the class should look like when printing out instance"""
        return "Movie({}, {})".format(self.id, self.title)


class Genre(db.Model):
    """
    Resolves Many to Many relationship between movies and genres
    Is related to:
    -Movie: M to 1
    """
    genre = db.Column(db.String(100), primary_key=True)
    movie_id = db.Column(db.Integer, db.ForeignKey(
        'movie.id'), primary_key=True)

    def __repr__(self):
        """Define what the class should look like when printing out instance"""
        return "Genre({}, {})".format(self.movie_id, self.genre)
