from sqlalchemy.orm.scoping import scoped_session

from project.dao.models import Director


class DirectorDAO:
    def __init__(self, session: scoped_session):
        self._db_session = session

    def get_one_by_id(self, pk):
        """
        Получаем режиссёра из БД по его id.
        Param pk: id режиссёра.
        """
        return self._db_session.query(Director).filter(Director.id == pk).one_or_none()

    def get_all(self):
        """
        Получаем всех режиссёров из БД.
        """
        return self._db_session.query(Director).all()

    def get_by_limit(self, limit, offset):
        """
        Получаем всех режиссёров из БД с учётом ограничений по выдаче.
        Param limit: количество режиссёров на одной странице выдачи.
        Param offset: количество режиссёров, которое нужно пропустить перед выводом.
        """
        return self._db_session.query(Director).limit(limit).offset(offset).all()
