from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from app import db
from app.models.family_impact import FamilyImpact, FamilyMember
from app.models.user import User

families_bp = Blueprint('families', __name__)

@families_bp.route('/')
@login_required
def list():
    families = FamilyImpact.query.filter_by(is_active=True).all()
    
    # Famille de l'utilisateur
    user_family = db.session.query(FamilyImpact).join(FamilyMember).filter(
        FamilyMember.user_id == current_user.id,
        FamilyMember.is_active == True
    ).first()
    
    return render_template('families/list.html', 
                         families=families,
                         user_family=user_family)

@families_bp.route('/<int:family_id>')
@login_required
def detail(family_id):
    family = FamilyImpact.query.get_or_404(family_id)
    
    # Vérifier si l'utilisateur est membre ou responsable
    is_member = any(fm.family_id == family_id and fm.is_active 
                   for fm in current_user.family_memberships)
    is_responsible = family.responsible_id == current_user.id
    
    # Membres de la famille
    members = db.session.query(User).join(FamilyMember).filter(
        FamilyMember.family_id == family_id,
        FamilyMember.is_active == True
    ).all()
    
    # Annonces de la famille
    announcements = family.announcements.filter_by(is_active=True).order_by(
        db.desc(family.announcements.property.mapper.class_.created_at)
    ).limit(5).all()
    
    return render_template('families/detail.html',
                         family=family,
                         members=members,
                         announcements=announcements,
                         is_member=is_member,
                         is_responsible=is_responsible)

@families_bp.route('/<int:family_id>/join', methods=['POST'])
@login_required
def join(family_id):
    family = FamilyImpact.query.get_or_404(family_id)
    
    # Vérifier si l'utilisateur est déjà dans une famille
    current_family = db.session.query(FamilyMember).filter_by(
        user_id=current_user.id,
        is_active=True
    ).first()
    
    if current_family:
        flash('Vous êtes déjà membre d\'une Famille d\'Impact. Vous ne pouvez appartenir qu\'à une seule famille à la fois.', 'error')
        return redirect(url_for('families.detail', family_id=family_id))
    
    # Vérifier la capacité
    if family.current_members_count >= family.max_capacity:
        flash('Cette Famille d\'Impact est complète.', 'error')
        return redirect(url_for('families.detail', family_id=family_id))
    
    # Créer la demande d'adhésion
    membership = FamilyMember(
        user_id=current_user.id,
        family_id=family_id,
        status='Pending'
    )
    db.session.add(membership)
    db.session.commit()
    
    flash('Votre demande d\'adhésion a été envoyée au responsable de la famille.', 'info')
    return redirect(url_for('families.detail', family_id=family_id))

@families_bp.route('/<int:family_id>/leave', methods=['POST'])
@login_required
def leave(family_id):
    membership = FamilyMember.query.filter_by(
        user_id=current_user.id,
        family_id=family_id,
        is_active=True
    ).first()
    
    if membership:
        membership.is_active = False
        db.session.commit()
        flash('Vous avez quitté la Famille d\'Impact.', 'info')
    
    return redirect(url_for('families.list'))

@families_bp.route('/map')
@login_required
def map():
    families = FamilyImpact.query.filter_by(is_active=True).all()
    
    # Préparer les données pour la carte
    families_data = []
    for family in families:
        if family.latitude and family.longitude:
            families_data.append({
                'id': family.id,
                'name': family.name,
                'address': family.address,
                'latitude': family.latitude,
                'longitude': family.longitude,
                'responsible': family.responsible.full_name if family.responsible else 'Non assigné',
                'members_count': family.current_members_count,
                'max_capacity': family.max_capacity,
                'available_spots': family.available_spots,
                'meeting_day': family.meeting_day,
                'meeting_time': family.meeting_time.strftime('%H:%M') if family.meeting_time else None
            })
    
    return render_template('families/map.html', families_data=families_data)