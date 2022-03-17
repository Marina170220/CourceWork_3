import pytest

from project.dao.models import Genre, Director, User
from project.dao.models.movie import Movie


class TestMoviesView:
    url = "/movies/"

    @pytest.fixture
    def movie(self, db):
        m = Movie(title="test1",
                  description='test1',
                  trailer='test1',
                  year=2000,
                  rating='10',
                  genre_id='1',
                  director_id='1')
        db.session.add(m)
        db.session.commit()
        return m

    @pytest.fixture
    def genre(self, db):
        g = Genre(name="Боевик")
        db.session.add(g)
        db.session.commit()
        return g

    @pytest.fixture
    def director(self, db):
        d = Director(name="Тим Бёртон")
        db.session.add(d)
        db.session.commit()
        return d

    def test_get_movies(self, client, movie, genre, director):
        response = client.get(self.url)
        assert response.status_code == 200
        assert response.json == [
            {"id": movie.id,
             "title": movie.title,
             "description": movie.description,
             "trailer": movie.trailer,
             "year": movie.year,
             "rating": movie.rating,
             "genre": genre.name,
             "director": director.name
             },
        ]

    def test_movies_pages(self, client, movie, genre, director):
        response = client.get("movies/?page=1")
        assert response.status_code == 200
        assert len(response.json) == 1

    def test_movies_status(self, client, movie, genre, director):
        response = client.get("movies/?status=new")
        assert response.status_code == 200
        assert len(response.json) == 1

    def test_movies_page_and_status(self, client, movie, genre, director):
        response = client.get("movies/?page=1&status=new")
        assert response.status_code == 200
        assert len(response.json) == 1

    def test_movies_by_director(self, client, movie, genre, director):
        response = client.get("movies/?director_id=1")
        assert response.status_code == 200
        assert len(response.json) == 1

    def test_movies_by_genre(self, client, movie, genre, director):
        response = client.get("movies/?genre_id=1")
        assert response.status_code == 200
        assert len(response.json) == 1

    def test_movies_by_year(self, client, movie, genre, director):
        response = client.get("movies/?year=2000")
        assert response.status_code == 200
        assert len(response.json) == 1


class TestMovieView:
    url = "/movies/{movie_id}"

    @pytest.fixture
    def movie(self, db):
        m = Movie(title="test1",
                  description='test1',
                  trailer='test1',
                  year=2000,
                  rating=3.8,
                  genre_id=1,
                  director_id=1)
        db.session.add(m)
        db.session.commit()
        return m

    @pytest.fixture
    def genre(self, db):
        g = Genre(name="Боевик")
        db.session.add(g)
        db.session.commit()
        return g

    @pytest.fixture
    def director(self, db):
        d = Director(name="Тим Бёртон")
        db.session.add(d)
        db.session.commit()
        return d

    def test_get_movie(self, client, movie, genre, director):
        response = client.get(self.url.format(movie_id=movie.id))
        assert response.status_code == 200
        assert response.json == {"id": movie.id,
                                 "title": movie.title,
                                 "description": movie.description,
                                 "trailer": movie.trailer,
                                 "year": movie.year,
                                 "rating": movie.rating,
                                 "genre": genre.name,
                                 "director": director.name
                                 }

    def test_movie_not_found(self, client):
        response = client.get(self.url.format(movie_id=1))
        assert response.status_code == 404


class TestGenreMovieView:
    url = "/movies/genre"

    @pytest.fixture
    def movie(self, db):
        m = Movie(title="test1",
                  description='test1',
                  trailer='test1',
                  year=2000,
                  rating=3.8,
                  genre_id=1,
                  director_id=1)
        db.session.add(m)
        db.session.commit()
        return m

    @pytest.fixture
    def genre(self, db):
        g = Genre(name="Боевик")
        db.session.add(g)
        db.session.commit()
        return g

    @pytest.fixture
    def director(self, db):
        d = Director(name="Тим Бёртон")
        db.session.add(d)
        db.session.commit()
        return d

    @pytest.fixture
    def user_1(self, db):
        u = User(email="test@test.ry",
                 password="mypass",
                 role="test",
                 favorite_genre="Боевик")
        db.session.add(u)
        db.session.commit()
        return u

    @pytest.fixture
    def user_2(self, db):
        u = User(email="test@test.ry",
                 password="mypass",
                 role="test"
                 )
        db.session.add(u)
        db.session.commit()
        return u

    @pytest.fixture
    def login_headers(self, db):
        return {
            "Authorization": "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJlbWFpbCI6InRlc3RfMUB0ZXN0LmNvbSIsInBhc3N3b3JkIjoibXlwYXNzIiwiZmF2b3JpdGVfZ2VucmUiOiJcdTA0MTRcdTA0NDBcdTA0MzBcdTA0M2NcdTA0MzAiLCJyb2xlIjoiYWRtaW4iLCJpZCI6MywiZXhwIjoxNjU4NzUyNzI3fQ.sCYtnTTMIXhnEUaZeiRHv4R9T4fzkmFvLvoH6-_ialQ"}

    def test_genre_movies(self, client, movie, genre, director, user_1, login_headers):
        response = client.get(self.url, headers=login_headers)
        assert response.status_code == 200
