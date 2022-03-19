from unittest.mock import patch, Mock
import pytest


class TestMoviesView:
    url = "/movies/"

    @pytest.fixture
    def movie_data(self, db):
        return {"title": "test1",
                "description": 'test1',
                "trailer": 'test1',
                "year": 2000,
                "rating": 10,
                "genre_id": 1,
                "director_id": 1
                }

    @pytest.fixture
    def header(self, db):
        return {
            "Authorization": "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJlbWFpbCI6Im15ZW1haWxAY29tIiwicGFzc3dvcmQiOiIxMjM0NXF3ZXJ0eSIsInJvbGUiOm51bGwsImlkIjoxLCJleHAiOjE2NTg4NDMzMjl9.7tRYmMFgZo8HmpguGc1FCjpFaOXQw5xXIWDpVkjX-Ds"
        }

    @pytest.fixture
    def movie_service_mock(self, movie_data):
        with patch("project.views.movies.MoviesService") as mock:
            mock.return_value = Mock(
                get_filter_movies=Mock(return_value=[movie_data]),
                get_limit_movies=Mock(return_value=[movie_data]),
                get_all_movies=Mock(return_value=[movie_data]),
                get_movies_by_favorite_genre=Mock(return_value=[movie_data])
            )
            yield mock

    def test_get_movies(self, client, header, movie_service_mock, movie_data):
        response = client.get(self.url, headers=header)
        assert response.status_code == 200
        assert response.json == [movie_data]
        movie_service_mock().get_all_movies.assert_called_once()

    def test_movie_pages(self, client, header, movie_service_mock, movie_data):
        response = client.get("/movies/?page=1", headers=header)
        assert response.status_code == 200
        assert len(response.json) == 1
        assert response.json == [movie_data]
        movie_service_mock().get_limit_movies.assert_called_once()

    def test_movie_status(self, client, header, movie_service_mock, movie_data):
        response = client.get("/movies/?status=new", headers=header)
        assert response.status_code == 200
        assert len(response.json) == 1
        assert response.json == [movie_data]
        movie_service_mock().get_limit_movies.assert_called_once()

    def test_movie_page_and_status(self, client, header, movie_service_mock, movie_data):
        response = client.get("/movies/?status=new&page=1", headers=header)
        assert response.status_code == 200
        assert len(response.json) == 1
        assert response.json == [movie_data]
        movie_service_mock().get_limit_movies.assert_called_once()

    def test_movie_director_id(self, client, header, movie_service_mock, movie_data):
        response = client.get("/movies/?director_id=1", headers=header)
        assert response.status_code == 200
        assert len(response.json) == 1
        assert response.json == [movie_data]
        movie_service_mock().get_filter_movies.assert_called_once()

    def test_movie_genre_id(self, client, header, movie_service_mock, movie_data):
        response = client.get("/movies/?genre_id=1", headers=header)
        assert response.status_code == 200
        assert len(response.json) == 1
        assert response.json == [movie_data]
        movie_service_mock().get_filter_movies.assert_called_once()

    def test_movie_year(self, client, header, movie_service_mock, movie_data):
        response = client.get("/movies/?year=2000", headers=header)
        assert response.status_code == 200
        assert len(response.json) == 1
        assert response.json == [movie_data]
        movie_service_mock().get_filter_movies.assert_called_once()

    def test_movie_fav_genre(self, client, header, movie_service_mock, movie_data):
        response = client.get("/movies/genre", headers=header)
        assert response.status_code == 200
        assert len(response.json) == 1
        assert response.json == [movie_data]
        movie_service_mock().get_movies_by_favorite_genre.assert_called_once()


class TestMovieView:
    url = "/movies/{movie_id}"

    @pytest.fixture
    def movie_data(self, db):
        return {"title": "test1",
                "description": 'test1',
                "trailer": 'test1',
                "year": 2000,
                "rating": 10,
                "genre_id": 1,
                "director_id": 1
                }

    @pytest.fixture
    def header(self, db):
        return {
            "Authorization": "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJlbWFpbCI6Im15ZW1haWxAY29tIiwicGFzc3dvcmQiOiIxMjM0NXF3ZXJ0eSIsInJvbGUiOm51bGwsImlkIjoxLCJleHAiOjE2NTg4NDMzMjl9.7tRYmMFgZo8HmpguGc1FCjpFaOXQw5xXIWDpVkjX-Ds"
        }

    @pytest.fixture
    def movie_service_mock(self, movie_data):
        with patch("project.views.movies.MoviesService") as mock:
            mock.return_value = Mock(
                get_movie_by_id=Mock(return_value=movie_data)
            )
            yield mock

    def test_get_movie(self, client, header, movie_service_mock, movie_data):
        response = client.get(self.url.format(movie_id=1), headers=header)
        assert response.status_code == 200
        assert response.json == movie_data
        movie_service_mock().get_movie_by_id.assert_called_once()

    def test_movie_not_found(self, header, movie_service_mock, client):
        response = client.get(self.url, headers=header)
        assert response.status_code == 404
        movie_service_mock.assert_not_called()
