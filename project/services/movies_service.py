from project.dao.movie import MovieDAO
from project.exceptions import ItemNotFound
from project.schemas.movie import MovieSchema
from project.services.base import BaseService
from project.config import BaseConfig


class MoviesService(BaseService):

    def get_movie_by_id(self, pk):
        """
        Получаем фильм по его id.
        Param pk: id фильма.
        """
        movie = MovieDAO(self._db_session).get_one_by_id(pk)
        if not movie:
            raise ItemNotFound
        return MovieSchema().dump(movie)

    def get_all_movies(self):
        """
        Получаем все фильмы.
        """
        movies = MovieDAO(self._db_session).get_all()
        return MovieSchema(many=True).dump(movies)

    def get_movies_by_favorite_genre(self, pk):
        """
        Получаем все фильмы, относящиеся к любимому жанру, указанному в карточке пользователя.
        Param user_id: id пользователя.
        """
        movies = MovieDAO(self._db_session).get_by_favorite_genre(pk)
        return MovieSchema(many=True).dump(movies)

    def get_limit_movies(self, args):
        """
        Получаем все фильмы с учётом ограничений по выдаче.
        Param args: аргумент, который может содержать номер страницы и/или статус фильма.
        """
        limit = 0
        offset = 0
        status = 'no_status'
        if args.get('page'):
            limit = BaseConfig.ITEMS_PER_PAGE
            offset = (int(args.get('page')) - 1) * limit
        if args.get('status'):
            status = args.get('status')

        movies = MovieDAO(self._db_session).get_by_limit(limit=limit, offset=offset, status=status)
        return MovieSchema(many=True).dump(movies)

    def get_filter_movies(self, filters):
        """
        Получаем все фильмы в соответствии с фильтром.
        Param filters: аргумент, который может содержать id режиссёра, id жанры или год выхода фильма.
        Если фильтров нет, возвращаем все фильмы.
        """
        if filters.get('director_id'):
            movies = MovieDAO(self._db_session).get_by_director(filters['director_id'])
            return MovieSchema(many=True).dump(movies)
        elif filters.get('genre_id'):
            movies = MovieDAO(self._db_session).get_by_genre(filters['genre_id'])
            return MovieSchema(many=True).dump(movies)
        elif filters.get('year'):
            movies = MovieDAO(self._db_session).get_by_year(filters['year'])
            return MovieSchema(many=True).dump(movies)
        else:
            movies = MovieDAO(self._db_session).get_all()
            return MovieSchema(many=True).dump(movies)
