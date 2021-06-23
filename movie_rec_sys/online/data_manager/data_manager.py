#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pandas as pd
from movie_rec_sys.online.data_manager.movie import movie, serialization


class DataManager(object):
    movie_dict = {}
    user_dict = {}

    # 类别 - 电影的倒排索引
    genre_reverse_index_dict = {}  # {"genre': [movie, movie]}

    def load_data(self, movie_data_path: str, link_data_path: str, rating_data_path: str, movie_emb_path: str,
                  user_emb_path: str, movie_redis_key: str, user_redis_key: str):
        self.__load_movie_data(movie_data_path=movie_data_path)

    def __load_movie_data(self, movie_data_path: str):
        # 从movie.csv中加载电影数据
        print("Loading movie data from " + movie_data_path + " ...")
        df = pd.read_csv(movie_data_path, encoding='utf-8')
        for temp in df.to_dict(orient='records'):
            movie_obj = movie()
            movie_id = temp['movieId']
            title = temp['title']
            genres = temp['genres']
            movie_obj.movie_id = int(movie_id)
            release_year = DataManager.parse_release_year(raw_title=title)
            if release_year == -1:
                movie_obj.title = title.strip()
            else:
                movie_obj.title = title.strip()[0:-6].strip()
                movie_obj.release_year = release_year
            if genres.strip():
                genres_list = genres.strip().split('|')
                for genre_temp in genres_list:
                    genre_temp = genre_temp.strip()
                    movie_obj.add_genre(genre_temp)
                    self.genre_reverse_index_dict.setdefault(genre_temp, []).append(movie_obj)
            self.movie_dict[movie_obj.movie_id] = movie_obj

        print("Loading movie data completed. " + str(len(self.movie_dict)) + " movies in total.")

    @staticmethod
    def parse_release_year(raw_title: str):
        raw_title = raw_title.strip()
        if raw_title is None or len(raw_title) < 6:
            return -1
        else:
            year_str = raw_title[-5:-1]
            try:
                return int(year_str)
            except Exception as err:
                return -1

    def get_movies_by_genre(self, genre: str, size: int, sort_by: str):
        if genre and genre in self.genre_reverse_index_dict:
            movies = self.genre_reverse_index_dict[genre]
            if sort_by == 'rating':
                movies.sort(key=lambda x: x.average_rating)
            elif sort_by == 'release_year':
                movies.sort(key=lambda x: x.release_year)
            return movies[0:size]
        return []

    @staticmethod
    def obj2dict(obj):
        if isinstance(obj, list):
            result = []
            for temp in obj:
                obj_serialize = DataManager._obj2dict(temp)
                if obj_serialize:
                    result.append(obj_serialize)
            return result
        else:
            return DataManager._obj2dict(obj)

    @staticmethod
    def _obj2dict(obj: serialization):
        return obj.serialize()


data_manager_holder = DataManager()

if __name__ == '__main__':
    pass
