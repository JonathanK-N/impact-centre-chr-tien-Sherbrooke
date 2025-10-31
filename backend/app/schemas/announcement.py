"""Schemas for announcements."""

from marshmallow import fields, validate

from ..extensions import ma


class AnnouncementSchema(ma.Schema):
    id = fields.Integer(dump_only=True)
    title = fields.String(required=True, validate=validate.Length(min=3, max=200))
    body = fields.String(required=True)
    scope = fields.String(required=True)
    author_id = fields.Integer(dump_only=True)
    department_id = fields.Integer(allow_none=True)
    family_id = fields.Integer(allow_none=True)
    published_at = fields.DateTime(dump_only=True)
    expires_at = fields.DateTime(allow_none=True)
