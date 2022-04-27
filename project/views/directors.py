from flask import request
from flask_restx import abort, Namespace, Resource

from project.exceptions import ItemNotFound
from project.services.directors_service import DirectorService
from project.setup_db import db
from project.tools.security import auth_required

directors_ns = Namespace("directors")


@directors_ns.route("/")
class DirectorsView(Resource):
    @directors_ns.response(200, "OK")
    @auth_required
    def get(self):
        """Get all directors"""
        page = request.args.get('page')
        if page:
            return DirectorService(db.session).get_limit_directors(page)

        return DirectorService(db.session).get_all_directors()


@directors_ns.route('/<int:dir_id>/')
class DirectorView(Resource):
    @directors_ns.response(200, "OK")
    @directors_ns.response(404, "Director not found")
    @auth_required
    def get(self, dir_id: int):
        """Get director by id"""
        try:
            return DirectorService(db.session).get_director_by_id(dir_id)
        except ItemNotFound:
            abort(404)
