from sqlalchemy.orm.scoping import scoped_session

from project.dao.models import Genre


class GenreDAO:
    def __init__(self, session: scoped_session):
        self._db_session = session

    def get_one_by_id(self, pk):
        """
        Получаем жанр из БД по его id.
        Param pk: id жанра.
        """
        return self._db_session.query(Genre).filter(Genre.id == pk).one_or_none()

    def get_all(self):
        """
        Получаем все жанры из БД.
        """
        return self._db_session.query(Genre).all()

    def get_by_limit(self, limit, offset):
        """
        Получаем все жанры из БД с учётом ограничений по выдаче.
        Param limit: количество жанров на одной странице выдачи.
        Param offset: количество жанров, которое нужно пропустить перед выводом.
        """
        return self._db_session.query(Genre).limit(limit).offset(offset).all()
