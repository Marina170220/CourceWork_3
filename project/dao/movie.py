from sqlalchemy import desc
from sqlalchemy.orm.scoping import scoped_session

from project.dao.models import Movie
from project.dao.models import FavoriteMovie


class MovieDAO:
    def __init__(self, session: scoped_session):
        self._db_session = session

    def get_one_by_id(self, pk):
        return self._db_session.query(Movie).filter(Movie.id == pk).one_or_none()

    def get_all(self):
        return self._db_session.query(Movie).all()

    def get_by_filter(self, limit, offset, status):
        if limit > 0 and status == 'new':
            return self._db_session.query(Movie).order_by(desc(Movie.year)).limit(limit).offset(offset).all()
        elif limit > 0:
            return self._db_session.query(Movie).limit(limit).offset(offset).all()
        elif status == 'new':
            return self._db_session.query(Movie).order_by(desc(Movie.year)).all()

    def get_by_director(self, dir_id):
        return self._db_session.query(Movie).filter(Movie.director_id == dir_id).all()

    def get_by_genre(self, gen_id):
        return self._db_session.query(Movie).filter(Movie.genre_id == gen_id).all()

    def get_by_year(self, year):
        return self._db_session.query(Movie).filter(Movie.year == year).all()

    def get_favorite(self, user_id):
        return self._db_session.query(Movie).filter(
            FavoriteMovie.movie_id == Movie.id, FavoriteMovie.user_id == user_id).all()


