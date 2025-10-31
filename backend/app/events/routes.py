"""Event management endpoints."""

from datetime import datetime

from flask import jsonify, request
from flask_jwt_extended import get_jwt, get_jwt_identity, jwt_required

from ..extensions import db
from ..models import Event, EventParticipant, Role, Department, FamilyImpact
from ..schemas.event import EventSchema, EventParticipantSchema
from ..common.decorators import role_required
from . import events_bp

event_schema = EventSchema()
events_schema = EventSchema(many=True)
participant_schema = EventParticipantSchema()


def _can_manage_event(event: Event, claims):
    role = claims.get("role")
    user_id = int(claims.get("sub"))

    if role == Role.ADMIN.value:
        return True
    if role == Role.DEPARTMENT_LEAD.value and event.department and event.department.responsible_id == user_id:
        return True
    if role == Role.FAMILY_LEAD.value and event.family and event.family.responsible_id == user_id:
        return True
    if event.created_by == user_id:
        return True
    return False


@events_bp.get("/")
@jwt_required(optional=True)
def list_events():
    scope = request.args.get("scope")
    department_id = request.args.get("department_id", type=int)
    family_id = request.args.get("family_id", type=int)

    query = Event.query
    if scope == "department" and department_id:
        query = query.filter(Event.department_id == department_id)
    elif scope == "family" and family_id:
        query = query.filter(Event.family_id == family_id)
    elif scope == "global":
        query = query.filter(Event.department_id.is_(None), Event.family_id.is_(None))

    events = query.order_by(Event.start_at.desc()).all()
    return jsonify(events_schema.dump(events))


@events_bp.post("/")
@jwt_required()
def create_event():
    claims = get_jwt()
    role = claims.get("role")
    payload = request.get_json() or {}
    errors = event_schema.validate(payload)
    if errors:
        return jsonify({"errors": errors}), 400

    department_id = payload.get("department_id")
    family_id = payload.get("family_id")
    creator_id = get_jwt_identity()

    if department_id:
        department = Department.query.get_or_404(department_id)
        if role not in {Role.ADMIN.value, Role.DEPARTMENT_LEAD.value} or (
            role == Role.DEPARTMENT_LEAD.value and department.responsible_id != int(claims["sub"])
        ):
            return jsonify({"message": "Insufficient permissions"}), 403
    elif family_id:
        family = FamilyImpact.query.get_or_404(family_id)
        if role not in {Role.ADMIN.value, Role.FAMILY_LEAD.value} or (
            role == Role.FAMILY_LEAD.value and family.responsible_id != int(claims["sub"])
        ):
            return jsonify({"message": "Insufficient permissions"}), 403
    else:
        if role not in {Role.ADMIN.value, Role.DEPARTMENT_LEAD.value, Role.FAMILY_LEAD.value}:
            return jsonify({"message": "Insufficient permissions for global event"}), 403

    start_at = datetime.fromisoformat(payload["start_at"])
    end_at = datetime.fromisoformat(payload["end_at"])
    if end_at <= start_at:
        return jsonify({"message": "Event end time must be after start time"}), 400

    event = Event(
        title=payload["title"],
        description=payload.get("description"),
        start_at=start_at,
        end_at=end_at,
        location=payload.get("location"),
        is_virtual=payload.get("is_virtual", False),
        max_attendees=payload.get("max_attendees"),
        department_id=department_id,
        family_id=family_id,
        created_by=creator_id,
    )
    db.session.add(event)
    db.session.commit()
    return jsonify(event_schema.dump(event)), 201


@events_bp.get("/<int:event_id>")
@jwt_required()
def get_event(event_id):
    event = Event.query.get_or_404(event_id)
    data = event_schema.dump(event)
    data["participants"] = [
        participant_schema.dump(participant) for participant in event.participants
    ]
    return jsonify(data)


@events_bp.patch("/<int:event_id>")
@jwt_required()
def update_event(event_id):
    event = Event.query.get_or_404(event_id)
    claims = get_jwt()
    if not _can_manage_event(event, claims):
        return jsonify({"message": "Insufficient permissions"}), 403

    payload = request.get_json() or {}
    errors = event_schema.validate(payload, partial=True)
    if errors:
        return jsonify({"errors": errors}), 400

    for field in {"title", "description", "location", "is_virtual", "max_attendees"} & payload.keys():
        setattr(event, field, payload[field])

    if "start_at" in payload:
        event.start_at = datetime.fromisoformat(payload["start_at"])
    if "end_at" in payload:
        event.end_at = datetime.fromisoformat(payload["end_at"])

    if event.end_at <= event.start_at:
        return jsonify({"message": "Event end time must be after start time"}), 400

    db.session.commit()
    return jsonify(event_schema.dump(event))


@events_bp.delete("/<int:event_id>")
@jwt_required()
def delete_event(event_id):
    event = Event.query.get_or_404(event_id)
    if not _can_manage_event(event, get_jwt()):
        return jsonify({"message": "Insufficient permissions"}), 403
    db.session.delete(event)
    db.session.commit()
    return "", 204


@events_bp.post("/<int:event_id>/participants")
@jwt_required()
def register_for_event(event_id):
    event = Event.query.get_or_404(event_id)
    user_id = get_jwt_identity()
    if event.max_attendees and len(event.participants) >= event.max_attendees:
        return jsonify({"message": "Event is full"}), 400

    existing = EventParticipant.query.filter_by(event_id=event.id, user_id=user_id).first()
    if existing:
        return jsonify({"message": "Already registered"}), 400

    participant = EventParticipant(event_id=event.id, user_id=user_id, status="registered")
    db.session.add(participant)
    db.session.commit()
    return jsonify(participant_schema.dump(participant)), 201


@events_bp.delete("/<int:event_id>/participants/<int:user_id>")
@jwt_required()
def unregister_from_event(event_id, user_id):
    event = Event.query.get_or_404(event_id)
    claims = get_jwt()
    if user_id != int(claims.get("sub")) and not _can_manage_event(event, claims):
        return jsonify({"message": "Insufficient permissions"}), 403

    participant = EventParticipant.query.filter_by(event_id=event.id, user_id=user_id).first()
    if not participant:
        return jsonify({"message": "Participant not found"}), 404
    db.session.delete(participant)
    db.session.commit()
    return "", 204
