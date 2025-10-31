"""Populate development database with sample data."""

from datetime import datetime, timedelta

from flask import current_app

from .extensions import db, bcrypt
from .models import (
    User,
    Department,
    DepartmentMember,
    FamilyImpact,
    FamilyMember,
    Event,
    EventParticipant,
    Announcement,
    AnnouncementScope,
    Donation,
    MediaItem,
    Role,
    MediaType,
)


def seed():
    """Seed the database with baseline data if empty."""
    if User.query.count() > 0:
        current_app.logger.info("Database already seeded")
        return

    admin_password = bcrypt.generate_password_hash("Impact123!").decode("utf-8")
    admin = User(
        first_name="Admin",
        last_name="ICC Sherbrooke",
        email="admin@impact-sherbrooke.ca",
        password_hash=admin_password,
        role=Role.ADMIN,
        membership_status="Membre officiel",
    )

    member_password = bcrypt.generate_password_hash("Member123!").decode("utf-8")
    member = User(
        first_name="Jean",
        last_name="Tremblay",
        email="jean.tremblay@example.com",
        password_hash=member_password,
        role=Role.MEMBER,
        membership_status="Baptisé",
    )

    worship_lead = User(
        first_name="Sarah",
        last_name="Lavoie",
        email="sarah.lavoie@example.com",
        password_hash=member_password,
        role=Role.DEPARTMENT_LEAD,
        membership_status="Membre officiel",
    )

    family_lead = User(
        first_name="Marc",
        last_name="Nguyen",
        email="marc.nguyen@example.com",
        password_hash=member_password,
        role=Role.FAMILY_LEAD,
        membership_status="Membre officiel",
    )

    db.session.add_all([admin, member, worship_lead, family_lead])
    db.session.commit()

    worship = Department(
        name="Louange",
        description="Equipe de louange et d'adoration",
        responsible_id=worship_lead.id,
    )
    intercession = Department(
        name="Intercession",
        description="Equipe d'intercesseurs",
        responsible_id=admin.id,
    )
    db.session.add_all([worship, intercession])
    db.session.commit()

    db.session.add(DepartmentMember(department_id=worship.id, user_id=worship_lead.id))
    db.session.add(DepartmentMember(department_id=worship.id, user_id=member.id))
    db.session.add(DepartmentMember(department_id=intercession.id, user_id=admin.id))

    family = FamilyImpact(
        name="Famille d'Impact Nord",
        description="Groupe de maison secteur nord",
        address="123 Rue Principale",
        city="Sherbrooke",
        postal_code="J1H 1A1",
        country="Canada",
        meeting_day="Mercredi",
        meeting_time="19:00",
        latitude=45.4001,
        longitude=-71.8826,
        responsible_id=family_lead.id,
    )
    db.session.add(family)
    db.session.commit()

    db.session.add(FamilyMember(family_id=family.id, user_id=family_lead.id))
    db.session.add(FamilyMember(family_id=family.id, user_id=member.id))

    event = Event(
        title="Reunion de Louange",
        description="Soirée de louange et d'adoration",
        start_at=datetime.utcnow() + timedelta(days=3),
        end_at=datetime.utcnow() + timedelta(days=3, hours=2),
        location="Eglise ICC Sherbrooke",
        created_by=admin.id,
        department_id=worship.id,
    )
    db.session.add(event)
    db.session.commit()
    db.session.add(EventParticipant(event_id=event.id, user_id=member.id))

    announcement = Announcement(
        title="Bienvenue à ICC Sherbrooke",
        body="Rejoignez-nous ce dimanche pour un service spécial.",
        scope=AnnouncementScope.GLOBAL,
        author_id=admin.id,
    )
    db.session.add(announcement)

    donation = Donation(
        user_id=member.id,
        amount=50,
        currency="CAD",
        payment_method="stripe",
        status="completed",
    )
    db.session.add(donation)

    media = MediaItem(
        title="Prédication du dimanche",
        description="Message du pasteur principal",
        media_type=MediaType.VIDEO,
        url="https://www.youtube.com/watch?v=dQw4w9WgXcQ",
        department_id=worship.id,
    )
    db.session.add(media)

    db.session.commit()
    current_app.logger.info("Database seeded successfully")
