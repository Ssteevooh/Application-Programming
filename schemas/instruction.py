from marshmallow import Schema, fields, post_dump, validate, validates, ValidationError
from schemas.user import UserSchema


def validate_duration(n):
    if n < 1:
        raise ValidationError('Number of duration must be greater than 0.')
    if n > 50:
        raise ValidationError('Number of duration must not be greater than 50.')

class InstructionSchemas(Schema):
    class Meta:
        ordered = True

    id = fields.Integer(dump_only=True)
    name = fields.String(required=True, validate=[validate.Length(max=100)])
    description = fields.String(validate=[validate.Length(max=200)])
    steps = fields.List(fields.String())
    tools = fields.List(fields.String())
    cost = fields.Integer()
    duration = fields.Integer(validate=validate_duration)
    is_publish = fields.Boolean(dump_only=True)
    author = fields.Nested(UserSchema, attribute='user', dump_only=True, exclude=('email',))
    created_at = fields.DateTime(dump_only=True)
    updated_at =fields.DateTime(dump_only=True)

    @post_dump(pass_many=True)
    def wrap(self, data, many, **kwargs):
        if many:
            return {'data': data}
        return data

    @validates('cost')
    def validate_cost(self, value):
        if value < 1:
            raise ValidationError('Cost must be greater than 0.')
        if value > 10000:
            raise ValidationError('Cost must not be greater than 10 000.')
