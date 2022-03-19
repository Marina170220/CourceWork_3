from sqlalchemy import desc
from sqlalchemy.orm.scoping import scoped_session

from project.dao.models import Movie, Genre, Director, User


class MovieDAO:
    def __init__(self, session: scoped_session):
        self._db_session = session

    def get_one_by_id(self, pk):
        """
        Получаем фильм из БД по его id.
        Param pk: id фильма.
        Return: фильм из БД если найден, либо None.
        """
        return self._db_session.query(Movie).filter(Movie.id == pk).one_or_none()

    def get_all(self):
        """
        Получаем все фильмы из БД.
        Return: список всех фильмов из БД.
        """
        return self._db_session.query(Movie).all()

    def get_by_limit(self, limit, offset, status):
        """
        Получаем все фильмы из БД с учётом ограничений по выдаче.
        Если ограничений по выдаче нет, возвращаем все записи.
        Param limit: количество фильмов на одной странице выдачи.
        Param offset: количество фильмов, которое нужно пропустить перед выводом.
        Param status: если он присутствует и имеет значение new — возвращаем записи в отсортированном виде
        (самые свежие), иначе возвращаем в том порядке, в котором они лежат в базе.
        Return: список всех фильмов из БД с учётом лимита и отступа.
        """
        if limit > 0 and status == 'new':
            return self._db_session.query(Movie).order_by(desc(Movie.year)).limit(limit).offset(offset).all()
        elif limit > 0:
            return self._db_session.query(Movie).limit(limit).offset(offset).all()
        elif status == 'new':
            return self._db_session.query(Movie).order_by(desc(Movie.year)).all()
        else:
            return self.get_all()

    def get_by_director(self, dir_id):
        """
        Получаем все фильмы выбранного режиссёра.
        Param dir_id: id режиссёра.
        Return: список всех фильмов выбранного режиссёра.
        """
        return self._db_session.query(Movie).filter(Movie.director_id == dir_id).all()

    def get_by_genre(self, gen_id):
        """
        Получаем все фильмы выбранного жанра.
        Param gen_id: id жанра.
        Return: список всех фильмов выбранного жанра.
        """
        return self._db_session.query(Movie).filter(Movie.genre_id == gen_id).all()

    def get_by_year(self, year):
        """
        Получаем все фильмы выбранного года.
        Param year: год выхода фильма.
        Return: список всех фильмов выбранного года.
        """
        return self._db_session.query(Movie).filter(Movie.year == year).all()

    def get_by_favorite_genre(self, user_id):
        """
        Получаем все фильмы, относящиеся к любимому жанру, указанному в карточке пользователя.
        Param user_id: id пользователя.
        Return: список всех фильмов, относящихся к любимому жанру пользователя.
        """
        return self._db_session.query(Movie).select_from(User, Genre).filter(Movie.genre_id == Genre.id,
                                                                             User.favorite_genre_id == Genre.id,
                                                                             User.id == user_id).all()
