from marshmallow import fields, Schema


class FavoriteMovieSchema(Schema):
    user_id = fields.Int(required=True, dump_only=True)
    movie_id = fields.Str(required=True)
