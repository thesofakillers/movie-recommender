import pandas as pd
from pellicola.models import Rating, User, Movie, Genre
from pellicola import app, db

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
