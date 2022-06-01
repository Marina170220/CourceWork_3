from project.dao.models.base import BaseMixin
from project.setup_db import db


class User(BaseMixin, db.Model):
    __tablename__ = "users"

    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(500), nullable=False)
    role = db.Column(db.String(50))
    name = db.Column(db.String(100))
    surname = db.Column(db.String(100))
    favourite_genre_id = db.Column(db.Integer, db.ForeignKey("genres.id"))
    favourite_genre = db.relationship("Genre")

    def __repr__(self):
        return f"{self.name.title()}"
