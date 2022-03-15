from marshmallow import fields, Schema


class MovieSchema(Schema):
    id = fields.Int(required=True, dump_only=True)
    title = fields.Str(required=True)
    description = fields.Str(required=True)
    trailer = fields.Str(required=True)
    year = fields.Int(required=True)
    rating = fields.Float(required=True)
    genre = fields.Str(required=True)
    director = fields.Str(required=True)
