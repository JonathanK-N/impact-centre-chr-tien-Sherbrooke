"""Schemas for media resources."""

from marshmallow import fields, validate

from ..extensions import ma


class MediaSchema(ma.Schema):
    id = fields.Integer(dump_only=True)
    title = fields.String(required=True, validate=validate.Length(min=3, max=200))
    description = fields.String()
    media_type = fields.String(required=True)
    url = fields.String(required=True)
    published_at = fields.DateTime(dump_only=True)
    tags = fields.String()
    department_id = fields.Integer(allow_none=True)
    family_id = fields.Integer(allow_none=True)
