import pytest

from project.dao import DirectorDAO
from project.dao.models import Director


class TestDirectorDAO:
    @pytest.fixture(autouse=True)
    def dao(self, db):
        self.dao = DirectorDAO(db.session)

    @pytest.fixture
    def dir_1(self, db):
        d = Director(name="Карен Шахназаров")
        db.session.add(d)
        db.session.commit()
        return d

    @pytest.fixture
    def dir_2(self, db):
        d = Director(name="Александр Митта")
        db.session.add(d)
        db.session.commit()
        return d

    def test_get_director_by_id(self, dir_1):
        assert self.dao.get_one_by_id(dir_1.id) == dir_1

    def test_get_director_by_id_not_found(self):
        assert self.dao.get_one_by_id(1) is None

    def test_get_all_directors(self, dir_1, dir_2):
        assert self.dao.get_all() == [dir_1, dir_2]

    def test_get_by_limit(self):
        limit = 2
        offset = 10
        assert len(self.dao.get_by_limit(limit, offset)) == 0
