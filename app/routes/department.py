from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app import db
from app.models.department import Department
from app.models.announcement import Announcement
from app.models.event import Event
from app.models.user import User

department_bp = Blueprint('department', __name__)

@department_bp.route('/manage')
@login_required
def manage():
    # Vérifier si l'utilisateur est responsable d'un département
    department = Department.query.filter_by(responsible_id=current_user.id, is_active=True).first()
    
    if not department:
        flash('Vous n\'êtes responsable d\'aucun département.', 'error')
        return redirect(url_for('main.dashboard'))
    
    # Statistiques du département
    stats = {
        'total_members': department.members.filter_by(is_active=True).count(),
        'total_announcements': department.announcements.filter_by(is_active=True).count(),
        'total_events': department.events.filter_by(is_active=True).count()
    }
    
    # Annonces récentes
    recent_announcements = department.announcements.filter_by(is_active=True).order_by(
        db.desc(Announcement.created_at)
    ).limit(5).all()
    
    # Événements à venir
    from datetime import datetime
    upcoming_events = department.events.filter(
        Event.start_date >= datetime.utcnow(),
        Event.is_active == True
    ).order_by(Event.start_date).limit(5).all()
    
    return render_template('department/manage.html',
                         department=department,
                         stats=stats,
                         recent_announcements=recent_announcements,
                         upcoming_events=upcoming_events)

@department_bp.route('/announcements')
@login_required
def announcements():
    department = Department.query.filter_by(responsible_id=current_user.id, is_active=True).first()
    
    if not department:
        flash('Accès non autorisé.', 'error')
        return redirect(url_for('main.dashboard'))
    
    announcements = department.announcements.order_by(db.desc(Announcement.created_at)).all()
    return render_template('department/announcements.html', 
                         department=department, 
                         announcements=announcements)

@department_bp.route('/announcements/create', methods=['GET', 'POST'])
@login_required
def create_announcement():
    department = Department.query.filter_by(responsible_id=current_user.id, is_active=True).first()
    
    if not department:
        flash('Accès non autorisé.', 'error')
        return redirect(url_for('main.dashboard'))
    
    if request.method == 'POST':
        announcement = Announcement(
            title=request.form['title'],
            content=request.form['content'],
            announcement_type='Department',
            priority=request.form['priority'],
            target_department_id=department.id,
            author_id=current_user.id,
            is_pinned=bool(request.form.get('is_pinned'))
        )
        
        db.session.add(announcement)
        db.session.commit()
        
        flash('Annonce créée avec succès!', 'success')
        return redirect(url_for('department.announcements'))
    
    return render_template('department/create_announcement.html', department=department)

@department_bp.route('/events')
@login_required
def events():
    department = Department.query.filter_by(responsible_id=current_user.id, is_active=True).first()
    
    if not department:
        flash('Accès non autorisé.', 'error')
        return redirect(url_for('main.dashboard'))
    
    events = department.events.order_by(db.desc(Event.start_date)).all()
    return render_template('department/events.html', 
                         department=department, 
                         events=events)

@department_bp.route('/events/create', methods=['GET', 'POST'])
@login_required
def create_event():
    department = Department.query.filter_by(responsible_id=current_user.id, is_active=True).first()
    
    if not department:
        flash('Accès non autorisé.', 'error')
        return redirect(url_for('main.dashboard'))
    
    if request.method == 'POST':
        from datetime import datetime
        
        event = Event(
            title=request.form['title'],
            description=request.form['description'],
            location=request.form['location'],
            start_date=datetime.fromisoformat(request.form['start_date']),
            end_date=datetime.fromisoformat(request.form['end_date']) if request.form['end_date'] else None,
            capacity=int(request.form['capacity']) if request.form['capacity'] else None,
            event_type='Department',
            target_department_id=department.id,
            created_by_id=current_user.id
        )
        
        db.session.add(event)
        db.session.commit()
        
        flash('Événement créé avec succès!', 'success')
        return redirect(url_for('department.events'))
    
    return render_template('department/create_event.html', department=department)

@department_bp.route('/members')
@login_required
def members():
    department = Department.query.filter_by(responsible_id=current_user.id, is_active=True).first()
    
    if not department:
        flash('Accès non autorisé.', 'error')
        return redirect(url_for('main.dashboard'))
    
    members = department.members.filter_by(is_active=True).all()
    return render_template('department/members.html', 
                         department=department, 
                         members=members)