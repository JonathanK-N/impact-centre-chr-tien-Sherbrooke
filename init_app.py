#!/usr/bin/env python3
"""
Script d'initialisation pour Impact Centre Chrétien Sherbrooke
Ce script configure l'application et crée les données de démonstration
"""

import os
import sys
from datetime import datetime, timedelta, time
from decimal import Decimal

# Ajouter le répertoire racine au path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from app.models.user import User
from app.models.department import Department, DepartmentMember
from app.models.family_impact import FamilyImpact, FamilyMember
from app.models.event import Event, EventParticipant
from app.models.announcement import Announcement
from app.models.donation import Donation

def init_database():
    """Initialise la base de données avec des données de démonstration"""
    
    print("[INFO] Initialisation de la base de données...")
    
    # Créer toutes les tables
    db.create_all()
    print("[OK] Tables créées")
    
    # Vérifier si des données existent déjà
    try:
        if User.query.first():
            print("[INFO] Données existantes détectées, pas de recréation")
            return
    except:
        print("[INFO] Première initialisation de la base de données")
    
    # Créer l'utilisateur administrateur
    admin = User(
        email='admin@impactcentre.ca',
        first_name='Admin',
        last_name='Système',
        role='Admin',
        membership_status='Membre officiel',
        phone='819-555-0000'
    )
    admin.set_password('admin123')
    db.session.add(admin)
    print("[USER] Administrateur créé: admin@impactcentre.ca / admin123")
    
    # Créer des utilisateurs de test
    users_data = [
        {
            'email': 'jean.dupont@email.com',
            'first_name': 'Jean',
            'last_name': 'Dupont',
            'phone': '819-555-0101',
            'role': 'Responsable Département',
            'membership_status': 'Membre officiel',
            'church_role': 'Pasteur',
            'address': '123 Rue King Ouest, Sherbrooke, QC J1H 1N8',
            'gender': 'M',
            'marital_status': 'Marié(e)'
        },
        {
            'email': 'marie.martin@email.com',
            'first_name': 'Marie',
            'last_name': 'Martin',
            'phone': '819-555-0102',
            'role': 'Responsable Famille',
            'membership_status': 'Baptisé',
            'church_role': 'Responsable Louange',
            'address': '456 Rue Wellington Sud, Sherbrooke, QC J1H 5C5',
            'gender': 'F',
            'marital_status': 'Célibataire'
        },
        {
            'email': 'pierre.gagnon@email.com',
            'first_name': 'Pierre',
            'last_name': 'Gagnon',
            'phone': '819-555-0103',
            'membership_status': 'En formation',
            'church_role': 'Intercesseur',
            'address': '789 Rue Galt Ouest, Sherbrooke, QC J1H 2B3',
            'gender': 'M',
            'marital_status': 'Marié(e)'
        },
        {
            'email': 'sophie.lavoie@email.com',
            'first_name': 'Sophie',
            'last_name': 'Lavoie',
            'phone': '819-555-0104',
            'membership_status': 'Nouveau',
            'address': '321 Rue Portland, Sherbrooke, QC J1H 2Y7',
            'gender': 'F',
            'marital_status': 'Célibataire'
        }
    ]
    
    users = []
    for user_data in users_data:
        user = User(**user_data)
        user.set_password('password123')
        users.append(user)
        db.session.add(user)
    
    db.session.commit()
    print(f"[USERS] {len(users)} utilisateurs de test créés (mot de passe: password123)")
    
    # Créer des départements
    departments_data = [
        {
            'name': 'Louange et Adoration',
            'description': 'Département responsable de la musique et des chants lors des cultes. Nous recherchons des musiciens, chanteurs et techniciens son.',
            'responsible_id': users[1].id
        },
        {
            'name': 'Intercession',
            'description': 'Groupe de prière pour l\'église et la communauté. Nous nous réunissons pour prier pour les besoins de notre église et de notre ville.',
            'responsible_id': users[0].id
        },
        {
            'name': 'Jeunesse',
            'description': 'Ministère dédié aux jeunes de 12 à 25 ans. Activités, camps, études bibliques et événements spéciaux pour les jeunes.',
            'responsible_id': users[2].id
        },
        {
            'name': 'Enfants',
            'description': 'École du dimanche et activités pour les enfants de 3 à 11 ans. Enseignement biblique adapté à leur âge.',
            'responsible_id': users[1].id
        },
        {
            'name': 'Accueil',
            'description': 'Équipe chargée d\'accueillir les visiteurs et nouveaux membres. Premier contact avec notre communauté.',
            'responsible_id': users[0].id
        }
    ]
    
    departments = []
    for dept_data in departments_data:
        dept = Department(**dept_data)
        departments.append(dept)
        db.session.add(dept)
    
    db.session.commit()
    print(f"[DEPT] {len(departments)} départements créés")
    
    # Ajouter des membres aux départements
    dept_memberships = [
        (users[0].id, departments[0].id),  # Jean -> Louange
        (users[0].id, departments[1].id),  # Jean -> Intercession
        (users[1].id, departments[0].id),  # Marie -> Louange
        (users[2].id, departments[1].id),  # Pierre -> Intercession
        (users[2].id, departments[2].id),  # Pierre -> Jeunesse
        (users[3].id, departments[3].id),  # Sophie -> Enfants
    ]
    
    for user_id, dept_id in dept_memberships:
        membership = DepartmentMember(user_id=user_id, department_id=dept_id)
        db.session.add(membership)
    
    db.session.commit()
    print("[OK] Membres ajoutés aux départements")
    
    # Créer des Familles d'Impact
    families_data = [
        {
            'name': 'Famille Espoir',
            'description': 'Groupe de maison axé sur l\'étude biblique et la communion fraternelle. Nous explorons ensemble les Écritures dans une atmosphère détendue.',
            'address': '123 Rue King Ouest, Sherbrooke, QC J1H 1N8',
            'latitude': 45.4042,
            'longitude': -71.8929,
            'postal_code': 'J1H 1N8',
            'meeting_day': 'Mercredi',
            'meeting_time': time(19, 0),
            'responsible_id': users[1].id,
            'max_capacity': 12
        },
        {
            'name': 'Famille Grâce',
            'description': 'Groupe familial pour couples et familles avec enfants. Nous partageons nos expériences de parents chrétiens et soutenons nos enfants.',
            'address': '456 Rue Wellington Sud, Sherbrooke, QC J1H 5C5',
            'latitude': 45.3986,
            'longitude': -71.8958,
            'postal_code': 'J1H 5C5',
            'meeting_day': 'Vendredi',
            'meeting_time': time(19, 30),
            'responsible_id': users[0].id,
            'max_capacity': 15
        },
        {
            'name': 'Famille Jeunesse',
            'description': 'Groupe spécialement conçu pour les jeunes adultes (18-30 ans). Discussions sur la foi, la carrière, les relations et les défis de la vie moderne.',
            'address': '789 Rue Galt Ouest, Sherbrooke, QC J1H 2B3',
            'latitude': 45.4015,
            'longitude': -71.8845,
            'postal_code': 'J1H 2B3',
            'meeting_day': 'Samedi',
            'meeting_time': time(18, 0),
            'responsible_id': users[2].id,
            'max_capacity': 10
        }
    ]
    
    families = []
    for family_data in families_data:
        family = FamilyImpact(**family_data)
        families.append(family)
        db.session.add(family)
    
    db.session.commit()
    print(f"[FAMILIES] {len(families)} Familles d'Impact créées")
    
    # Ajouter des membres aux familles
    family_memberships = [
        (users[0].id, families[1].id, 'Approved'),  # Jean -> Famille Grâce
        (users[1].id, families[0].id, 'Approved'),  # Marie -> Famille Espoir
        (users[2].id, families[2].id, 'Approved'),  # Pierre -> Famille Jeunesse
        (users[3].id, families[0].id, 'Pending'),   # Sophie -> Famille Espoir (en attente)
    ]
    
    for user_id, family_id, status in family_memberships:
        membership = FamilyMember(
            user_id=user_id, 
            family_id=family_id, 
            status=status,
            is_active=(status == 'Approved')
        )
        db.session.add(membership)
    
    db.session.commit()
    print("[OK] Membres ajoutés aux Familles d'Impact")
    
    # Créer des événements
    now = datetime.now()
    events_data = [
        {
            'title': 'Culte du Dimanche',
            'description': 'Culte dominical avec louange, prédication et communion fraternelle. Venez nombreux pour ce moment de recueillement et de partage.',
            'start_date': now + timedelta(days=7 - now.weekday() + 6),  # Prochain dimanche
            'end_date': now + timedelta(days=7 - now.weekday() + 6, hours=2),
            'location': 'Sanctuaire principal',
            'address': '789 Rue Galt Ouest, Sherbrooke, QC',
            'event_type': 'General',
            'organizer_id': users[0].id,
            'max_participants': 200,
            'registration_required': False
        },
        {
            'title': 'Soirée de Louange',
            'description': 'Soirée spéciale de louange et d\'adoration avec des chants contemporains et traditionnels. Moment privilégié de communion avec Dieu.',
            'start_date': now + timedelta(days=14),
            'end_date': now + timedelta(days=14, hours=3),
            'location': 'Sanctuaire principal',
            'address': '789 Rue Galt Ouest, Sherbrooke, QC',
            'event_type': 'Department',
            'target_department_id': departments[0].id,
            'organizer_id': users[1].id,
            'max_participants': 150,
            'registration_required': True,
            'registration_deadline': now + timedelta(days=12)
        },
        {
            'title': 'Retraite Jeunesse',
            'description': 'Week-end de retraite pour les jeunes avec enseignements, activités et temps de communion. Hébergement et repas inclus.',
            'start_date': now + timedelta(days=21),
            'end_date': now + timedelta(days=23),
            'location': 'Centre de retraite Mont-Orford',
            'address': 'Mont-Orford, QC',
            'event_type': 'Department',
            'target_department_id': departments[2].id,
            'organizer_id': users[2].id,
            'max_participants': 30,
            'registration_required': True,
            'registration_deadline': now + timedelta(days=14)
        },
        {
            'title': 'Conférence Familiale',
            'description': 'Conférence sur les valeurs familiales chrétiennes avec des intervenants spécialisés. Garderie disponible pour les enfants.',
            'start_date': now + timedelta(days=28),
            'end_date': now + timedelta(days=28, hours=6),
            'location': 'Salle communautaire',
            'address': '789 Rue Galt Ouest, Sherbrooke, QC',
            'event_type': 'General',
            'organizer_id': users[0].id,
            'max_participants': 100,
            'registration_required': True,
            'registration_deadline': now + timedelta(days=25)
        }
    ]
    
    events = []
    for event_data in events_data:
        event = Event(**event_data)
        events.append(event)
        db.session.add(event)
    
    db.session.commit()
    print(f"[EVENTS] {len(events)} événements créés")
    
    # Inscrire des utilisateurs aux événements
    event_participations = [
        (users[0].id, events[0].id),
        (users[1].id, events[0].id),
        (users[2].id, events[0].id),
        (users[1].id, events[1].id),
        (users[2].id, events[2].id),
        (users[0].id, events[3].id),
        (users[1].id, events[3].id),
    ]
    
    for user_id, event_id in event_participations:
        participation = EventParticipant(user_id=user_id, event_id=event_id)
        db.session.add(participation)
    
    db.session.commit()
    print("[OK] Inscriptions aux événements créées")
    
    # Créer des annonces
    announcements_data = [
        {
            'title': 'Bienvenue sur notre nouvelle plateforme!',
            'content': 'Nous sommes heureux de vous présenter notre nouvelle plateforme communautaire. Vous pouvez maintenant gérer votre profil, rejoindre des départements, vous inscrire aux événements et bien plus encore! N\'hésitez pas à explorer toutes les fonctionnalités disponibles.',
            'announcement_type': 'General',
            'priority': 'High',
            'author_id': admin.id,
            'is_pinned': True
        },
        {
            'title': 'Répétition de la chorale',
            'content': 'Répétition générale pour la chorale ce jeudi à 19h30 dans le sanctuaire. Présence obligatoire pour tous les membres du département Louange. Nous préparerons les chants pour le culte de dimanche prochain.',
            'announcement_type': 'Department',
            'target_department_id': departments[0].id,
            'priority': 'Normal',
            'author_id': users[1].id
        },
        {
            'title': 'Collecte de nourriture',
            'content': 'Nous organisons une collecte de denrées non périssables pour les familles dans le besoin de notre communauté. Vous pouvez déposer vos dons dans les boîtes prévues à cet effet à l\'entrée du sanctuaire.',
            'announcement_type': 'General',
            'priority': 'Normal',
            'author_id': admin.id
        },
        {
            'title': 'Réunion Famille Espoir reportée',
            'content': 'La réunion de mercredi prochain est reportée au vendredi en raison d\'un conflit d\'horaire. Même heure, même lieu. Merci de votre compréhension.',
            'announcement_type': 'Family',
            'target_family_id': families[0].id,
            'priority': 'High',
            'author_id': users[1].id
        }
    ]
    
    for ann_data in announcements_data:
        announcement = Announcement(**ann_data)
        db.session.add(announcement)
    
    db.session.commit()
    print(f"[ANNOUNCE] {len(announcements_data)} annonces créées")
    
    # Créer des dons de démonstration
    donations_data = [
        {
            'user_id': users[0].id,
            'amount': Decimal('100.00'),
            'donation_type': 'Dîme',
            'payment_method': 'Stripe',
            'payment_status': 'Completed',
            'donation_date': now - timedelta(days=30),
            'processed_at': now - timedelta(days=30)
        },
        {
            'user_id': users[1].id,
            'amount': Decimal('50.00'),
            'donation_type': 'Offrande',
            'payment_method': 'Stripe',
            'payment_status': 'Completed',
            'donation_date': now - timedelta(days=15),
            'processed_at': now - timedelta(days=15)
        },
        {
            'user_id': users[2].id,
            'amount': Decimal('250.00'),
            'donation_type': 'Mission',
            'purpose': 'Soutien aux missions en Haïti',
            'payment_method': 'Stripe',
            'payment_status': 'Completed',
            'donation_date': now - timedelta(days=7),
            'processed_at': now - timedelta(days=7)
        }
    ]
    
    for don_data in donations_data:
        donation = Donation(**don_data)
        donation.generate_receipt_number()
        db.session.add(donation)
    
    db.session.commit()
    print(f"[DONATIONS] {len(donations_data)} dons de démonstration créés")
    
    print("\n[SUCCESS] Initialisation terminée avec succès!")
    print("\n[SUMMARY] Résumé:")
    print(f"   Utilisateurs: {User.query.count()}")
    print(f"   Départements: {Department.query.count()}")
    print(f"   Familles d'Impact: {FamilyImpact.query.count()}")
    print(f"   Événements: {Event.query.count()}")
    print(f"   Annonces: {Announcement.query.count()}")
    print(f"   Dons: {Donation.query.count()}")
    
    print("\n[ACCOUNTS] Comptes de connexion:")
    print("   Admin: admin@impactcentre.ca / admin123")
    print("   Jean Dupont: jean.dupont@email.com / password123")
    print("   Marie Martin: marie.martin@email.com / password123")
    print("   Pierre Gagnon: pierre.gagnon@email.com / password123")
    print("   Sophie Lavoie: sophie.lavoie@email.com / password123")
    
    print("\n[READY] L'application est prête à être utilisée!")

if __name__ == '__main__':
    app = create_app('development')
    with app.app_context():
        init_database()