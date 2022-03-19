from unittest.mock import patch, Mock
import pytest

from project.dao.models import User
from project.exceptions import ItemNotFound
from project.services import UsersService
from project.tools.security import generate_password_hash


class TestUserView:
    url = "/user/"

    @pytest.fixture(autouse=True)
    def service(self, db):
        self.service = UsersService(db.session)

    @pytest.fixture
    def user(self, db):
        return User(id=1,
                    email="test1@test",
                    password="testpass",
                    role="usertest",
                    name="testname_2",
                    surname="testsurname_2",
                    favorite_genre_id=1
                    )

    @pytest.fixture
    def user_data(self, db):
        return {"id": 1,
                "email": "test1@test",
                "password": "testpass",
                "role": "usertest",
                "name": "test",
                "surname": "testsurname_2",
                "favorite_genre_id": 1,
                }

    @pytest.fixture
    def old_user_data(self, db):
        password = generate_password_hash("testpass")
        return {"id": 3,
                "email": "test1@test",
                "password": password,
                "role": "usertest",
                "name": "test",
                "favorite_genre_id": 1,
                }

    @pytest.fixture
    def new_user_data(self, db):
        password = generate_password_hash("newpass")
        return {"id": 3,
                "email": "test1@test",
                "password": password,
                "role": "usertest",
                "name": "test",
                "favorite_genre_id": 1,
                }

    @pytest.fixture
    def passwords(self, db):
        return {"password_1": "testpass",
                "password_2": 'newpass'
                }

    @pytest.fixture
    def header(self, db):
        return {
            "Authorization": "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJlbWFpbCI6InRlc3QxQHRlc3QiLCJwYXNzd29yZCI6InRlc3RwYXNzIiwicm9sZSI6InVzZXJ0ZXN0IiwiaWQiOjMsImV4cCI6MTY1ODg1ODk4N30.7fzEafch1LOf4PyKDE6POPFY22JMwVb3hqwCBmTh6rI"
        }

    @pytest.fixture
    def user_service_mock(self, user_data, new_user_data, user):
        with patch("project.views.users.UsersService") as mock:
            mock.return_value = Mock(
                get_user_by_id=Mock(return_value=user_data),
                update=Mock(return_value=user_data),
                update_user_pass=Mock(return_value=new_user_data),
            )
            yield mock

    def test_get_user(self, client, header, user_service_mock, user_data):
        response = client.get(self.url, headers=header)
        assert response.status_code == 200
        assert response.json == user_data
        user_service_mock().get_user_by_id.assert_called_once()

    def test_get_item_by_id_not_found(self, user_service_mock):
        user_service_mock().get_user_by_id.return_value = None

        with pytest.raises(ItemNotFound):
            self.service.get_user_by_id(5)

    def test_update_user(self, client, header, user_service_mock, user_data):
        response = client.get(self.url, headers=header)
        assert response.status_code == 200
        assert response.json == user_data
