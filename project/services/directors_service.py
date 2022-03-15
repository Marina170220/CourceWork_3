from project.dao.director import DirectorDAO
from project.exceptions import ItemNotFound
from project.schemas.director import DirectorSchema
from project.services.base import BaseService
from project.config import BaseConfig


class DirectorService(BaseService):

    def get_director_by_id(self, pk):
        """
        Получаем режиссёра по его id.
        Param pk: id режиссёра.
        """
        director = DirectorDAO(self._db_session).get_one_by_id(pk)
        if not director:
            raise ItemNotFound
        return DirectorSchema().dump(director)

    def get_all_directors(self):
        """
        Получаем всех режиссёров.
        """
        directors = DirectorDAO(self._db_session).get_all()
        return DirectorSchema(many=True).dump(directors)

    def get_limit_directors(self, page):
        """
        Получаем всех режиссёров из БД с учётом ограничений по выдаче.
        Param page: номер страницы выдачи.
        """
        limit = BaseConfig.ITEMS_PER_PAGE
        offset = (int(page) - 1) * limit
        directors = DirectorDAO(self._db_session).get_by_limit(limit=limit, offset=offset)
        return DirectorSchema(many=True).dump(directors)
