from flask_restx import abort, Namespace, Resource

from project.exceptions import ItemNotFound
from project.services.fav_movies_service import FavoriteMoviesService
from project.setup_db import db
from project.tools.security import auth_required, get_id_from_token

fav_movies_ns = Namespace("favorites/movies")


@fav_movies_ns.route("/")
class FavoriteMoviesView(Resource):
    @auth_required
    @fav_movies_ns.response(200, "OK")
    def get(self):
        """Get all favorite movies"""
        uid = get_id_from_token()
        try:
            return FavoriteMoviesService(db.session).get_by_user_id(uid)
        except ItemNotFound:
            abort(404)


@fav_movies_ns.route("/<int:mov_id>")
class FavoriteMovieView(Resource):
    @auth_required
    @fav_movies_ns.response(200, "OK")
    @fav_movies_ns.response(412, "Movie already exists")
    def post(self, mov_id: int):
        """Add movie to favorites"""
        uid = get_id_from_token()
        return FavoriteMoviesService(db.session).create(uid, mov_id)

    def delete(self, mov_id: int):
        """Delete movie from favorites"""
        uid = get_id_from_token()
        FavoriteMoviesService(db.session).delete(uid, mov_id)
        return "", 204
