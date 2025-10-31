"""Media endpoints."""

from flask import jsonify, request
from flask_jwt_extended import get_jwt, jwt_required

from ..extensions import db
from ..models import MediaItem, Role, Department, FamilyImpact
from ..schemas.media import MediaSchema
from . import media_bp

media_schema = MediaSchema()
media_list_schema = MediaSchema(many=True)


def _can_manage_media(item: MediaItem, claims):
    role = claims.get("role")
    user_id = int(claims.get("sub"))
    if role == Role.ADMIN.value:
        return True
    if role == Role.DEPARTMENT_LEAD.value and item.department and item.department.responsible_id == user_id:
        return True
    if role == Role.FAMILY_LEAD.value and item.family and item.family.responsible_id == user_id:
        return True
    return False


@media_bp.get("/")
@jwt_required(optional=True)
def list_media():
    media_type = request.args.get("media_type")
    department_id = request.args.get("department_id", type=int)
    family_id = request.args.get("family_id", type=int)

    query = MediaItem.query.order_by(MediaItem.published_at.desc())
    if media_type:
        query = query.filter(MediaItem.media_type == media_type)
    if department_id:
        query = query.filter(MediaItem.department_id == department_id)
    if family_id:
        query = query.filter(MediaItem.family_id == family_id)

    items = query.all()
    return jsonify(media_list_schema.dump(items))


@media_bp.post("/")
@jwt_required()
def create_media():
    payload = request.get_json() or {}
    errors = media_schema.validate(payload)
    if errors:
        return jsonify({"errors": errors}), 400

    claims = get_jwt()
    department_id = payload.get("department_id")
    family_id = payload.get("family_id")

    if department_id:
        department = Department.query.get_or_404(department_id)
        if claims.get("role") not in {Role.ADMIN.value, Role.DEPARTMENT_LEAD.value} or (
            claims.get("role") == Role.DEPARTMENT_LEAD.value
            and department.responsible_id != int(claims["sub"])
        ):
            return jsonify({"message": "Insufficient permissions"}), 403
    if family_id:
        family = FamilyImpact.query.get_or_404(family_id)
        if claims.get("role") not in {Role.ADMIN.value, Role.FAMILY_LEAD.value} or (
            claims.get("role") == Role.FAMILY_LEAD.value
            and family.responsible_id != int(claims["sub"])
        ):
            return jsonify({"message": "Insufficient permissions"}), 403

    item = MediaItem(**payload)
    db.session.add(item)
    db.session.commit()
    return jsonify(media_schema.dump(item)), 201


@media_bp.patch("/<int:media_id>")
@jwt_required()
def update_media(media_id):
    item = MediaItem.query.get_or_404(media_id)
    claims = get_jwt()
    if not _can_manage_media(item, claims):
        return jsonify({"message": "Insufficient permissions"}), 403

    payload = request.get_json() or {}
    errors = media_schema.validate(payload, partial=True)
    if errors:
        return jsonify({"errors": errors}), 400

    for field, value in payload.items():
        setattr(item, field, value)
    db.session.commit()
    return jsonify(media_schema.dump(item))


@media_bp.delete("/<int:media_id>")
@jwt_required()
def delete_media(media_id):
    item = MediaItem.query.get_or_404(media_id)
    if not _can_manage_media(item, get_jwt()):
        return jsonify({"message": "Insufficient permissions"}), 403
    db.session.delete(item)
    db.session.commit()
    return "", 204
