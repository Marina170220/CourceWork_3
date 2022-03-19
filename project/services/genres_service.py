from project.dao import GenreDAO
from project.exceptions import ItemNotFound
from project.schemas.genre import GenreSchema
from project.services.base import BaseService
from project.config import BaseConfig


class GenresService(BaseService):

    def get_genre_by_id(self, pk):
        """
        Получаем жанр по его id.
        Param pk: id жанра.
        Return: словарь с данными найденного жанра.
        """
        genre = GenreDAO(self._db_session).get_one_by_id(pk)
        if not genre:
            raise ItemNotFound
        return GenreSchema().dump(genre)

    def get_all_genres(self):
        """
        Получаем все жанры.
        Return: список словарей с данными всех жанров.
        """
        genres = GenreDAO(self._db_session).get_all()
        return GenreSchema(many=True).dump(genres)

    def get_limit_genres(self, page):
        """
        Получаем все жанры с учётом ограничений по выдаче.
        Param page: номер страницы выдачи.
        Return: список словарей с данными всех жанров с учётом лимита и отступа.
        """
        limit = BaseConfig.ITEMS_PER_PAGE
        offset = (int(page)-1)*limit
        genres = GenreDAO(self._db_session).get_by_limit(limit=limit, offset=offset)
        return GenreSchema(many=True).dump(genres)
