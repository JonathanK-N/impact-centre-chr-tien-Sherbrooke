"""Donation endpoints and integrations stubs."""

from decimal import Decimal
from datetime import datetime

from flask import jsonify, request
from flask_jwt_extended import get_jwt, get_jwt_identity, jwt_required

from ..extensions import db
from ..models import Donation, Role
from ..schemas.donation import DonationSchema
from . import donations_bp

donation_schema = DonationSchema()
donations_schema = DonationSchema(many=True)


@donations_bp.get("/")
@jwt_required()
def list_donations():
    claims = get_jwt()
    if claims.get("role") == Role.ADMIN.value:
        donations = Donation.query.order_by(Donation.created_at.desc()).all()
    else:
        user_id = get_jwt_identity()
        donations = Donation.query.filter_by(user_id=user_id).order_by(Donation.created_at.desc()).all()
    return jsonify(donations_schema.dump(donations))


@donations_bp.post("/")
@jwt_required()
def create_donation():
    payload = request.get_json() or {}
    errors = donation_schema.validate(payload, partial=("status",))
    if errors:
        return jsonify({"errors": errors}), 400

    user_id = get_jwt_identity()
    amount = Decimal(str(payload["amount"]))
    donation = Donation(
        user_id=user_id,
        amount=amount,
        currency=payload.get("currency", "CAD"),
        payment_method=payload.get("payment_method", "stripe"),
        status=payload.get("status", "pending"),
        receipt_url=payload.get("receipt_url"),
        created_at=datetime.utcnow(),
    )
    db.session.add(donation)
    db.session.commit()
    return jsonify(donation_schema.dump(donation)), 201


@donations_bp.get("/summary")
@jwt_required()
def donation_summary():
    claims = get_jwt()
    user_id = get_jwt_identity()

    query = Donation.query
    if claims.get("role") != Role.ADMIN.value:
        query = query.filter_by(user_id=user_id)

    donations = query.all()
    total_amount = sum(d.amount for d in donations)
    return jsonify(
        {
            "count": len(donations),
            "total_amount": str(total_amount),
            "currency": donations[0].currency if donations else "CAD",
        }
    )
