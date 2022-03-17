from unittest.mock import Mock, patch
import pytest

from project.dao.models import FavoriteMovie, Movie, User
from project.services import FavoriteMoviesService
from project.schemas.movie import MovieSchema
from project.exceptions import ItemNotFound


class TestFavMoviesService:
    @pytest.fixture(autouse=True)
    def service(self, db):
        self.service = FavoriteMoviesService(db.session)

    @pytest.fixture
    def movie(self, db):
        return Movie(id=1,
                     title="test1",
                     description='test1',
                     trailer='test1',
                     year=2020,
                     rating=10,
                     genre_id=1,
                     director_id=1)

    @pytest.fixture
    def fav_movie(self, db):
        return FavoriteMovie(user_id=1,
                             movie_id=1)

    @pytest.fixture
    def user(self, db):
        return User(id=1,
                    email="test_1@test.su",
                    password="testpass_1",
                    role="testrole_1",
                    name="testname_1",
                    surname="testsurname_1",
                    favorite_genre="testgen_1"
                    )

    @pytest.fixture
    def fav_movie_dao_mock(self, fav_movie, movie, user):
        with patch("project.services.fav_movies_service.FavoriteMovieDAO") as mock:
            mock.return_value = Mock(
                get_by_user_id=Mock(return_value=MovieSchema(many=True).dump([movie])),
                create=Mock(return_value=MovieSchema().dump(movie)),
                delete=Mock(return_value=None)
            )
            yield mock

    def test_get_item_by_id(self, fav_movie_dao_mock, movie, user):
        assert self.service.get_by_user_id(user.id) == MovieSchema(many=True).dump([movie])
        fav_movie_dao_mock().get_by_user_id.assert_called_once_with(movie.id)

    def test_get_item_by_id_not_found(self, fav_movie_dao_mock):
        fav_movie_dao_mock().get_by_user_id.return_value = None

        with pytest.raises(ItemNotFound):
            self.service.get_by_user_id(1)

    def test_create(self, fav_movie_dao_mock, user, movie):
        assert self.service.create(user.id, movie.id) == MovieSchema().dump(movie)
        fav_movie_dao_mock().create.assert_called_once_with(movie.id, user.id)

    def test_delete(self, fav_movie_dao_mock, user, movie):
        assert self.service.delete(user.id, movie.id) is None
        fav_movie_dao_mock().delete.assert_called_once_with(movie.id, user.id)
