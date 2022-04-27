from project.config import ProductionConfig
from project.dao.models import Genre, Director, Movie, User, FavoriteMovie
from project.server import create_app, db

app = create_app(ProductionConfig)

@app.shell_context_processor
def shell():
    return {
        "db": db,
        "Genre": Genre,
        "Director": Director,
        "Movie": Movie,
        "User": User,
        "FavoriteMovie": FavoriteMovie,
    }
