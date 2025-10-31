"""Database models for the Impact Centre Chretien Sherbrooke platform."""

from __future__ import annotations

import enum
from datetime import datetime

from sqlalchemy import Enum, CheckConstraint, UniqueConstraint

from .extensions import db


class Role(enum.Enum):
    ADMIN = "admin"
    DEPARTMENT_LEAD = "department_lead"
    FAMILY_LEAD = "family_lead"
    MEMBER = "member"


class AnnouncementScope(enum.Enum):
    GLOBAL = "global"
    DEPARTMENT = "department"
    FAMILY = "family"


class MediaType(enum.Enum):
    VIDEO = "video"
    AUDIO = "audio"
    DOCUMENT = "document"


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(120), nullable=False)
    last_name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    phone = db.Column(db.String(50))
    address = db.Column(db.String(255))
    city = db.Column(db.String(120))
    postal_code = db.Column(db.String(20))
    country = db.Column(db.String(120))
    date_of_birth = db.Column(db.Date)
    gender = db.Column(db.String(20))
    marital_status = db.Column(db.String(50))
    church_role = db.Column(db.String(120))
    membership_status = db.Column(db.String(50), default="Nouveau")
    role = db.Column(Enum(Role), default=Role.MEMBER, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )

    department_memberships = db.relationship(
        "DepartmentMember", back_populates="member", cascade="all, delete-orphan"
    )
    family_membership = db.relationship(
        "FamilyMember",
        back_populates="member",
        uselist=False,
        cascade="all, delete-orphan",
    )
    donations = db.relationship("Donation", back_populates="donor", cascade="all, delete-orphan")
    announcements = db.relationship("Announcement", back_populates="author")
    events_created = db.relationship("Event", back_populates="created_by_user")

    def __repr__(self):
        return f"<User {self.email}>"


class Department(db.Model):
    __tablename__ = "departments"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False, unique=True)
    description = db.Column(db.Text)
    responsible_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    responsible = db.relationship("User", foreign_keys=[responsible_id])
    members = db.relationship(
        "DepartmentMember",
        back_populates="department",
        cascade="all, delete-orphan",
    )
    announcements = db.relationship("Announcement", back_populates="department")
    events = db.relationship("Event", back_populates="department")

    def __repr__(self):
        return f"<Department {self.name}>"


class DepartmentMember(db.Model):
    __tablename__ = "department_members"
    __table_args__ = (UniqueConstraint("department_id", "user_id", name="uniq_department_member"),)

    id = db.Column(db.Integer, primary_key=True)
    department_id = db.Column(db.Integer, db.ForeignKey("departments.id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    joined_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    department = db.relationship("Department", back_populates="members")
    member = db.relationship("User", back_populates="department_memberships")


class FamilyImpact(db.Model):
    __tablename__ = "families_impact"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False, unique=True)
    description = db.Column(db.Text)
    address = db.Column(db.String(255))
    city = db.Column(db.String(120))
    postal_code = db.Column(db.String(20))
    country = db.Column(db.String(120))
    meeting_day = db.Column(db.String(20))
    meeting_time = db.Column(db.String(20))
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    responsible_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    responsible = db.relationship("User", foreign_keys=[responsible_id])
    members = db.relationship(
        "FamilyMember",
        back_populates="family",
        cascade="all, delete-orphan",
    )
    announcements = db.relationship("Announcement", back_populates="family")
    events = db.relationship("Event", back_populates="family")

    def __repr__(self):
        return f"<FamilyImpact {self.name}>"


class FamilyMember(db.Model):
    __tablename__ = "family_members"

    id = db.Column(db.Integer, primary_key=True)
    family_id = db.Column(db.Integer, db.ForeignKey("families_impact.id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, unique=True)
    joined_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    family = db.relationship("FamilyImpact", back_populates="members")
    member = db.relationship("User", back_populates="family_membership")


class Event(db.Model):
    __tablename__ = "events"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    start_at = db.Column(db.DateTime, nullable=False)
    end_at = db.Column(db.DateTime, nullable=False)
    location = db.Column(db.String(255))
    is_virtual = db.Column(db.Boolean, default=False)
    max_attendees = db.Column(db.Integer)
    created_by = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    department_id = db.Column(db.Integer, db.ForeignKey("departments.id"))
    family_id = db.Column(db.Integer, db.ForeignKey("families_impact.id"))
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    created_by_user = db.relationship("User", back_populates="events_created")
    department = db.relationship("Department", back_populates="events")
    family = db.relationship("FamilyImpact", back_populates="events")
    participants = db.relationship(
        "EventParticipant",
        back_populates="event",
        cascade="all, delete-orphan",
    )

    __table_args__ = (
        CheckConstraint(
            "(department_id IS NULL AND family_id IS NULL) OR "
            "(department_id IS NOT NULL AND family_id IS NULL) OR "
            "(department_id IS NULL AND family_id IS NOT NULL)",
            name="check_event_scope",
        ),
    )


class EventParticipant(db.Model):
    __tablename__ = "event_participants"
    __table_args__ = (UniqueConstraint("event_id", "user_id", name="uniq_event_participant"),)

    id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey("events.id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    registered_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    status = db.Column(db.String(20), default="registered")

    event = db.relationship("Event", back_populates="participants")
    member = db.relationship("User")


class Announcement(db.Model):
    __tablename__ = "announcements"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    body = db.Column(db.Text, nullable=False)
    scope = db.Column(Enum(AnnouncementScope), default=AnnouncementScope.GLOBAL, nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    department_id = db.Column(db.Integer, db.ForeignKey("departments.id"), nullable=True)
    family_id = db.Column(db.Integer, db.ForeignKey("families_impact.id"), nullable=True)
    published_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    expires_at = db.Column(db.DateTime)

    author = db.relationship("User", back_populates="announcements")
    department = db.relationship("Department", back_populates="announcements")
    family = db.relationship("FamilyImpact", back_populates="announcements")


class Donation(db.Model):
    __tablename__ = "donations"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    currency = db.Column(db.String(10), default="CAD")
    payment_method = db.Column(db.String(50))
    status = db.Column(db.String(20), default="pending")
    receipt_url = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    donor = db.relationship("User", back_populates="donations")


class MediaItem(db.Model):
    __tablename__ = "media_items"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    media_type = db.Column(Enum(MediaType), nullable=False)
    url = db.Column(db.String(500), nullable=False)
    published_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    tags = db.Column(db.String(255))
    department_id = db.Column(db.Integer, db.ForeignKey("departments.id"))
    family_id = db.Column(db.Integer, db.ForeignKey("families_impact.id"))

    department = db.relationship("Department")
    family = db.relationship("FamilyImpact")
