from unittest.mock import Mock, patch
import pytest

from project.dao.models import Movie
from project.services import MoviesService
from project.schemas.movie import MovieSchema
from project.exceptions import ItemNotFound


class TestMoviesService:
    @pytest.fixture(autouse=True)
    def service(self, db):
        self.service = MoviesService(db.session)

    @pytest.fixture
    def movie(self, db):
        return Movie(title="test1",
                     description='test1',
                     trailer='test1',
                     year=2020,
                     rating=10,
                     genre_id=1,
                     director_id=1)

    @pytest.fixture
    def filters_dir(self, db):
        filters = {"director_id": 1}
        return filters

    @pytest.fixture
    def filters_gen(self, db):
        filters = {"genre_id": 1}
        return filters

    @pytest.fixture
    def filters_year(self, db):
        filters = {"year": 2020}
        return filters

    @pytest.fixture
    def limits(self, db):
        limits = {"page": 1,
                  "status": "new"}
        return limits

    @pytest.fixture
    def movie_dao_mock(self, movie):
        with patch("project.services.movies_service.MovieDAO") as mock:
            mock.return_value = Mock(
                get_one_by_id=Mock(return_value=MovieSchema().dump(movie)),
                get_all=Mock(return_value=MovieSchema(many=True).dump([movie])),
                get_by_limit=Mock(return_value=MovieSchema(many=True).dump([movie])),
                get_by_director=Mock(return_value=MovieSchema(many=True).dump([movie])),
                get_by_genre=Mock(return_value=MovieSchema(many=True).dump([movie])),
                get_by_year=Mock(return_value=MovieSchema(many=True).dump([movie])),
                get_by_favorite_genre=Mock(return_value=MovieSchema(many=True).dump([movie]))
            )
            yield mock

    def test_get_all_movies(self, movie_dao_mock, movie):
        assert self.service.get_all_movies() == MovieSchema(many=True).dump([movie])
        movie_dao_mock().get_all.assert_called_once()

    def test_get_item_by_id(self, movie_dao_mock, movie):
        assert self.service.get_movie_by_id(movie.id) == MovieSchema().dump(movie)
        movie_dao_mock().get_one_by_id.assert_called_once_with(movie.id)

    def test_get_item_by_id_not_found(self, movie_dao_mock):
        movie_dao_mock().get_one_by_id.return_value = None

        with pytest.raises(ItemNotFound):
            self.service.get_movie_by_id(1)

    def test_get_by_limit(self, movie_dao_mock, limits, movie):
        assert self.service.get_limit_movies(limits) == MovieSchema(many=True).dump([movie])
        movie_dao_mock().get_by_limit.assert_called_once()

    def test_get_by_filters_director(self, movie_dao_mock, movie, filters_dir):
        assert self.service.get_filter_movies(filters_dir) == MovieSchema(many=True).dump([movie])
        movie_dao_mock().get_by_director.assert_called_once()
        movie_dao_mock().get_by_genre.assert_not_called()
        movie_dao_mock().get_by_year.assert_not_called()

    def test_get_by_filters_genre(self, movie_dao_mock, movie, filters_gen):
        assert self.service.get_filter_movies(filters_gen) == MovieSchema(many=True).dump([movie])
        movie_dao_mock().get_by_genre.assert_called_once()
        movie_dao_mock().get_by_director.assert_not_called()
        movie_dao_mock().get_by_year.assert_not_called()

    def test_get_by_filters_year(self, movie_dao_mock, movie, filters_year):
        assert self.service.get_filter_movies(filters_year) == MovieSchema(many=True).dump([movie])
        movie_dao_mock().get_by_year.assert_called_once()
        movie_dao_mock().get_by_genre.assert_not_called()
        movie_dao_mock().get_by_director.assert_not_called()

    def test_get_by_filters_all(self, movie_dao_mock, movie, limits):
        assert self.service.get_filter_movies(limits) == MovieSchema(many=True).dump([movie])
        movie_dao_mock().get_by_year.assert_not_called()
        movie_dao_mock().get_by_genre.assert_not_called()
        movie_dao_mock().get_by_director.assert_not_called()

    def test_get_by_favorite_genre(self, movie_dao_mock, movie):
        assert self.service.get_movies_by_favorite_genre(1) == MovieSchema(many=True).dump([movie])
        movie_dao_mock().get_by_favorite_genre.assert_called_once()
