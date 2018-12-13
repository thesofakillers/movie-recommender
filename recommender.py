import pandas as pd
from pellicola.models import Rating, User, Movie, Genre
from pellicola import app, db
import numpy as np
from scipy.sparse.linalg import svds

# getting all ratings from database and storing these in a 3 X N list
query = [[rating.user_id, rating.movie_id, rating.score]
         for rating in Rating.query.all()]
# where N is the number of ratings

# converting query into DataFrame
ratings_df = pd.DataFrame(query)
# providing column names to Dataframe
ratings_df.columns = Rating.__table__.columns.keys()

# creating utility matrix for user ratings of movies from ratings_df
utility_matrix = ratings_df.pivot(
    index="user_id", columns='movie_id', values="score")

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
predicted_ratings = pd.DataFrame(np.dot(
    np.dot(user_feat, singulars), movie_feat_dag), columns=utility_matrix.columns)

# Fixing index so that it matches with user_id
predicted_ratings.index += 1 # shifting up one
predicted_ratings.index = predicted_ratings.index.rename('user_id')

# de-meaning
predicted_ratings = predicted_ratings.add(user_means, axis=0)



# print(predicted_ratings.loc[611].sort_values(ascending=True))
