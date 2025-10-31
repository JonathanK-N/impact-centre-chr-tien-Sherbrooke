"""Department endpoints."""

from flask import jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt

from ..extensions import db
from ..models import Department, DepartmentMember, User, Role
from ..schemas.department import DepartmentSchema, DepartmentMemberSchema
from ..schemas.user import UserSchema
from ..common.decorators import role_required, roles_to_str
from . import departments_bp

department_schema = DepartmentSchema()
department_member_schema = DepartmentMemberSchema()
department_list_schema = DepartmentSchema(many=True)
user_schema = UserSchema()
user_list_schema = UserSchema(many=True)


@departments_bp.get("/")
@jwt_required()
def list_departments():
    departments = Department.query.order_by(Department.name).all()
    return jsonify(department_list_schema.dump(departments))


@departments_bp.post("/")
@jwt_required()
@role_required(Role.ADMIN.value)
def create_department():
    payload = request.get_json() or {}
    errors = department_schema.validate(payload)
    if errors:
        return jsonify({"errors": errors}), 400
    department = Department(
        name=payload["name"],
        description=payload.get("description"),
        responsible_id=payload.get("responsible_id"),
    )
    db.session.add(department)
    db.session.commit()
    return jsonify(department_schema.dump(department)), 201


@departments_bp.get("/<int:department_id>")
@jwt_required()
def get_department(department_id):
    department = Department.query.get_or_404(department_id)
    members = [dm.member for dm in department.members]
    response = department_schema.dump(department)
    response["members"] = user_list_schema.dump(members)
    return jsonify(response)


def _can_manage_department(department: Department, claims):
    role = claims.get("role")
    user_id = claims.get("sub")
    if role == Role.ADMIN.value:
        return True
    if role == Role.DEPARTMENT_LEAD.value and department.responsible_id == int(user_id):
        return True
    return False


@departments_bp.patch("/<int:department_id>")
@jwt_required()
def update_department(department_id):
    department = Department.query.get_or_404(department_id)
    claims = get_jwt()
    if not _can_manage_department(department, claims):
        return jsonify({"message": "Insufficient permissions"}), 403

    payload = request.get_json() or {}
    errors = department_schema.validate(payload, partial=True)
    if errors:
        return jsonify({"errors": errors}), 400

    for field in {"name", "description", "responsible_id"} & payload.keys():
        setattr(department, field, payload[field])
    db.session.commit()
    return jsonify(department_schema.dump(department))


@departments_bp.delete("/<int:department_id>")
@jwt_required()
@role_required(Role.ADMIN.value)
def delete_department(department_id):
    department = Department.query.get_or_404(department_id)
    db.session.delete(department)
    db.session.commit()
    return "", 204


@departments_bp.post("/<int:department_id>/members")
@jwt_required()
def add_member(department_id):
    department = Department.query.get_or_404(department_id)
    claims = get_jwt()
    if not _can_manage_department(department, claims):
        return jsonify({"message": "Insufficient permissions"}), 403

    payload = request.get_json() or {}
    errors = department_member_schema.validate(payload)
    if errors:
        return jsonify({"errors": errors}), 400

    member = User.query.get_or_404(payload["user_id"])
    if DepartmentMember.query.filter_by(department_id=department.id, user_id=member.id).first():
        return jsonify({"message": "Member already in department"}), 400

    membership = DepartmentMember(department_id=department.id, user_id=member.id)
    db.session.add(membership)
    db.session.commit()
    return jsonify(user_schema.dump(member)), 201


@departments_bp.delete("/<int:department_id>/members/<int:user_id>")
@jwt_required()
def remove_member(department_id, user_id):
    department = Department.query.get_or_404(department_id)
    claims = get_jwt()
    if not _can_manage_department(department, claims):
        return jsonify({"message": "Insufficient permissions"}), 403

    membership = DepartmentMember.query.filter_by(
        department_id=department.id, user_id=user_id
    ).first()
    if not membership:
        return jsonify({"message": "Member not found"}), 404
    db.session.delete(membership)
    db.session.commit()
    return "", 204
