from flask_restx import abort, Namespace, Resource

from project.exceptions import ItemNotFound
from project.services.fav_movies_service import FavoriteMoviesService
from project.setup_db import db
from project.tools.security import auth_required, get_id_from_token

fav_movies_ns = Namespace("favorites/movies")


@fav_movies_ns.route("/")
class FavoriteMoviesView(Resource):
    @fav_movies_ns.doc(description='Get all favorite movies')
    @fav_movies_ns.response(200, "OK")
    @auth_required
    def get(self):
        uid = get_id_from_token()
        try:
            return FavoriteMoviesService(db.session).get_by_user_id(uid)
        except ItemNotFound:
            abort(404)


@fav_movies_ns.route("/<int:mov_id>/")
class FavoriteMovieView(Resource):
    @fav_movies_ns.doc(description='Add movie to favorites')
    @fav_movies_ns.response(200, "OK")
    @fav_movies_ns.response(412, "Movie already exists")
    @auth_required
    def post(self, mov_id: int):
        uid = get_id_from_token()
        return FavoriteMoviesService(db.session).create(uid, mov_id)

    @fav_movies_ns.doc(description='Delete movie from favorites')
    @fav_movies_ns.response(200, "OK")
    @fav_movies_ns.response(412, "Movie already exists")
    @auth_required
    def delete(self, mov_id: int):
        uid = get_id_from_token()
        FavoriteMoviesService(db.session).delete(uid, mov_id)
        return "", 204
