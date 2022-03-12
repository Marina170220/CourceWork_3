from project.dao.models.base import BaseMixin
from project.setup_db import db


class FavoriteMovie(BaseMixin, db.Model):
    __tablename__ = "favorite_movies"

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    user = db.relationship("User")
    movie_id = db.Column(db.Integer, db.ForeignKey("movies.id"), nullable=False)
    director = db.relationship("Movie")

    def __repr__(self):
        return "<FavoriteMovie>"
