from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from datetime import datetime
from app import db
from app.models.event import Event, EventParticipant
from app.models.department import DepartmentMember
from app.models.family_impact import FamilyMember

events_bp = Blueprint('events', __name__)

@events_bp.route('/')
@login_required
def list():
    # Événements à venir
    upcoming_events = Event.query.filter(
        Event.start_date >= datetime.utcnow(),
        Event.is_active == True,
        Event.is_cancelled == False
    ).order_by(Event.start_date).all()
    
    # Filtrer les événements selon les permissions
    visible_events = []
    user_department_ids = [dm.department_id for dm in current_user.department_memberships if dm.is_active]
    user_family = db.session.query(FamilyMember).filter_by(
        user_id=current_user.id,
        is_active=True
    ).first()
    user_family_id = user_family.family_id if user_family else None
    
    for event in upcoming_events:
        if (event.event_type == 'General' or
            (event.event_type == 'Department' and event.target_department_id in user_department_ids) or
            (event.event_type == 'Family' and event.target_family_id == user_family_id)):
            visible_events.append(event)
    
    # Mes inscriptions
    user_event_ids = [ep.event_id for ep in current_user.event_participations 
                     if ep.status == 'Confirmed']
    
    return render_template('events/list.html', 
                         events=visible_events,
                         user_event_ids=user_event_ids)

@events_bp.route('/<int:event_id>')
@login_required
def detail(event_id):
    event = Event.query.get_or_404(event_id)
    
    # Vérifier les permissions de visualisation
    user_department_ids = [dm.department_id for dm in current_user.department_memberships if dm.is_active]
    user_family = db.session.query(FamilyMember).filter_by(
        user_id=current_user.id,
        is_active=True
    ).first()
    user_family_id = user_family.family_id if user_family else None
    
    can_view = (event.event_type == 'General' or
                (event.event_type == 'Department' and event.target_department_id in user_department_ids) or
                (event.event_type == 'Family' and event.target_family_id == user_family_id))
    
    if not can_view:
        flash('Vous n\'avez pas accès à cet événement.', 'error')
        return redirect(url_for('events.list'))
    
    # Vérifier si l'utilisateur est inscrit
    user_participation = EventParticipant.query.filter_by(
        user_id=current_user.id,
        event_id=event_id
    ).first()
    
    # Participants (si l'utilisateur peut les voir)
    participants = []
    if (current_user.is_admin() or 
        event.organizer_id == current_user.id or
        user_participation):
        participants = db.session.query(User).join(EventParticipant).filter(
            EventParticipant.event_id == event_id,
            EventParticipant.status == 'Confirmed'
        ).all()
    
    return render_template('events/detail.html',
                         event=event,
                         user_participation=user_participation,
                         participants=participants)

@events_bp.route('/<int:event_id>/register', methods=['POST'])
@login_required
def register(event_id):
    event = Event.query.get_or_404(event_id)
    
    # Vérifications
    if event.is_cancelled:
        flash('Cet événement a été annulé.', 'error')
        return redirect(url_for('events.detail', event_id=event_id))
    
    if event.registration_deadline and datetime.utcnow() > event.registration_deadline:
        flash('La période d\'inscription est terminée.', 'error')
        return redirect(url_for('events.detail', event_id=event_id))
    
    if event.is_full:
        flash('Cet événement est complet.', 'error')
        return redirect(url_for('events.detail', event_id=event_id))
    
    # Vérifier si déjà inscrit
    existing_participation = EventParticipant.query.filter_by(
        user_id=current_user.id,
        event_id=event_id
    ).first()
    
    if existing_participation:
        if existing_participation.status == 'Confirmed':
            flash('Vous êtes déjà inscrit à cet événement.', 'info')
        else:
            existing_participation.status = 'Confirmed'
            db.session.commit()
            flash('Votre inscription a été confirmée!', 'success')
    else:
        participation = EventParticipant(
            user_id=current_user.id,
            event_id=event_id,
            status='Confirmed'
        )
        db.session.add(participation)
        db.session.commit()
        flash('Inscription réussie!', 'success')
    
    return redirect(url_for('events.detail', event_id=event_id))

@events_bp.route('/<int:event_id>/unregister', methods=['POST'])
@login_required
def unregister(event_id):
    participation = EventParticipant.query.filter_by(
        user_id=current_user.id,
        event_id=event_id
    ).first()
    
    if participation:
        participation.status = 'Cancelled'
        db.session.commit()
        flash('Votre inscription a été annulée.', 'info')
    
    return redirect(url_for('events.detail', event_id=event_id))

@events_bp.route('/calendar')
@login_required
def calendar():
    # Tous les événements visibles pour l'utilisateur
    user_department_ids = [dm.department_id for dm in current_user.department_memberships if dm.is_active]
    user_family = db.session.query(FamilyMember).filter_by(
        user_id=current_user.id,
        is_active=True
    ).first()
    user_family_id = user_family.family_id if user_family else None
    
    events = Event.query.filter(
        Event.is_active == True,
        Event.is_cancelled == False,
        db.or_(
            Event.event_type == 'General',
            db.and_(Event.event_type == 'Department', Event.target_department_id.in_(user_department_ids)),
            db.and_(Event.event_type == 'Family', Event.target_family_id == user_family_id)
        )
    ).all()
    
    # Préparer les données pour le calendrier
    events_data = []
    for event in events:
        events_data.append({
            'id': event.id,
            'title': event.title,
            'start': event.start_date.isoformat(),
            'end': event.end_date.isoformat() if event.end_date else None,
            'url': url_for('events.detail', event_id=event.id),
            'color': '#0d6efd' if event.event_type == 'General' else '#198754'
        })
    
    return render_template('events/calendar.html', events_data=events_data)