from unittest.mock import Mock, patch
import pytest

from project.dao.models import Director
from project.services import DirectorService
from project.schemas.director import DirectorSchema
from project.exceptions import ItemNotFound


class TestDirectorsService:
    @pytest.fixture(autouse=True)
    def service(self, db):
        self.service = DirectorService(db.session)

    @pytest.fixture
    def director(self, db):
        return Director(id=1, name="dir_1")

    @pytest.fixture
    def page(self, db):
        return 1

    @pytest.fixture
    def director_dao_mock(self, director):
        with patch("project.services.directors_service.DirectorDAO") as mock:
            mock.return_value = Mock(
                get_one_by_id=Mock(return_value=DirectorSchema().dump(director)),
                get_all=Mock(return_value=DirectorSchema(many=True).dump([director])),
                get_by_limit=Mock(return_value=DirectorSchema(many=True).dump([director]))
            )
            yield mock

    def test_get_all_directors(self, director_dao_mock, director):
        assert self.service.get_all_directors() == DirectorSchema(many=True).dump([director])
        director_dao_mock().get_all.assert_called_once()

    def test_get_item_by_id(self, director_dao_mock, director):
        assert self.service.get_director_by_id(director.id) == DirectorSchema().dump(director)
        director_dao_mock().get_one_by_id.assert_called_once_with(director.id)

    def test_get_item_by_id_not_found(self, director_dao_mock):
        director_dao_mock().get_one_by_id.return_value = None

        with pytest.raises(ItemNotFound):
            self.service.get_director_by_id(1)

    def test_get_by_limit(self, director_dao_mock, page, director):
        assert self.service.get_limit_directors(page) == DirectorSchema(many=True).dump([director])
        director_dao_mock().get_by_limit.assert_called_once()
