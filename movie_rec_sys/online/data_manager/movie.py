#!/usr/bin/env python
# -*- coding: utf-8 -*-


class serialization(object):

    def serialize(self):
        raise NotImplementedError
    raise NotImplemented


class movie(serialization):
    TOP_RATING_SIZE = 10

    movie_id = -1
    title = ''
    release_year = 0
    imdb_id = ''
    tmdb_id = ''
    genres = []

    # 评论人数
    rating_number = 0

    # 平均分
    average_rating = 0

    # embedding of the movie
    emb = None

    # all rating scores list
    ratings = []

    movie_features = {}

    top_ratings = []

    def add_genre(self, genre: str):
        if genre.strip():
            self.genres.append(genre)

    def serialize(self):
        result = {
            'movie_id': self.movie_id,
            'title': self.title,
            'release_year': self.release_year,
            'imdb_id': self.imdb_id,
            'tmdb_id': self.tmdb_id,
            'genres': self.genres
        }
        return result
