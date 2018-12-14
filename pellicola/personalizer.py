"""
Module containing functions/objects having to do with personalization logic
"""

from collections import Counter
import random
from flask import Markup

def determine_top_genres(RatingModel, GenreModel, user_id):
    # get all user ratings
    ratings = RatingModel.query.filter_by(user_id=user_id).all()
    # get movie_ids corresponding to these ratings
    movie_ids = [rating.movie_id for rating in ratings]
    # get genres of each of these movies
    movie_genres = GenreModel.query.filter(
        GenreModel.movie_id.in_(movie_ids)).all()
    # create a list of genres of each film (including repetitions)
    genres = [genreinstance.genre for genreinstance in movie_genres]
    # count occurrence of each genre. return sorted dictionary
    return Counter(genres).most_common(3)


genre_thing_dict = {"Action": "John McClane",
"Adventure":"Frodo Baggins",
"Animation":"Hayao Miyazaki",
"Children's":"Disney",
"Comedy":"Jim Carrey",
"Crime":"Joe Pesci",
"Documentary":"David Attenborough",
"Drama":"Requiem For a Dream",
"Fantasy":"Falkor",
"Film-Noir": "Sam Spade",
"Horror":"Freddy Krueger",
"Musical":"Danny Zuko",
"Mystery":"Sherlock Holmes",
"Romance":"William Darcy",
"Sci-Fi":"Spock",
"Thriller":"Hannibal Lecter",
"War":"Private Ryan",
"Western":"Sergio Leone"
}


def construct_personalized_message(RatingModel, GenreModel, user_instance):
    # get 1 of 3 top genres that are relevant to the user given their rated films
    relevant_genre = random.choice(
        determine_top_genres(RatingModel, GenreModel, user_instance.id))[0]
    # get a link that may interest user
    relevant_genre_link = "https://twitter.com/search?l=&q=%22{}%22%20film\
    %20OR%20movie%20OR%20actor%20OR%20actress%20OR%20director%20OR%20star\
    %20OR%20hollywood%20OR%20producer\
    %20-live&src=typd&lang=en-gb".format(relevant_genre)
    # get a relevant person from that genre that may interest user
    relevant_person = genre_thing_dict[relevant_genre]
    # get a relvant link to that person
    relevant_person_link = 'https://www.google.com/search?q={}'.format(
        relevant_person)
    # construct personalized message
    return Markup("Hey there {0}, we noticed there's a bit of \
    <a href='{1}' target='_blank'>{2}</a> in you - you may be interested in \
    <a href='{3}' target='_blank'>these tweets </a>".format(
                                                    user_instance.username,
                                                    relevant_person_link,
                                                    relevant_person,
                                                    relevant_genre_link
                                                    ))
