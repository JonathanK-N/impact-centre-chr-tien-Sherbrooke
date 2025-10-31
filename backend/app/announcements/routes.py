"""Announcement endpoints."""

from datetime import datetime

from flask import jsonify, request
from flask_jwt_extended import get_jwt, get_jwt_identity, jwt_required

from ..extensions import db
from ..models import Announcement, AnnouncementScope, Department, FamilyImpact, Role
from ..schemas.announcement import AnnouncementSchema
from . import announcements_bp

announcement_schema = AnnouncementSchema()
announcements_schema = AnnouncementSchema(many=True)


def _can_manage_announcement(announcement: Announcement, claims):
    role = claims.get("role")
    user_id = int(claims.get("sub"))

    if role == Role.ADMIN.value or announcement.author_id == user_id:
        return True
    if (
        role == Role.DEPARTMENT_LEAD.value
        and announcement.department
        and announcement.department.responsible_id == user_id
    ):
        return True
    if (
        role == Role.FAMILY_LEAD.value
        and announcement.family
        and announcement.family.responsible_id == user_id
    ):
        return True
    return False


@announcements_bp.get("/")
@jwt_required(optional=True)
def list_announcements():
    scope = request.args.get("scope")
    department_id = request.args.get("department_id", type=int)
    family_id = request.args.get("family_id", type=int)

    query = Announcement.query.order_by(Announcement.published_at.desc())
    now = datetime.utcnow()
    query = query.filter((Announcement.expires_at.is_(None)) | (Announcement.expires_at > now))

    if scope == AnnouncementScope.GLOBAL.value:
        query = query.filter(Announcement.scope == AnnouncementScope.GLOBAL)
    elif scope == AnnouncementScope.DEPARTMENT.value and department_id:
        query = query.filter(
            Announcement.scope == AnnouncementScope.DEPARTMENT,
            Announcement.department_id == department_id,
        )
    elif scope == AnnouncementScope.FAMILY.value and family_id:
        query = query.filter(
            Announcement.scope == AnnouncementScope.FAMILY,
            Announcement.family_id == family_id,
        )

    announcements = query.all()
    return jsonify(announcements_schema.dump(announcements))


@announcements_bp.post("/")
@jwt_required()
def create_announcement():
    payload = request.get_json() or {}
    errors = announcement_schema.validate(payload)
    if errors:
        return jsonify({"errors": errors}), 400

    scope_value = payload["scope"]
    try:
        scope = AnnouncementScope(scope_value)
    except ValueError:
        return jsonify({"message": "Invalid scope"}), 400

    claims = get_jwt()
    user_id = get_jwt_identity()

    if scope == AnnouncementScope.GLOBAL and claims.get("role") != Role.ADMIN.value:
        return jsonify({"message": "Only admins can publish global announcements"}), 403
    if scope == AnnouncementScope.DEPARTMENT:
        department = Department.query.get_or_404(payload.get("department_id"))
        if claims.get("role") not in {Role.ADMIN.value, Role.DEPARTMENT_LEAD.value} or (
            claims.get("role") == Role.DEPARTMENT_LEAD.value
            and department.responsible_id != int(claims["sub"])
        ):
            return jsonify({"message": "Insufficient permissions"}), 403
    if scope == AnnouncementScope.FAMILY:
        family = FamilyImpact.query.get_or_404(payload.get("family_id"))
        if claims.get("role") not in {Role.ADMIN.value, Role.FAMILY_LEAD.value} or (
            claims.get("role") == Role.FAMILY_LEAD.value
            and family.responsible_id != int(claims["sub"])
        ):
            return jsonify({"message": "Insufficient permissions"}), 403

    announcement = Announcement(
        title=payload["title"],
        body=payload["body"],
        scope=scope,
        author_id=user_id,
        department_id=payload.get("department_id"),
        family_id=payload.get("family_id"),
        expires_at=datetime.fromisoformat(payload["expires_at"]) if payload.get("expires_at") else None,
    )
    db.session.add(announcement)
    db.session.commit()
    return jsonify(announcement_schema.dump(announcement)), 201


@announcements_bp.patch("/<int:announcement_id>")
@jwt_required()
def update_announcement(announcement_id):
    announcement = Announcement.query.get_or_404(announcement_id)
    claims = get_jwt()
    if not _can_manage_announcement(announcement, claims):
        return jsonify({"message": "Insufficient permissions"}), 403

    payload = request.get_json() or {}
    errors = announcement_schema.validate(payload, partial=True)
    if errors:
        return jsonify({"errors": errors}), 400

    if "scope" in payload:
        try:
            new_scope = AnnouncementScope(payload["scope"])
        except ValueError:
            return jsonify({"message": "Invalid scope"}), 400
        announcement.scope = new_scope
    if "title" in payload:
        announcement.title = payload["title"]
    if "body" in payload:
        announcement.body = payload["body"]
    if "department_id" in payload:
        announcement.department_id = payload["department_id"]
    if "family_id" in payload:
        announcement.family_id = payload["family_id"]
    if "expires_at" in payload:
        announcement.expires_at = (
            datetime.fromisoformat(payload["expires_at"]) if payload["expires_at"] else None
        )

    db.session.commit()
    return jsonify(announcement_schema.dump(announcement))


@announcements_bp.delete("/<int:announcement_id>")
@jwt_required()
def delete_announcement(announcement_id):
    announcement = Announcement.query.get_or_404(announcement_id)
    if not _can_manage_announcement(announcement, get_jwt()):
        return jsonify({"message": "Insufficient permissions"}), 403
    db.session.delete(announcement)
    db.session.commit()
    return "", 204
