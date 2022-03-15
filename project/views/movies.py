from flask import request
from flask_restx import abort, Namespace, Resource

from project.exceptions import ItemNotFound
from project.services.movies_service import MoviesService
from project.setup_db import db
from project.tools.security import auth_required, auth_check

movies_ns = Namespace("movies")


@movies_ns.route('/')
class MoviesView(Resource):
    @auth_required
    @movies_ns.response(200, "OK")
    def get(self):
        """Get all movies"""
        limits = {}
        filters = {}
        if request.args.get('page'):
            limits['page'] = request.args.get('page')
        if request.args.get('status'):
            limits['status'] = request.args.get('status')

        if request.args.get("director_id"):
            filters['director_id'] = request.args.get('director_id')
        if request.args.get("genre_id"):
            filters['genre_id'] = request.args.get('genre_id')
        if request.args.get("year"):
            filters['year'] = request.args.get('year')

        if filters:
            return MoviesService(db.session).get_filter_movies(filters)
        if limits:
            return MoviesService(db.session).get_limit_movies(limits)
        else:
            return MoviesService(db.session).get_all_movies()


@movies_ns.route('/genre')
class MoviesByGenreView(Resource):
    @auth_required
    @movies_ns.response(200, "OK")
    def get(self):
        """Get movies by user's favorite genre"""
        user_id = auth_check().get('id')
        try:
            return MoviesService(db.session).get_movies_by_favorite_genre(user_id)
        except ItemNotFound:
            abort(404)


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
