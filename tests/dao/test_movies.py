import pytest

from project.dao.models import Director, Genre, User
from project.dao.models.movie import Movie
from project.dao.movie import MovieDAO


class TestMovieDAO:
    @pytest.fixture(autouse=True)
    def dao(self, db):
        self.dao = MovieDAO(db.session)

    @pytest.fixture
    def movie_1(self, db):
        m = Movie(title="test_1",
                  description='Desc_test_1',
                  trailer='Trailer_test_1',
                  year=2020,
                  rating=10,
                  genre_id=1,
                  director_id=1)
        db.session.add(m)
        db.session.commit()
        return m

    @pytest.fixture
    def movie_2(self, db):
        m = Movie(title="test_2",
                  description='Desc_test_2',
                  trailer='Trailer_test_1',
                  year=1954,
                  rating=8.8,
                  genre_id=3,
                  director_id=5)
        db.session.add(m)
        db.session.commit()
        return m

    @pytest.fixture
    def dir_1(self, db):
        d = Director(name="Dirtest_1")
        db.session.add(d)
        db.session.commit()
        return d

    @pytest.fixture
    def gen_1(self, db):
        g = Genre(name="Драма")
        db.session.add(g)
        db.session.commit()
        return g

    @pytest.fixture
    def user_1(self, db):
        u = User(email="testemail@test",
                 password="testpass",
                 role="user_test",
                 favorite_genre="Драма")
        db.session.add(u)
        db.session.commit()
        return u

    @pytest.fixture
    def limits_all(self, db):
        limits = [2, 12, "new"]
        return limits

    @pytest.fixture
    def limits_status(self, db):
        limits = [0, 12, "new"]
        return limits

    @pytest.fixture
    def limits_page(self, db):
        limits = [1, 12, "no_status"]
        return limits

    @pytest.fixture
    def no_limits(self, db):
        limits = [0, 12, "no_status"]
        return limits

    def test_get_movie_by_id(self, movie_1, dir_1, gen_1):
        movie = self.dao.get_one_by_id(movie_1.id)
        assert movie.id == 1
        assert movie == movie_1
        assert movie.id is not None

    def test_get_movie_by_id_not_found(self):
        assert self.dao.get_one_by_id(1) is None

    def test_get_all_movies(self, movie_1, dir_1, gen_1):
        assert self.dao.get_all() == [movie_1]

    def test_get_by_limit(self, limits_all, limits_status, limits_page, no_limits):
        assert len(self.dao.get_by_limit(limits_all[0], limits_all[1], limits_all[2])) == 0
        assert len(self.dao.get_by_limit(limits_status[0], limits_status[1], limits_status[2])) == 0
        assert len(self.dao.get_by_limit(limits_page[0], limits_page[1], limits_page[2])) == 0
        assert self.dao.get_by_limit(no_limits[0], no_limits[1], no_limits[2]) == []

    def test_get_by_director(self, movie_1, dir_1, gen_1):
        assert self.dao.get_by_director(dir_1.id) == [movie_1]

    def test_get_by_genre(self, movie_1, dir_1, gen_1):
        assert self.dao.get_by_genre(gen_1.id) == [movie_1]

    def test_get_by_year(self, movie_1, dir_1, gen_1):
        year = 2020
        assert self.dao.get_by_year(year) == [movie_1]

    def test_get_by_favorite_genre(self, movie_1, user_1, gen_1):
        user_id = 1
        assert self.dao.get_by_favorite_genre(user_id) == [movie_1]
