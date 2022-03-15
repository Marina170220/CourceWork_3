from sqlalchemy.orm.scoping import scoped_session

from project.dao.models import FavoriteMovie, Movie


class FavoriteMovieDAO:
    def __init__(self, session: scoped_session):
        self._db_session = session

    def get_by_user_id(self, pk):
        """
        Получаем все фильмы, добавленные в список любимых.
        Param pk: id пользователя.
        """
        return self._db_session.query(Movie).select_from(FavoriteMovie).filter(
            FavoriteMovie.user_id == pk, FavoriteMovie.movie_id == Movie.id).all()

    def create(self, user_id, movie_id):
        """
        Добавляем фильм в список любимых.
        Param user_id: id пользователя.
        Param movie_id: id фильма.
        """
        new_movie = FavoriteMovie(user_id=user_id, movie_id=movie_id)
        self._db_session.add(new_movie)
        self._db_session.commit()
        return new_movie

    def delete(self, user_id, movie_id):
        """
        Удаляем фильм из списка любимых.
        Param user_id: id пользователя.
        Param movie_id: id фильма.
        """
        movie = self._db_session.query(FavoriteMovie).filter(FavoriteMovie.user_id == user_id,
                                                             FavoriteMovie.movie_id == movie_id).one_or_none()
        self._db_session.delete(movie)
        self._db_session.commit()
