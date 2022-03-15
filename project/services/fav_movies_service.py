from project.dao.favorite_movie import FavoriteMovieDAO
from project.exceptions import ItemNotFound
from project.schemas.movie import MovieSchema
from project.services.base import BaseService


class FavoriteMoviesService(BaseService):

    def get_by_user_id(self, user_id):
        """
        Получаем все фильмы, добавленные в список любимых.
        Param user_id: id пользователя.
        """
        movies = FavoriteMovieDAO(self._db_session).get_by_user_id(user_id)
        if not movies:
            raise ItemNotFound
        return MovieSchema(many=True).dump(movies)

    def create(self, user_id, mov_id):
        """
        Добавляем фильм в список любимых.
        Param user_id: id пользователя.
        Param movie_id: id фильма.
        """
        movie = FavoriteMovieDAO(self._db_session).create(user_id, mov_id)
        return MovieSchema().dump(movie)

    def delete(self, user_id, mov_id):
        """
        Удаляем фильм из списка любимых.
        Param user_id: id пользователя.
        Param movie_id: id фильма.
        """
        return FavoriteMovieDAO(self._db_session).delete(user_id, mov_id)
