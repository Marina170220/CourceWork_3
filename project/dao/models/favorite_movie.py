from project.setup_db import db


class FavoriteMovie(db.Model):
    __tablename__ = "favorite_movies"

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), primary_key=True, nullable=False)
    movie_id = db.Column(db.Integer, db.ForeignKey("movies.id"), primary_key=True, nullable=False)

    def __repr__(self):
        return "<FavoriteMovie>"
