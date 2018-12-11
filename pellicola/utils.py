from pellicola.models import Rating, User, Movie, Genre
from pellicola import app, db, bcrypt


def rate_movie(movie_id, user, score):
    """
    Creates new rating for a movie by a user
    Input:
    -movie_id: Integer corresponding to the ID identifying movie being rated
    -user: User model instance that has rated the movie
    -score: Float corresponding to the score that the user has given the movie

    Output:
    -rating: Rating model instance corresponding to the new rating
    """
    # remove previous rating for this movie by this user from database
    Rating.query.filter_by(movie_id=movie_id,
                           user_id=user.id).delete()
    # add rating to database
    # create rating instance
    rating = Rating(user_id=user.id,
                    movie_id=movie_id, score=score)
    # associate movie with it
    rating.movie = Movie.query.filter_by(id=movie_id).first()
    # append rating to user
    user.movies.append(rating)
    db.session.commit()
    return rating

def submit_form_rating(req, user):
    """
    Submits a rating from a form to the database
    Input:
    -req: the request object incoming from the form
    -user: the User model instance that has submitted the rating
    Output:
    -rating: Rating model instance corresponding to the new rating
    """
    movie_id, score = get_form_info(req)
    return rate_movie(movie_id, user, score)


def get_form_info(req):
    """
    Extracts movie ID and score from a submitted form
    """
    movie_id = int(req.form['movie_id'])
    score = float(req.form['rating_slider'])
    return movie_id, score
