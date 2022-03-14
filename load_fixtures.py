from sqlalchemy.exc import IntegrityError

from project.config import DevelopmentConfig
from project.dao.models import Genre, Director, Movie
from project.server import create_app
from project.setup_db import db
from project.utils import read_json

app = create_app(DevelopmentConfig)

data = read_json("fixtures.json")

with app.app_context():
    db.drop_all()
    db.create_all()

    for movie in data["movies"]:
        new_movie = Movie(
            id=movie["pk"],
            title=movie["title"],
            description=movie["description"],
            trailer=movie["trailer"],
            year=movie["year"],
            rating=movie["rating"],
            genre_id=movie["genre_id"],
            director_id=movie["director_id"]
        )
        with db.session.begin():
            db.session.add(new_movie)

    for director in data["directors"]:
        new_director = Director(
            id=director["pk"],
            name=director["name"],
        )
        with db.session.begin():
            db.session.add(new_director)

    for genre in data["genres"]:
        new_genre = Genre(
            id=genre["pk"],
            name=genre["name"],
        )
        with db.session.begin():
            db.session.add(new_genre)


    try:
        db.session.commit()
    except IntegrityError:
        print("Fixtures already loaded")
