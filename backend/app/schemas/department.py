"""Schemas for department resources."""

from marshmallow import fields, validate

from ..extensions import ma


class DepartmentSchema(ma.Schema):
    id = fields.Integer(dump_only=True)
    name = fields.String(required=True, validate=validate.Length(min=2, max=120))
    description = fields.String(allow_none=True)
    responsible_id = fields.Integer(allow_none=True)
    created_at = fields.DateTime(dump_only=True)


class DepartmentMemberSchema(ma.Schema):
    id = fields.Integer(dump_only=True)
    department_id = fields.Integer(required=True)
    user_id = fields.Integer(required=True)
    joined_at = fields.DateTime(dump_only=True)
