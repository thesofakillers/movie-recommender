import pandas as pd
from pellicola import app, db
import numpy as np
from scipy.sparse.linalg import svds


def get_utility_matrix(RatingModel):
    """
    Creates the ratings utility matrix

    Inputs:
    -RatingModel: SQL Alchemy Rating Model (usually imported)

    Outputs:
    -utility_matrix_numpy: Numpy array corresponding to the ratings utility_matrix
    """
    # getting all ratings from database and storing these in a 3 X N list
    query = [[rating.user_id, rating.movie_id, rating.score]
             for rating in RatingModel.query.all()]
    # where N is the number of ratings

    # converting query into DataFrame
    ratings_df = pd.DataFrame(query)
    # providing column names to Dataframe
    ratings_df.columns = RatingModel.__table__.columns.keys()

    # creating utility matrix for user ratings of movies from ratings_df
    utility_matrix = ratings_df.pivot(
        index="user_id", columns='movie_id', values="score")

    return utility_matrix


def make_predictions(utility_matrix):
    """
    Creates a prediction matrix corresponding to the rating utility matrix
    utilizing singular value decomposition

    Inputs:
    -utility_matrix: Pandas dataframe corresponding to the ratings utility_matrix

    Outputs:
    -prediction_matrix: Pandas dataframe corresponding to the prediction matrix
    described above
    """
    # get each user's mean rating
    user_means = utility_matrix.mean(axis=1)
    # normalizing the utility_matrix to remove scale bias
    utility_matrix = utility_matrix.sub(user_means, axis=0)

    # setting normalized NaNs as 0
    utility_matrix = utility_matrix.fillna(0)
    # converting to numpy array
    utility_matrix_numpy = utility_matrix.values

    # perform singular value decomposition
    user_feat, singulars, movie_feat_dag = svds(utility_matrix_numpy, k=50)
    # reformatting singulars so that it is a diagonal matrix, as it should be
    singulars = np.diag(singulars)

    # obtaining predicted_ratings
    prediction_matrix = pd.DataFrame(np.dot(
        np.dot(user_feat, singulars), movie_feat_dag), columns=utility_matrix.columns)

    # Fixing index so that it matches with user_id
    prediction_matrix.index += 1  # shifting up one
    prediction_matrix.index = prediction_matrix.index.rename('user_id')

    # de-meaning
    prediction_matrix = prediction_matrix.add(user_means, axis=0)

    return prediction_matrix


def get_recommended_movies(prediction_matrix, utility_matrix, user_id):
    """
    Gets a list of recommended movie_ids for a given user given a prediction_matrix

    Inputs:
    -prediction_matrix: Pandas dataframe containung predicted ratings of each
    movie for each user
    -utility_matrix: Pandas dataframe corresponding to the ratings utility_matrix
    -user_id: Integer corresponding to the ID of the user asking for recommendations

    Outputs:
    -recommendations: sorted Pandas Series of recommended movies, with indices
    corresponding to movie ID and values to predicted rating
    """
    # sort predictions for specific user by descending rating
    recommended_movies = prediction_matrix.loc[user_id].sort_values(
        ascending=False)

    # get ids of movies user has already rated
    mask = utility_matrix.loc[user_id].notna()
    rated = utility_matrix.loc[user_id][mask.values].index.tolist()

    # remove already rated movies from recommended list
    recommended_movies = recommended_movies.drop(rated)

    return recommended_movies


from pellicola.models import Rating


def get_recommendations(RatingModel, user_id):
    """
    Gets a list of recommended movie_ids for a given user

    Inputs:
    -RatingModel: SQL Alchemy Rating Model (usually imported)
    -user_id: Integer specifying id of user asking for recommendations

    Outputs:
    -recommendations: sorted Pandas Series of recommended movies, with indices
    corresponding to movie ID and values to predicted rating
    """
    # calculate utility matrix
    util_matrix = get_utility_matrix(RatingModel)
    # utilize it to calculate prediction matrix
    pred_mat = make_predictions(util_matrix)
    # get sorted list of recommendations from these two for specific user
    recommendations = get_recommended_movies(pred_mat, util_matrix, user_id)
    return recommendations


# rec_movies = get_recommendations(Rating, 611)
#
# movie_ids = rec_movies.index.tolist()
#
# for i, v in rec_movies.head().items():
#     print(i, v)
