from unittest.mock import patch, Mock
import pytest


class TestGenresView:
    url = "/genres/"

    @pytest.fixture
    def genre_data(self, db):
        return {"name": "Боевик",
                "id": 1}

    @pytest.fixture
    def header(self, db):
        return {
            "Authorization": "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJlbWFpbCI6Im15ZW1haWxAY29tIiwicGFzc3dvcmQiOiIxMjM0NXF3ZXJ0eSIsInJvbGUiOm51bGwsImlkIjoxLCJleHAiOjE2NTg4NDMzMjl9.7tRYmMFgZo8HmpguGc1FCjpFaOXQw5xXIWDpVkjX-Ds"
        }

    @pytest.fixture
    def genre_service_mock(self, genre_data):
        with patch("project.views.genres.GenresService") as mock:
            mock.return_value = Mock(
                get_limit_genres=Mock(return_value=[genre_data]),
                get_all_genres=Mock(return_value=[genre_data])
            )
            yield mock

    def test_get_genres(self, client, header, genre_service_mock, genre_data):
        response = client.get(self.url, headers=header)
        assert response.status_code == 200
        assert response.json == [genre_data]
        genre_service_mock().get_all_genres.assert_called_once()

    def test_genre_pages(self, client, header, genre_service_mock, genre_data):
        response = client.get("/genres/?page=1", headers=header)
        assert response.status_code == 200
        assert len(response.json) == 1
        assert response.json == [genre_data]
        genre_service_mock().get_limit_genres.assert_called_once()


class TestGenreView:
    url = "/genres/{genre_id}"

    @pytest.fixture
    def genre_data(self, db):
        return {"name": "Боевик",
                "id": 1}

    @pytest.fixture
    def header(self, db):
        return {
            "Authorization": "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJlbWFpbCI6Im15ZW1haWxAY29tIiwicGFzc3dvcmQiOiIxMjM0NXF3ZXJ0eSIsInJvbGUiOm51bGwsImlkIjoxLCJleHAiOjE2NTg4NDMzMjl9.7tRYmMFgZo8HmpguGc1FCjpFaOXQw5xXIWDpVkjX-Ds"
        }

    @pytest.fixture
    def genre_service_mock(self, genre_data):
        with patch("project.views.genres.GenresService") as mock:
            mock.return_value = Mock(
                get_genre_by_id=Mock(return_value=genre_data)
            )
            yield mock

    def test_get_genre(self, client, header, genre_service_mock, genre_data):
        response = client.get(self.url.format(genre_id=1), headers=header)
        assert response.status_code == 200
        assert response.json == genre_data
        genre_service_mock().get_genre_by_id.assert_called_once()

    def test_genre_not_found(self, header, client):
        response = client.get(self.url, headers=header)
        assert response.status_code == 404

