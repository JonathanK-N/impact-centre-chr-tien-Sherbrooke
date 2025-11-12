#!/usr/bin/env python3
"""
Outil de peuplement rapide pour Impact Centre Chrétien Sherbrooke.
Exécutez `python seed/seed.py` pour (ré)initialiser la base et afficher un aperçu
des départements, des Familles d'Impact et des événements créés.
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from app import create_app, db  # noqa: E402
from app.models.department import Department  # noqa: E402
from app.models.family_impact import FamilyImpact  # noqa: E402
from app.models.event import Event  # noqa: E402
from app.models.user import User  # noqa: E402
from init_app import init_database  # noqa: E402


def show_details() -> None:
    """Affiche un aperçu lisible des données de démonstration."""
    print("\n[DÉTAILS] Utilisateurs disponibles :")
    for user in User.query.order_by(User.first_name).all():
        print(f" - {user.full_name} ({user.email}) · rôle: {user.role}")

    print("\n[DÉPARTEMENTS]")
    departments = Department.query.order_by(Department.name).all()
    if not departments:
        print("   Aucun département enregistré pour le moment.")
    for dept in departments:
        members = sum(1 for m in dept.members if m.is_active)
        responsible = dept.responsible.full_name if dept.responsible else "Non assigné"
        print(f" - {dept.name} · Responsable: {responsible} · Membres actifs: {members}")

    print("\n[Familles d'Impact]")
    families = FamilyImpact.query.order_by(FamilyImpact.name).all()
    if not families:
        print("   Aucune famille enregistrée.")
    for family in families:
        spots = f"{family.current_members_count}/{family.max_capacity}"
        print(f" - {family.name} ({spots}) · Adresse: {family.address}")

    print("\n[Événements]")
    events = Event.query.order_by(Event.start_date).all()
    if not events:
        print("   Aucun événement planifié.")
    for event in events:
        scope = getattr(event, 'event_type', 'Communautaire')
        print(f" - {event.title} · {event.start_date:%d/%m/%Y} · Portée: {scope}")


def main() -> None:
    config_name = os.environ.get('FLASK_CONFIG', 'development')
    app = create_app(config_name)

    with app.app_context():
        init_database()
        db.session.commit()
        show_details()

    print("\n[TERMINE] Consultez les informations ci-dessus pour plus de détails.")


if __name__ == '__main__':
    main()
