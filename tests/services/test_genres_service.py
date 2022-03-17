from unittest.mock import Mock, patch
import pytest

from project.dao.models import Genre
from project.services import GenresService
from project.schemas.genre import GenreSchema
from project.exceptions import ItemNotFound


class TestGenresService:
    @pytest.fixture(autouse=True)
    def service(self, db):
        self.service = GenresService(db.session)

    @pytest.fixture
    def genre(self, db):
        return Genre(id=1, name="genre_1")

    @pytest.fixture
    def page(self, db):
        return 1

    @pytest.fixture
    def genre_dao_mock(self, genre):
        with patch("project.services.genres_service.GenreDAO") as mock:
            mock.return_value = Mock(
                get_one_by_id=Mock(return_value=GenreSchema().dump(genre)),
                get_all=Mock(return_value=GenreSchema(many=True).dump([genre])),
                get_by_limit=Mock(return_value=GenreSchema(many=True).dump([genre]))
            )
            yield mock

    def test_get_all_genres(self, genre_dao_mock, genre):
        assert self.service.get_all_genres() == GenreSchema(many=True).dump([genre])
        genre_dao_mock().get_all.assert_called_once()

    def test_get_item_by_id(self, genre_dao_mock, genre):
        assert self.service.get_genre_by_id(genre.id) == GenreSchema().dump(genre)
        genre_dao_mock().get_one_by_id.assert_called_once_with(genre.id)

    def test_get_item_by_id_not_found(self, genre_dao_mock):
        genre_dao_mock().get_one_by_id.return_value = None

        with pytest.raises(ItemNotFound):
            self.service.get_genre_by_id(1)

    def test_get_by_limit(self, genre_dao_mock, page, genre):
        assert self.service.get_limit_genres(page) == GenreSchema(many=True).dump([genre])
        genre_dao_mock().get_by_limit.assert_called_once()
