"""Member management endpoints."""

from flask import jsonify, request
from flask_jwt_extended import get_jwt, jwt_required

from ..extensions import db
from ..models import (
    User,
    DepartmentMember,
    FamilyMember,
    EventParticipant,
    Donation,
    Role,
)
from ..schemas.user import UserSchema
from . import members_bp

user_schema = UserSchema()
users_schema = UserSchema(many=True)


@members_bp.get("/")
@jwt_required()
def list_members():
    claims = get_jwt()
    if claims.get("role") not in {Role.ADMIN.value, Role.DEPARTMENT_LEAD.value, Role.FAMILY_LEAD.value}:
        return jsonify({"message": "Insufficient permissions"}), 403

    status = request.args.get("status")
    role = request.args.get("role")
    department_id = request.args.get("department_id", type=int)
    family_id = request.args.get("family_id", type=int)

    query = User.query
    if status:
        query = query.filter(User.membership_status == status)
    if role:
        query = query.filter(User.role == Role(role))
    if department_id:
        query = query.join(DepartmentMember).filter(DepartmentMember.department_id == department_id)
    if family_id:
        query = query.join(FamilyMember).filter(FamilyMember.family_id == family_id)

    users = query.order_by(User.last_name, User.first_name).all()
    return jsonify(users_schema.dump(users))


@members_bp.get("/<int:user_id>")
@jwt_required()
def member_detail(user_id):
    claims = get_jwt()
    requesting_role = claims.get("role")
    if requesting_role == Role.MEMBER.value and int(claims.get("sub")) != user_id:
        return jsonify({"message": "Insufficient permissions"}), 403

    user = User.query.get_or_404(user_id)
    data = user_schema.dump(user)
    data["departments"] = [
        {"id": membership.department.id, "name": membership.department.name}
        for membership in user.department_memberships
    ]
    data["family"] = (
        {"id": user.family_membership.family.id, "name": user.family_membership.family.name}
        if user.family_membership
        else None
    )
    data["events"] = [
        {"id": participant.event.id, "title": participant.event.title, "status": participant.status}
        for participant in EventParticipant.query.filter_by(user_id=user.id).all()
    ]
    data["donations"] = [
        {"id": donation.id, "amount": str(donation.amount), "created_at": donation.created_at.isoformat()}
        for donation in Donation.query.filter_by(user_id=user.id).order_by(Donation.created_at.desc()).limit(10)
    ]
    return jsonify(data)


@members_bp.patch("/<int:user_id>/status")
@jwt_required()
def update_membership_status(user_id):
    claims = get_jwt()
    if claims.get("role") not in {Role.ADMIN.value, Role.DEPARTMENT_LEAD.value}:
        return jsonify({"message": "Insufficient permissions"}), 403

    user = User.query.get_or_404(user_id)
    payload = request.get_json() or {}
    status = payload.get("membership_status")
    if not status:
        return jsonify({"message": "membership_status is required"}), 400

    user.membership_status = status
    db.session.commit()
    return jsonify(user_schema.dump(user))
