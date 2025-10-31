"""Schemas for Families d'Impact resources."""

from marshmallow import fields, validate

from ..extensions import ma


class FamilySchema(ma.Schema):
    id = fields.Integer(dump_only=True)
    name = fields.String(required=True, validate=validate.Length(min=2, max=150))
    description = fields.String(allow_none=True)
    address = fields.String()
    city = fields.String()
    postal_code = fields.String()
    country = fields.String()
    meeting_day = fields.String()
    meeting_time = fields.String()
    latitude = fields.Float()
    longitude = fields.Float()
    responsible_id = fields.Integer(allow_none=True)
    created_at = fields.DateTime(dump_only=True)


class FamilyMemberSchema(ma.Schema):
    id = fields.Integer(dump_only=True)
    family_id = fields.Integer(required=True)
    user_id = fields.Integer(required=True)
    joined_at = fields.DateTime(dump_only=True)
