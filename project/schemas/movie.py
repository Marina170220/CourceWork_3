from marshmallow import fields, Schema

from project.schemas.director import DirectorSchema
from project.schemas.genre import GenreSchema


class MovieSchema(Schema):
    id = fields.Int(required=True, dump_only=True)
    title = fields.Str(required=True)
    description = fields.Str(required=True)
    trailer = fields.Str(required=True)
    year = fields.Int(required=True)
    rating = fields.Float(required=True)
    # genre_id = fields.Str(required=True)
    genre = fields.Nested(GenreSchema)
    # director_id = fields.Str(required=True)
    director = fields.Nested(DirectorSchema)
