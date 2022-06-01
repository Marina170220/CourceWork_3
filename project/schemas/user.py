from marshmallow import fields, Schema

from project.schemas.genre import GenreSchema


class UserSchema(Schema):
    id = fields.Int(required=True, dump_only=True)
    email = fields.Str(required=True)
    password = fields.Str(required=True)
    role = fields.Str()
    name = fields.Str()
    surname = fields.Str()
    favourite_genre = fields.Nested(GenreSchema(only=("name",)))
