"""Families d'Impact endpoints."""

import math

from flask import jsonify, request
from flask_jwt_extended import jwt_required, get_jwt, get_jwt_identity

from ..extensions import db
from ..models import FamilyImpact, FamilyMember, User, Role
from ..schemas.family import FamilySchema, FamilyMemberSchema
from ..schemas.user import UserSchema
from ..common.decorators import role_required
from . import families_bp

family_schema = FamilySchema()
families_schema = FamilySchema(many=True)
family_member_schema = FamilyMemberSchema()
user_schema = UserSchema()


def _can_manage_family(family: FamilyImpact, claims):
    role = claims.get("role")
    user_id = int(claims.get("sub"))
    if role == Role.ADMIN.value:
        return True
    if role == Role.FAMILY_LEAD.value and family.responsible_id == user_id:
        return True
    return False


@families_bp.get("/")
@jwt_required()
def list_families():
    families = FamilyImpact.query.order_by(FamilyImpact.name).all()
    return jsonify(families_schema.dump(families))


@families_bp.post("/")
@jwt_required()
@role_required(Role.ADMIN.value, Role.FAMILY_LEAD.value)
def create_family():
    payload = request.get_json() or {}
    errors = family_schema.validate(payload)
    if errors:
        return jsonify({"errors": errors}), 400

    family = FamilyImpact(**payload)
    db.session.add(family)
    db.session.commit()
    return jsonify(family_schema.dump(family)), 201


@families_bp.get("/<int:family_id>")
@jwt_required()
def get_family(family_id):
    family = FamilyImpact.query.get_or_404(family_id)
    members = [fm.member for fm in family.members]
    result = family_schema.dump(family)
    result["members"] = [user_schema.dump(member) for member in members]
    return jsonify(result)


@families_bp.patch("/<int:family_id>")
@jwt_required()
def update_family(family_id):
    family = FamilyImpact.query.get_or_404(family_id)
    claims = get_jwt()
    if not _can_manage_family(family, claims):
        return jsonify({"message": "Insufficient permissions"}), 403

    payload = request.get_json() or {}
    errors = family_schema.validate(payload, partial=True)
    if errors:
        return jsonify({"errors": errors}), 400

    for field, value in payload.items():
        setattr(family, field, value)
    db.session.commit()
    return jsonify(family_schema.dump(family))


@families_bp.post("/<int:family_id>/members")
@jwt_required()
def assign_to_family(family_id):
    family = FamilyImpact.query.get_or_404(family_id)
    claims = get_jwt()
    if not _can_manage_family(family, claims):
        return jsonify({"message": "Insufficient permissions"}), 403

    payload = request.get_json() or {}
    errors = family_member_schema.validate(payload)
    if errors:
        return jsonify({"errors": errors}), 400

    user = User.query.get_or_404(payload["user_id"])
    existing = FamilyMember.query.filter_by(user_id=user.id).first()
    if existing:
        if existing.family_id == family.id:
            return jsonify({"message": "Member already assigned to this family"}), 400
        existing.family_id = family.id
        db.session.commit()
        return jsonify(user_schema.dump(user))

    membership = FamilyMember(user_id=user.id, family_id=family.id)
    db.session.add(membership)
    db.session.commit()
    return jsonify(user_schema.dump(user)), 201


@families_bp.post("/find")
@jwt_required(optional=True)
def find_nearest_family():
    payload = request.get_json() or {}
    postal_code = payload.get("postal_code")
    latitude = payload.get("latitude")
    longitude = payload.get("longitude")

    query = FamilyImpact.query
    families = query.filter(FamilyImpact.latitude.isnot(None), FamilyImpact.longitude.isnot(None)).all()
    if not families:
        return jsonify({"message": "No families available"}), 404

    def haversine(lat1, lon1, lat2, lon2):
        r = 6371  # km
        phi1, phi2 = math.radians(lat1), math.radians(lat2)
        delta_phi = math.radians(lat2 - lat1)
        delta_lambda = math.radians(lon2 - lon1)
        a = (
            math.sin(delta_phi / 2) ** 2
            + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2) ** 2
        )
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        return r * c

    # If lat/long provided use that, otherwise fallback to postal code match
    if latitude is not None and longitude is not None:
        latitude = float(latitude)
        longitude = float(longitude)
        families.sort(key=lambda f: haversine(latitude, longitude, f.latitude, f.longitude))
        family = families[0]
        return jsonify({"family": family_schema.dump(family)})

    if postal_code:
        family = (
            FamilyImpact.query.filter(
                FamilyImpact.postal_code.ilike(f"{postal_code.strip()}%")
            ).first()
        )
        if family:
            return jsonify({"family": family_schema.dump(family)})

    return jsonify({"message": "No family matched the provided information"}), 404


@families_bp.post("/request/<int:family_id>")
@jwt_required()
def request_join_family(family_id):
    """Member requests to join a family, flagged for responsible follow-up."""
    user_id = get_jwt_identity()
    family = FamilyImpact.query.get_or_404(family_id)
    existing = FamilyMember.query.filter_by(user_id=user_id).first()
    if existing and existing.family_id == family.id:
        return jsonify({"message": "Already part of this family"}), 400

    # For now auto-assign; future enhancements could create approval workflow.
    if existing:
        existing.family_id = family.id
    else:
        db.session.add(FamilyMember(user_id=user_id, family_id=family.id))
    db.session.commit()
    return jsonify({"message": "Request recorded", "family": family_schema.dump(family)})
