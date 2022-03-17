import pytest

from project.dao.models.user import User
from project.dao.user import UserDAO


class TestUserDAO:
    @pytest.fixture(autouse=True)
    def dao(self, db):
        self.dao = UserDAO(db.session)

    @pytest.fixture
    def user_1(self, db):
        u = User(email="test_1@test.su",
                    password="testpass_1",
                    role="testrole_1",
                    name="testname_1",
                    surname="testsurname_1",
                    favorite_genre="testgen_1"
                 )
        db.session.add(u)
        db.session.commit()
        return u

    @pytest.fixture
    def user_2(self, db):
        u = User(email="test_2@test.su",
                    password="testpass_2",
                    role="testrole_2",
                    name="testname_2",
                    surname="testsurname_2",
                    favorite_genre="testgen_2"
                 )
        db.session.add(u)
        db.session.commit()
        return u

    def test_get_user_by_id(self, user_1):
        assert self.dao.get_one_by_id(user_1.id) == user_1

    def test_get_user_by_id_not_found(self):
        assert self.dao.get_one_by_id(1) is None

    def test_get_all_users(self, user_1, user_2):
        assert self.dao.get_all() == [user_1, user_2]

    def test_get_by_email(self, user_2):
        email = "test_2@test.su"
        assert self.dao.get_by_email(email) == user_2

    def test_user_create(self):
        data = {"id": 1,
                "email": "test@test.com",
                "password": "testpass_2",
                "role": "testrole_2"}
        user = self.dao.create(data)
        assert self.dao.get_one_by_id(1) == user

    def test_user_update(self, user_1):
        user_1.email = 'new_email@test.ry'
        self.dao.update(user_1)
        assert user_1.email == 'new_email@test.ry'
        assert self.dao.get_one_by_id(1) == user_1

    def test_get_by_limit(self):
        limit = 2
        offset = 10
        assert len(self.dao.get_by_limit(limit, offset)) == 0
