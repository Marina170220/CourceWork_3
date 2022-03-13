from flask import request
from flask_restx import abort, Namespace, Resource

from project.exceptions import ItemNotFound
from project.services.fav_movies_service import FavoriteMoviesService
from project.setup_db import db
from project.tools.security import auth_required

fav_movies_ns = Namespace("favorites/movies")
