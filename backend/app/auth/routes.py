"""Authentication endpoints."""

from datetime import datetime

from flask import request, jsonify
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    get_jwt_identity,
    jwt_required,
    get_jwt,
)

from ..extensions import db, bcrypt
from ..models import User, Role
from ..schemas.user import RegistrationSchema, LoginSchema, UserSchema, UpdateProfileSchema
from ..common.decorators import role_required
from . import auth_bp

registration_schema = RegistrationSchema()
login_schema = LoginSchema()
user_schema = UserSchema()
profile_update_schema = UpdateProfileSchema()


@auth_bp.post("/register")
def register():
    """Register a new member."""
    payload = request.get_json() or {}
    errors = registration_schema.validate(payload)
    if errors:
        return jsonify({"errors": errors}), 400

    if User.query.filter_by(email=payload["email"].lower()).first():
        return jsonify({"message": "Email already registered"}), 400

    password_hash = bcrypt.generate_password_hash(payload["password"]).decode("utf-8")
    user = User(
        first_name=payload["first_name"],
        last_name=payload["last_name"],
        email=payload["email"].lower(),
        password_hash=password_hash,
        phone=payload.get("phone"),
        membership_status="Nouveau",
        role=Role.MEMBER,
        created_at=datetime.utcnow(),
    )
    db.session.add(user)
    db.session.commit()

    access_token = create_access_token(identity=user.id, additional_claims={"role": user.role.value})
    refresh_token = create_refresh_token(identity=user.id, additional_claims={"role": user.role.value})

    return (
        jsonify(
            {
                "access_token": access_token,
                "refresh_token": refresh_token,
                "user": user_schema.dump(user),
            }
        ),
        201,
    )


@auth_bp.post("/login")
def login():
    """Authenticate a user and issue JWT tokens."""
    payload = request.get_json() or {}
    errors = login_schema.validate(payload)
    if errors:
        return jsonify({"errors": errors}), 400

    user = User.query.filter_by(email=payload["email"].lower()).first()
    if not user or not bcrypt.check_password_hash(user.password_hash, payload["password"]):
        return jsonify({"message": "Invalid email or password"}), 401

    access_token = create_access_token(identity=user.id, additional_claims={"role": user.role.value})
    refresh_token = create_refresh_token(identity=user.id, additional_claims={"role": user.role.value})

    return jsonify({"access_token": access_token, "refresh_token": refresh_token, "user": user_schema.dump(user)})


@auth_bp.post("/refresh")
@jwt_required(refresh=True)
def refresh():
    """Refresh the access token."""
    identity = get_jwt_identity()
    claims = get_jwt()
    role = claims.get("role")
    new_access = create_access_token(identity=identity, additional_claims={"role": role})
    return jsonify({"access_token": new_access})


@auth_bp.get("/me")
@jwt_required()
def me():
    """Return the authenticated user's profile."""
    identity = get_jwt_identity()
    user = User.query.get_or_404(identity)
    return jsonify(user_schema.dump(user))


@auth_bp.patch("/me")
@jwt_required()
def update_profile():
    """Update current user's profile fields."""
    identity = get_jwt_identity()
    user = User.query.get_or_404(identity)
    payload = request.get_json() or {}
    errors = profile_update_schema.validate(payload)
    if errors:
        return jsonify({"errors": errors}), 400

    for field, value in payload.items():
        setattr(user, field, value)
    user.updated_at = datetime.utcnow()
    db.session.commit()
    return jsonify(user_schema.dump(user))


@auth_bp.post("/promote/<int:user_id>")
@jwt_required()
@role_required(Role.ADMIN.value)
def promote_member(user_id):
    """Promote a member to a specific role."""
    payload = request.get_json() or {}
    role_value = payload.get("role")
    if not role_value or role_value not in {r.value for r in Role}:
        return jsonify({"message": "Invalid role"}), 400

    user = User.query.get_or_404(user_id)
    user.role = Role(role_value)
    db.session.commit()
    return jsonify(user_schema.dump(user))
