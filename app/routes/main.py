from flask import Blueprint, render_template, request, redirect, url_for, flash
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