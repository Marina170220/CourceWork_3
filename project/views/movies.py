from flask import request
from flask_restx import abort, Namespace, Resource

from project.exceptions import ItemNotFound
from project.services.movies_service import MoviesService
from project.setup_db import db
from project.tools.security import auth_required

movies_ns = Namespace("movies")


@movies_ns.route('/')
class MoviesView(Resource):
    @auth_required
    @movies_ns.response(200, "OK")
    def get(self):
        """Get all movies"""
        page = request.args.get('page')
        status = request.args.get('status')
        limits = {'page': page,
                  'status': status}
        director = request.args.get("director_id")
        genre = request.args.get("genre_id")
        year = request.args.get("year")
        filters = {
            "director_id": director,
            "genre_id": genre,
            "year": year,
        }
        if limits:
            return MoviesService(db.session).get_limit_movies(limits)
        if filters:
            return MoviesService(db.session).get_filter_movies(filters)
        return MoviesService(db.session).get_all_movies()


@movies_ns.route('/<int:mov_id>')
class MovieView(Resource):
    @auth_required
    @movies_ns.response(200, "OK")
    @movies_ns.response(404, "Movie not found")
    def get(self, mov_id: int):
        """Get movie by id"""
        try:
            return MoviesService(db.session).get_movie_by_id(mov_id)
        except ItemNotFound:
            abort(404)

