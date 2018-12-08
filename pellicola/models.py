"""
Maintains the class definitions (i.e. tables) for the models in the Database
"""


from pellicola import db


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
