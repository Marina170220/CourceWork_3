from flask import request
from flask_restx import abort, Namespace, Resource

from project.exceptions import ItemNotFound
from project.services import GenresService
from project.setup_db import db
from project.tools.security import auth_required

genres_ns = Namespace("genres")


@genres_ns.route("/")
class GenresView(Resource):
    @genres_ns.doc(description='Get all genres')
    @genres_ns.response(200, "OK")
    @auth_required
    def get(self):
        page = request.args.get('page')
        if page:
            return GenresService(db.session).get_limit_genres(page)

        return GenresService(db.session).get_all_genres()


@genres_ns.route("/<int:gen_id>/")
class GenreView(Resource):
    @genres_ns.doc(description='Get genre by id')
    @genres_ns.response(200, "OK")
    @genres_ns.response(404, "Genre not found")
    @auth_required
    def get(self, gen_id: int):
        try:
            return GenresService(db.session).get_genre_by_id(gen_id)
        except ItemNotFound:
            abort(404)
