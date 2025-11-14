import os
from flask import Flask
from app import create_app, db
from app.models.user import User
from app.models.department import Department, DepartmentMember
from app.models.family_impact import FamilyImpact, FamilyMember
from app.models.event import Event, EventParticipant
from app.models.announcement import Announcement
from app.models.donation import Donation

app = create_app(os.getenv('FLASK_CONFIG') or 'default')

# Initialiser la base de données au démarrage
with app.app_context():
    try:
        db.create_all()
    except Exception as e:
        print(f"Erreur lors de l'initialisation de la base de données: {e}")

@app.shell_context_processor
def make_shell_context():
    return dict(
        db=db,
        User=User,
        Department=Department,
        DepartmentMember=DepartmentMember,
        FamilyImpact=FamilyImpact,
        FamilyMember=FamilyMember,
        Event=Event,
        EventParticipant=EventParticipant,
        Announcement=Announcement,
        Donation=Donation
    )

@app.cli.command()
def init_db():
    """Initialize the database with sample data."""
    db.create_all()
    
    # Créer un utilisateur admin
    admin = User(
        email='admin@impactcentre.ca',
        first_name='Admin',
        last_name='Système',
        role='Admin',
        membership_status='Membre officiel'
    )
    admin.set_password('admin123')
    db.session.add(admin)
    
    # Créer quelques utilisateurs de test
    users_data = [
        {
            'email': 'jean.dupont@email.com',
            'first_name': 'Jean',
            'last_name': 'Dupont',
            'phone': '819-555-0101',
            'role': 'Responsable Département',
            'membership_status': 'Membre officiel',
            'church_role': 'Pasteur'
        },
        {
            'email': 'marie.martin@email.com',
            'first_name': 'Marie',
            'last_name': 'Martin',
            'phone': '819-555-0102',
            'role': 'Responsable Famille',
            'membership_status': 'Baptisé',
            'church_role': 'Responsable Louange'
        },
        {
            'email': 'pierre.gagnon@email.com',
            'first_name': 'Pierre',
            'last_name': 'Gagnon',
            'phone': '819-555-0103',
            'membership_status': 'En formation'
        }
    ]
    
    users = []
    for user_data in users_data:
        user = User(**user_data)
        user.set_password('password123')
        users.append(user)
        db.session.add(user)
    
    db.session.commit()
    
    # Créer des départements
    departments_data = [
        {
            'name': 'Louange et Adoration',
            'description': 'Département responsable de la musique et des chants lors des cultes',
            'responsible_id': users[1].id
        },
        {
            'name': 'Intercession',
            'description': 'Groupe de prière pour l\'église et la communauté',
            'responsible_id': users[0].id
        },
        {
            'name': 'Jeunesse',
            'description': 'Ministère dédié aux jeunes de 12 à 25 ans'
        },
        {
            'name': 'Enfants',
            'description': 'École du dimanche et activités pour les enfants'
        }
    ]
    
    departments = []
    for dept_data in departments_data:
        dept = Department(**dept_data)
        departments.append(dept)
        db.session.add(dept)
    
    db.session.commit()
    
    # Créer des Familles d'Impact
    families_data = [
        {
            'name': 'Famille Espoir',
            'description': 'Groupe de maison axé sur l\'étude biblique et la communion fraternelle',
            'address': '123 Rue King Ouest, Sherbrooke, QC J1H 1N8',
            'latitude': 45.4042,
            'longitude': -71.8929,
            'postal_code': 'J1H 1N8',
            'meeting_day': 'Mercredi',
            'meeting_time': '19:00',
            'responsible_id': users[1].id,
            'max_capacity': 12
        },
        {
            'name': 'Famille Grâce',
            'description': 'Groupe familial pour couples et familles avec enfants',
            'address': '456 Rue Wellington Sud, Sherbrooke, QC J1H 5C5',
            'latitude': 45.3986,
            'longitude': -71.8958,
            'postal_code': 'J1H 5C5',
            'meeting_day': 'Vendredi',
            'meeting_time': '19:30',
            'max_capacity': 15
        }
    ]
    
    families = []
    for family_data in families_data:
        from datetime import time
        if 'meeting_time' in family_data:
            hour, minute = map(int, family_data['meeting_time'].split(':'))
            family_data['meeting_time'] = time(hour, minute)
        
        family = FamilyImpact(**family_data)
        families.append(family)
        db.session.add(family)
    
    db.session.commit()
    
    # Créer des événements
    from datetime import datetime, timedelta
    
    events_data = [
        {
            'title': 'Culte du Dimanche',
            'description': 'Culte dominical avec louange, prédication et communion',
            'start_date': datetime.now() + timedelta(days=7),
            'end_date': datetime.now() + timedelta(days=7, hours=2),
            'location': 'Sanctuaire principal',
            'address': '789 Rue Galt Ouest, Sherbrooke, QC',
            'event_type': 'General',
            'organizer_id': users[0].id,
            'max_participants': 200
        },
        {
            'title': 'Soirée de Louange',
            'description': 'Soirée spéciale de louange et d\'adoration',
            'start_date': datetime.now() + timedelta(days=14),
            'end_date': datetime.now() + timedelta(days=14, hours=3),
            'location': 'Sanctuaire principal',
            'event_type': 'Department',
            'target_department_id': departments[0].id,
            'organizer_id': users[1].id,
            'max_participants': 150
        }
    ]
    
    for event_data in events_data:
        event = Event(**event_data)
        db.session.add(event)
    
    db.session.commit()
    
    # Créer des annonces
    announcements_data = [
        {
            'title': 'Bienvenue sur notre nouvelle plateforme!',
            'content': 'Nous sommes heureux de vous présenter notre nouvelle plateforme communautaire. Vous pouvez maintenant gérer votre profil, rejoindre des départements, vous inscrire aux événements et bien plus encore!',
            'announcement_type': 'General',
            'priority': 'High',
            'author_id': admin.id,
            'is_pinned': True
        },
        {
            'title': 'Répétition de la chorale',
            'content': 'Répétition générale pour la chorale ce jeudi à 19h30. Présence obligatoire pour tous les membres.',
            'announcement_type': 'Department',
            'target_department_id': departments[0].id,
            'priority': 'Normal',
            'author_id': users[1].id
        }
    ]
    
    for ann_data in announcements_data:
        announcement = Announcement(**ann_data)
        db.session.add(announcement)
    
    db.session.commit()
    
    print("Base de données initialisée avec succès!")
    print("Utilisateur admin créé: admin@impactcentre.ca / admin123")
    print("Utilisateurs de test créés avec le mot de passe: password123")

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)