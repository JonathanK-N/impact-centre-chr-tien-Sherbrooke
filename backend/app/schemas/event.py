"""Schemas for events."""

from marshmallow import fields, validate

from ..extensions import ma


class EventSchema(ma.Schema):
    id = fields.Integer(dump_only=True)
    title = fields.String(required=True, validate=validate.Length(min=3, max=200))
    description = fields.String(allow_none=True)
    start_at = fields.DateTime(required=True)
    end_at = fields.DateTime(required=True)
    location = fields.String()
    is_virtual = fields.Boolean()
    max_attendees = fields.Integer(allow_none=True)
    created_by = fields.Integer(dump_only=True)
    department_id = fields.Integer(allow_none=True)
    family_id = fields.Integer(allow_none=True)
    created_at = fields.DateTime(dump_only=True)


class EventParticipantSchema(ma.Schema):
    id = fields.Integer(dump_only=True)
    event_id = fields.Integer(required=True)
    user_id = fields.Integer(required=True)
    registered_at = fields.DateTime(dump_only=True)
    status = fields.String()
