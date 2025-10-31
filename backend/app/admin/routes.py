"""Administrative endpoints."""

from flask import jsonify, request
from flask_jwt_extended import jwt_required, get_jwt

from ..extensions import db
from ..models import (
    User,
    Department,
    FamilyImpact,
    Donation,
    Event,
    Role,
)
from ..schemas.department import DepartmentSchema
from ..schemas.family import FamilySchema
from . import admin_bp

department_schema = DepartmentSchema()
family_schema = FamilySchema()


@admin_bp.get("/dashboard")
@jwt_required()
def dashboard_summary():
    claims = get_jwt()
    if claims.get("role") != Role.ADMIN.value:
        return jsonify({"message": "Insufficient permissions"}), 403

    summary = {
        "members": User.query.count(),
        "departments": Department.query.count(),
        "families": FamilyImpact.query.count(),
        "events": Event.query.count(),
        "donations_total": str(sum(d.amount for d in Donation.query.all())),
    }
    return jsonify(summary)


@admin_bp.post("/departments/<int:department_id>/assign")
@jwt_required()
def assign_department_lead(department_id):
    claims = get_jwt()
    if claims.get("role") != Role.ADMIN.value:
        return jsonify({"message": "Insufficient permissions"}), 403

    payload = request.get_json() or {}
    user_id = payload.get("user_id")
    if not user_id:
        return jsonify({"message": "user_id is required"}), 400

    department = Department.query.get_or_404(department_id)
    user = User.query.get_or_404(user_id)
    department.responsible_id = user.id
    user.role = Role.DEPARTMENT_LEAD
    db.session.commit()
    return jsonify(department_schema.dump(department))


@admin_bp.post("/families/<int:family_id>/assign")
@jwt_required()
def assign_family_lead(family_id):
    claims = get_jwt()
    if claims.get("role") != Role.ADMIN.value:
        return jsonify({"message": "Insufficient permissions"}), 403

    payload = request.get_json() or {}
    user_id = payload.get("user_id")
    if not user_id:
        return jsonify({"message": "user_id is required"}), 400

    family = FamilyImpact.query.get_or_404(family_id)
    user = User.query.get_or_404(user_id)
    family.responsible_id = user.id
    user.role = Role.FAMILY_LEAD
    db.session.commit()
    return jsonify(family_schema.dump(family))
