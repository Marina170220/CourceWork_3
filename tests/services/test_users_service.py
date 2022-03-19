from unittest.mock import Mock, patch
import pytest

from project.dao.models import User
from project.services import UsersService
from project.schemas.user import UserSchema
from project.exceptions import ItemNotFound
from project.tools.security import generate_password_hash


class TestUsersService:
    @pytest.fixture(autouse=True)
    def service(self, db):
        self.service = UsersService(db.session)

    @pytest.fixture
    def user_1(self, db):
        password = generate_password_hash("testpass_1")
        return User(id=1,
                    email="test_1@test.su",
                    password=password,
                    role="testrole_1",
                    name="testname_1",
                    surname="testsurname_1",
                    favorite_genre="testgen_1"
                    )

    @pytest.fixture
    def user_2(self, db):
        return User(id=2,
                    email="test_2@test.su",
                    password="testpass_2",
                    role="testrole_2",
                    name="testname_2",
                    surname="testsurname_2",
                    favorite_genre="testgen_2"
                    )

    @pytest.fixture
    def limits(self, db):
        limits = {"page": 1}
        return limits

    @pytest.fixture
    def user_data(self, db):
        data = {"id": 1,
                "name": "new_name"}
        return data

    @pytest.fixture
    def new_user_data(self, db):
        return {"id": 3,
                "password": "password_3",
                "role": "user"}

    @pytest.fixture
    def no_password_user_data(self, db):
        return {"id": 3,
                "role": "user"}

    @pytest.fixture
    def updated_user_data(self, db):
        return {"name": "new_name",
                "surname": "new_surname",
                "favorite_genre": "new_genre"}

    @pytest.fixture
    def no_id_updated_user_data(self, db):
        return {"name": "new_name",
                "surname": "new_surname",
                "favorite_genre": "new_genre"}

    @pytest.fixture
    def user_password_data_1(self, db):
        return {"password_1": "testpass_1",
                "password_2": "new_password"}

    @pytest.fixture
    def user_password_data_2(self, db):
        return {"password_1": "old_password",
                "password_2": "new_password"}

    @pytest.fixture
    def user_dao_mock(self, user_1, user_2):
        with patch("project.services.users_service.UserDAO") as mock:
            mock.return_value = Mock(
                get_one_by_id=Mock(return_value=user_1),
                get_all=Mock(return_value=UserSchema(many=True).dump([user_1, user_2])),
                get_by_email=Mock(return_value=UserSchema().dump(user_1)),
                get_by_limit=Mock(return_value=UserSchema(many=True).dump([user_1, user_2])),
                create=Mock(return_value=UserSchema().dump(user_1)),
                update=Mock(return_value=user_1),
            )
            yield mock

    def test_get_all_users(self, user_dao_mock, user_1, user_2):
        assert self.service.get_all_users() == UserSchema(many=True).dump([user_1, user_2])
        user_dao_mock().get_all.assert_called_once()

    def test_get_user_by_id(self, user_dao_mock, user_1):
        assert self.service.get_user_by_id(user_1.id) == UserSchema().dump(user_1)
        user_dao_mock().get_one_by_id.assert_called_once_with(user_1.id)

    def test_get_item_by_id_not_found(self, user_dao_mock):
        user_dao_mock().get_one_by_id.return_value = None

        with pytest.raises(ItemNotFound):
            self.service.get_user_by_id(1)

    def test_get_user_by_email(self, user_dao_mock, user_1):
        assert self.service.get_user_by_email(user_1.email) == UserSchema().dump(user_1)
        user_dao_mock().get_by_email.assert_called_once_with(user_1.email)

    def test_get_limit_users(self, user_dao_mock, limits, user_1, user_2):
        assert self.service.get_limit_users(limits.get('page')) == UserSchema(many=True).dump([user_1, user_2])
        user_dao_mock().get_by_limit.assert_called_once()

    def test_create(self, user_dao_mock, new_user_data, user_1):
        assert self.service.create(new_user_data) == UserSchema().dump(user_1)
        user_dao_mock().create.assert_called_once()

    def test_create_is_fail(self, user_dao_mock, no_password_user_data):
        assert self.service.create(no_password_user_data) is None
        user_dao_mock().create.assert_not_called()

    def test_update(self, user_dao_mock, updated_user_data, user_1):
        assert self.service.update(updated_user_data, user_1.id) == UserSchema().dump(user_1)
        user_dao_mock().update.assert_called()

    def test_update_user_password(self, user_dao_mock, user_password_data_1, user_1):
        assert self.service.update_user_pass(user_password_data_1, user_1.id) == UserSchema().dump(user_1)
        user_dao_mock().update.assert_called_once()

    def test_update_user_password_fail(self, user_dao_mock, user_password_data_2, user_1):
        assert self.service.update_user_pass(user_password_data_2, user_1.id) is None
        user_dao_mock().update.assert_not_called()
