from marshmallow import fields, Schema


class DirectorSchema(Schema):
    id = fields.Int(required=True, dump_only=True)
    name = fields.Str(required=True)
