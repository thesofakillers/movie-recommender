"""
Maintains the class definitions (i.e. tables) for the models in the Database
"""
from pellicola import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


"""
Handles the many to many relationship between users and films
Each rating will mandatorily have
-a user who has placed the rating (FK) (PK)
-a movie which is being rated (FK) (PK)
-a score describing the value of the rating
"""
ratings = db.Table('ratings',
                   db.Column('user_id', db.Integer, db.ForeignKey(
                       'user.id'), primary_key=True),
                   db.Column('movie_id', db.Integer, db.ForeignKey(
                       'movie.id'), primary_key=True),
                   db.Column('score', db.Float)
                   )


class User(db.Model, UserMixin):
    """
    Each user will mandatorily have an id
    Username/Email/passwords are optional since we are feeding the DB with a
    series of users which are missing this data
    Is related to:
    -Movie: Many to Many handled via ratings
    """
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=True)
    email = db.Column(db.String(254), unique=True, nullable=True)
    password = db.Column(db.String(60), nullable=True)
    movies = db.relationship('Movie',
                             secondary=ratings,
                             back_populates='users')

    def __repr__(self):
        """Define what the class should look like when printing out instance"""
        return "User({})".format(self.id)


class Movie(db.Model):
    """
    Each movie will have a title and be part of one or more genres
    Is related to:
    -MovieGenre: 1 to M
    -User: Many to Many handled via ratings
    """
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    genres = db.relationship('MovieGenre', backref='movie', lazy='dynamic')
    users = db.relationship("User",
                            secondary=ratings,
                            back_populates='movies')

    def __repr__(self):
        """Define what the class should look like when printing out instance"""
        return "Movie({}, {})".format(self.id, self.title)


class MovieGenre(db.Model):
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
        return "MovieGenre({}, {})".format(self.movie_id, self.genre)
