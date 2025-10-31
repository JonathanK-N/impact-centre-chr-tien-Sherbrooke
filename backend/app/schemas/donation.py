"""Schemas for donations."""

from marshmallow import fields, validate

from ..extensions import ma


class DonationSchema(ma.Schema):
    id = fields.Integer(dump_only=True)
    user_id = fields.Integer(dump_only=True)
    amount = fields.Decimal(required=True, as_string=True)
    currency = fields.String(validate=validate.Length(max=10))
    payment_method = fields.String()
    status = fields.String()
    receipt_url = fields.String()
    created_at = fields.DateTime(dump_only=True)
