"""Marshmallow schemas for user resources."""

from marshmallow import fields, validate

from ..extensions import ma


class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        from ..models import User

        model = User
        include_fk = True
        load_instance = False
        ordered = True
        exclude = ("password_hash",)

    role = fields.String()
    membership_status = fields.String()


class RegistrationSchema(ma.Schema):
    first_name = fields.String(required=True, validate=validate.Length(min=1, max=120))
    last_name = fields.String(required=True, validate=validate.Length(min=1, max=120))
    email = fields.Email(required=True)
    password = fields.String(required=True, load_only=True, validate=validate.Length(min=8))
    phone = fields.String()


class LoginSchema(ma.Schema):
    email = fields.Email(required=True)
    password = fields.String(required=True, load_only=True)


class UpdateProfileSchema(ma.Schema):
    first_name = fields.String(validate=validate.Length(min=1, max=120))
    last_name = fields.String(validate=validate.Length(min=1, max=120))
    phone = fields.String()
    address = fields.String()
    city = fields.String()
    postal_code = fields.String()
    country = fields.String()
    date_of_birth = fields.Date(allow_none=True)
    gender = fields.String()
    marital_status = fields.String()
    church_role = fields.String()
    membership_status = fields.String()
