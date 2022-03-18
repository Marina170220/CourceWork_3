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
        """
        return self._db_session.query(Movie).filter(Movie.id == pk).one_or_none()

    def get_all(self):
        """
        Получаем все фильмы из БД.
        Подтягиваем имена режиссёров и названия жанров в соответствии с их id, указанными в карточке фильма.
        """
        return self._db_session.query(Movie).all()

    def get_by_limit(self, limit, offset, status):
        """
        Получаем все фильмы из БД с учётом ограничений по выдаче.
        Подтягиваем имена режиссёров и названия жанров в соответствии с их id, указанными в карточке фильма.
        Если ограничений по выдаче нет, возвращаем все записи.
        Param limit: количество фильмов на одной странице выдачи.
        Param offset: количество фильмов, которое нужно пропустить перед выводом.
        Param status: если он присутствует и имеет значение new — возвращаем записи в отсортированном виде
        (самые свежие), иначе возвращаем в том порядке, в котором они лежат в базе.
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
        Подтягиваем имена режиссёров и названия жанров в соответствии с их id, указанными в карточке фильма.
        Param dir_id: id режиссёра.
        """
        return self._db_session.query(Movie).filter(Movie.director_id == dir_id).all()

    def get_by_genre(self, gen_id):
        """
        Получаем все фильмы выбранного жанра.
        Подтягиваем имена режиссёров и названия жанров в соответствии с их id, указанными в карточке фильма.
        Param gen_id: id жанра.
        """
        return self._db_session.query(Movie).filter(Movie.genre_id == gen_id).all()

    def get_by_year(self, year):
        """
        Получаем все фильмы выбранного года.
        Подтягиваем имена режиссёров и названия жанров в соответствии с их id, указанными в карточке фильма.
        Param year: год выхода фильма.
        """
        return self._db_session.query(Movie).filter(Movie.year == year).all()

    def get_by_favorite_genre(self, user_id):
        """
        Получаем все фильмы, относящиеся к любимому жанру, указанному в карточке пользователя.
        Подтягиваем имена режиссёров и названия жанров в соответствии с их id, указанными в карточке фильма.
        Param user_id: id пользователя.
        """
        return self._db_session.query(Movie).select_from(User, Genre).filter(Movie.genre_id == Genre.id,
                                                                             User.favorite_genre_id == Genre.id,
                                                                             User.id == user_id).all()
