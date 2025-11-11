from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from sqlalchemy import desc
from app import db
from app.models.user import User
from app.models.department import Department, DepartmentMember
from app.models.family_impact import FamilyImpact, FamilyMember
from app.models.event import Event, EventParticipant
from app.models.announcement import Announcement
from app.models.donation import Donation

main_bp = Blueprint('main', __name__)

@main_bp.route('/health')
def health():
    return 'OK', 200

@main_bp.route('/api/notifications')
def notifications_api():
    """Retourne les notifications pertinentes pour le header."""
    if not current_user.is_authenticated:
        return jsonify({'notifications': [], 'unread': 0})
    
    try:
        user_departments = [dm.department_id for dm in current_user.department_memberships if dm.is_active]
        user_family = db.session.query(FamilyImpact).join(FamilyMember).filter(
            FamilyMember.user_id == current_user.id,
            FamilyMember.is_active == True
        ).first()
        user_family_id = user_family.id if user_family else None
        
        visibility_clauses = [Announcement.announcement_type == 'General']
        if user_departments:
            visibility_clauses.append(
                db.and_(
                    Announcement.announcement_type == 'Department',
                    Announcement.target_department_id.in_(user_departments)
                )
            )
        if user_family_id:
            visibility_clauses.append(
                db.and_(
                    Announcement.announcement_type == 'Family',
                    Announcement.target_family_id == user_family_id
                )
            )
        
        announcements = Announcement.query.filter(
            db.or_(*visibility_clauses),
            Announcement.is_active == True
        ).order_by(desc(Announcement.is_pinned), desc(Announcement.created_at)).limit(5).all()
        
        notification_items = [{
            'id': ann.id,
            'title': ann.title,
            'priority': ann.priority,
            'type': ann.announcement_type,
            'created_at': ann.created_at.isoformat(),
            'is_pinned': ann.is_pinned
        } for ann in announcements]
        
        unread = sum(1 for ann in notification_items if ann['priority'] in ('High', 'Urgent'))
    except Exception:
        notification_items = []
        unread = 0
    
    return jsonify({'notifications': notification_items, 'unread': unread})

@main_bp.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    
    # Statistiques par défaut
    stats = {
        'members': 0,
        'departments': 0,
        'families': 0,
        'events': 0
    }
    
    try:
        stats = {
            'members': User.query.filter_by(is_active=True).count(),
            'departments': Department.query.filter_by(is_active=True).count(),
            'families': FamilyImpact.query.filter_by(is_active=True).count(),
            'events': Event.query.filter_by(is_active=True).count()
        }
        public_announcements = Announcement.query.filter_by(
            announcement_type='General',
            is_active=True
        ).order_by(desc(Announcement.created_at)).limit(3).all()
    except:
        public_announcements = []
    
    return render_template('main/index.html', stats=stats, announcements=public_announcements)

@main_bp.route('/dashboard')
@login_required
def dashboard():
    # Mes départements
    user_departments = db.session.query(Department).join(DepartmentMember).filter(
        DepartmentMember.user_id == current_user.id,
        DepartmentMember.is_active == True
    ).all()
    
    # Ma famille d'impact
    user_family = db.session.query(FamilyImpact).join(FamilyMember).filter(
        FamilyMember.user_id == current_user.id,
        FamilyMember.is_active == True
    ).first()
    
    # Mes événements à venir
    upcoming_events = db.session.query(Event).join(EventParticipant).filter(
        EventParticipant.user_id == current_user.id,
        EventParticipant.status == 'Confirmed',
        Event.start_date >= db.func.current_timestamp()
    ).order_by(Event.start_date).limit(5).all()
    
    # Annonces pertinentes
    announcements = Announcement.query.filter(
        db.or_(
            Announcement.announcement_type == 'General',
            db.and_(
                Announcement.announcement_type == 'Department',
                Announcement.target_department_id.in_([d.id for d in user_departments])
            ),
            db.and_(
                Announcement.announcement_type == 'Family',
                Announcement.target_family_id == (user_family.id if user_family else None)
            )
        ),
        Announcement.is_active == True
    ).order_by(desc(Announcement.is_pinned), desc(Announcement.created_at)).limit(5).all()
    
    # Statistiques personnelles
    user_stats = {
        'departments': len(user_departments),
        'family': 1 if user_family else 0,
        'events': len(upcoming_events),
        'donations': Donation.query.filter_by(
            user_id=current_user.id,
            payment_status='Completed'
        ).count()
    }
    
    return render_template('main/dashboard.html',
                         user_departments=user_departments,
                         user_family=user_family,
                         upcoming_events=upcoming_events,
                         announcements=announcements,
                         user_stats=user_stats)

@main_bp.route('/profile')
@login_required
def profile():
    return render_template('main/profile.html', user=current_user)

@main_bp.route('/profile/edit', methods=['GET', 'POST'])
@login_required
def edit_profile():
    if request.method == 'POST':
        current_user.first_name = request.form.get('first_name')
        current_user.last_name = request.form.get('last_name')
        current_user.phone = request.form.get('phone')
        current_user.address = request.form.get('address')
        current_user.gender = request.form.get('gender')
        current_user.marital_status = request.form.get('marital_status')
        current_user.church_role = request.form.get('church_role')
        
        # Conversion de la date de naissance
        birth_date = request.form.get('birth_date')
        if birth_date:
            from datetime import datetime
            current_user.birth_date = datetime.strptime(birth_date, '%Y-%m-%d').date()
        
        db.session.commit()
        flash('Profil mis à jour avec succès!', 'success')
        return redirect(url_for('main.profile'))
    
    return render_template('main/edit_profile.html', user=current_user)

@main_bp.route('/formations')
def formations():
    pcnc_modules = [
        {
            'code': 'PCNC-001',
            'title': 'Découvrir la vision ICC',
            'duration': '12 min',
            'badge': 'Fondation',
            'video_id': 'dQw4w9WgXcQ'
        },
        {
            'code': 'PCNC-101',
            'title': 'Identité en Christ',
            'duration': '18 min',
            'badge': 'Croissance',
            'video_id': 'kXYiU_JCYtU'
        },
        {
            'code': 'PCNC-201',
            'title': 'Leadership serviteur',
            'duration': '22 min',
            'badge': 'Leadership',
            'video_id': '3JZ_D3ELwOQ'
        },
        {
            'code': 'PCNC-RTT',
            'title': 'Retour aux fondements',
            'duration': '15 min',
            'badge': 'Retraite',
            'video_id': 'YQHsXMglC9A'
        },
    ]
    
    tracks = {
        'bapteme': {
            'title': 'Parcours Baptême',
            'description': 'Préparez-vous au baptême d’eau grâce à des capsules simples et des fiches pratiques.',
            'items': [
                'Session 1 · Pourquoi le baptême chrétien ?',
                'Session 2 · Engagement et témoignage',
                'Session 3 · Atelier questions/réponses'
            ]
        },
        'ateliers': {
            'title': 'Ateliers pratiques',
            'description': 'Capsules vidéo animées par les équipes ICC (communication, accueil, louange…).',
            'items': [
                'Atelier Accueil & Hospitalité',
                'Atelier Communication & PC',
                'Atelier Louange & Technique'
            ]
        }
    }
    
    return render_template('main/formations.html',
                           pcnc_modules=pcnc_modules,
                           tracks=tracks)
