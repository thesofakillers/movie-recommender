"""
Module utilized to populate SQLAlchemy database from MovieLens csv files
"""
from tabulate import tabulate
from pellicola import db
from pellicola.models import Rating, User, Movie, Genre
import pandas as pd

# get SQL Alchemy engine
engine = db.engine

# specify where csv files are
csv_folder = "ml-latest-small/"

# read the movies csv file
movies_df = pd.read_csv(csv_folder + "movies.csv")
# read the ratings csv file
ratings_df = pd.read_csv(csv_folder + "ratings.csv")

# get rid of unnescessary column
ratings_df = ratings_df.drop(columns=['timestamp'])
# rename columns
ratings_df.columns = ['user_id', 'movie_id', 'score']

# get users dataframe
users_df = ratings_df.user_id.drop_duplicates().to_frame('id')


# create MovieGenre list of dics to then convert to pd dataframe
movie_genre_list = [{'movie_id': row.movieId, 'genre': genre}
                    for _, row in movies_df.iterrows()
                    for genre in row.genres.split('|')]

# MovieGenre dataframe equivalent, ready for sql
movie_genre_df = pd.DataFrame(movie_genre_list)


# rename movie df columns to match Movie SQL model column names
movies_df.columns = Movie.__table__.columns.keys() + ['genres']
# remove unnescessary column
movies_df = movies_df.drop(columns=['genres'])

# writing to database
movies_df.to_sql('movie', con=engine, if_exists='append', index=False)
movie_genre_df.to_sql('genre', con=engine,
                      if_exists='append', index=False)
ratings_df.to_sql('rating', con=engine, if_exists='append', index=False)
users_df.to_sql('user', con=engine, if_exists='append', index=False)
