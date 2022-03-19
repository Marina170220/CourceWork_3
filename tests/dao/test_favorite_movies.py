import pytest

from project.dao.favorite_movie import FavoriteMovieDAO
from project.dao.models import FavoriteMovie, Movie


class TestFavMovieDAO:
    @pytest.fixture(autouse=True)
    def dao(self, db):
        self.dao = FavoriteMovieDAO(db.session)

    @pytest.fixture
    def fav_movie_1(self, db):
        fm = FavoriteMovie(user_id=2,
                           movie_id=1)
        db.session.add(fm)
        db.session.commit()
        return fm

    @pytest.fixture
    def fav_movie_2(self, db):
        fm = FavoriteMovie(user_id=1,
                           movie_id=5)
        db.session.add(fm)
        db.session.commit()
        return fm

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

    def test_get_one(self, fav_movie_1, movie_1):
        assert self.dao.get_by_user_id(2) == [movie_1]

    def test_create(self, fav_movie_2, movie_1):
        self.dao.create(1, 1)
        assert self.dao.get_by_user_id(fav_movie_2.user_id) == [movie_1]

    def test_delete(self, fav_movie_1, movie_1):
        self.dao.delete(fav_movie_1.user_id, fav_movie_1.movie_id)
        assert self.dao.get_by_user_id(2) == []
