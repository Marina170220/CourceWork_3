from flask import request
from flask_restx import abort, Namespace, Resource

from project.exceptions import ItemNotFound
from project.services.fav_movies_service import FavoriteMoviesService
from project.setup_db import db
from project.tools.security import auth_required, auth_check

fav_movies_ns = Namespace("favorites/movies")


@fav_movies_ns.route("/")
class FavoriteMoviesView(Resource):
    @auth_required
    @fav_movies_ns.response(200, "OK")
    def get(self):
        """Get all favorite movies"""
        user_id = auth_check().get('id')
        try:
            return FavoriteMoviesService(db.session).get_by_user_id(user_id)
        except ItemNotFound:
            abort(404)


@fav_movies_ns.route("/<int:mov_id>")
class FavoriteMovieView(Resource):
    @auth_required
    @fav_movies_ns.response(200, "OK")
    @fav_movies_ns.response(404, "Movie not found")
    def post(self, mov_id: int):
        """Add movie to favorites"""
        user_id = auth_check().get('id')
        return FavoriteMoviesService(db.session).create(user_id, mov_id)

    def delete(self, mov_id: int):
        """Delete movie from favorites"""
        user_id = auth_check().get('id')
        FavoriteMoviesService(db.session).delete(user_id, mov_id)
        return "", 204
