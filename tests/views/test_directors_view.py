from unittest.mock import patch, Mock
import pytest


class TestDirectorsView:
    url = "/directors/"

    @pytest.fixture
    def director_data(self, db):
        return {"name": "Тим Бёртон",
                "id": 1}

    @pytest.fixture
    def header(self, db):
        return {
            "Authorization": "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJlbWFpbCI6Im15ZW1haWxAY29tIiwicGFzc3dvcmQiOiIxMjM0NXF3ZXJ0eSIsInJvbGUiOm51bGwsImlkIjoxLCJleHAiOjE2NTg4NDMzMjl9.7tRYmMFgZo8HmpguGc1FCjpFaOXQw5xXIWDpVkjX-Ds"
        }

    @pytest.fixture
    def director_service_mock(self, director_data):
        with patch("project.views.directors.DirectorService") as mock:
            mock.return_value = Mock(
                get_limit_directors=Mock(return_value=[director_data]),
                get_all_directors=Mock(return_value=[director_data])
            )
            yield mock

    def test_get_directors(self, client, header, director_service_mock, director_data):
        response = client.get(self.url, headers=header)
        assert response.status_code == 200
        assert response.json == [director_data]
        director_service_mock().get_all_directors.assert_called_once()

    def test_director_pages(self, client, header, director_service_mock, director_data):
        response = client.get("/directors/?page=1", headers=header)
        assert response.status_code == 200
        assert len(response.json) == 1
        assert response.json == [director_data]
        director_service_mock().get_limit_directors.assert_called_once()


class TestDirectorView:
    url = "/directors/{director_id}"

    @pytest.fixture
    def director_data(self, db):
        return {"name": "Владимир Бортко",
                "id": 1}

    @pytest.fixture
    def header(self, db):
        return {
            "Authorization": "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJlbWFpbCI6Im15ZW1haWxAY29tIiwicGFzc3dvcmQiOiIxMjM0NXF3ZXJ0eSIsInJvbGUiOm51bGwsImlkIjoxLCJleHAiOjE2NTg4NDMzMjl9.7tRYmMFgZo8HmpguGc1FCjpFaOXQw5xXIWDpVkjX-Ds"
        }

    @pytest.fixture
    def director_service_mock(self, director_data):
        with patch("project.views.directors.DirectorService") as mock:
            mock.return_value = Mock(
                get_director_by_id=Mock(return_value=director_data)
            )
            yield mock

    def test_get_director(self, client, header, director_service_mock, director_data):
        response = client.get(self.url.format(director_id=1), headers=header)
        assert response.status_code == 200
        assert response.json == director_data
        director_service_mock().get_director_by_id.assert_called_once()

    def test_director_not_found(self, header, director_service_mock, client):
        response = client.get(self.url, headers=header)
        assert response.status_code == 404
        director_service_mock().assert_not_called()
