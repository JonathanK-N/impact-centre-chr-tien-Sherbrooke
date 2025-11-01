from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from app import db
from app.models.department import Department, DepartmentMember
from app.models.user import User

departments_bp = Blueprint('departments', __name__)

@departments_bp.route('/')
@login_required
def list():
    departments = Department.query.filter_by(is_active=True).all()
    
    # Départements de l'utilisateur
    user_department_ids = [dm.department_id for dm in current_user.department_memberships if dm.is_active]
    
    return render_template('departments/list.html', 
                         departments=departments,
                         user_department_ids=user_department_ids)

@departments_bp.route('/<int:department_id>')
@login_required
def detail(department_id):
    department = Department.query.get_or_404(department_id)
    
    # Vérifier si l'utilisateur est membre ou responsable
    is_member = any(dm.department_id == department_id and dm.is_active 
                   for dm in current_user.department_memberships)
    is_responsible = department.responsible_id == current_user.id
    
    # Membres du département
    members = db.session.query(User).join(DepartmentMember).filter(
        DepartmentMember.department_id == department_id,
        DepartmentMember.is_active == True
    ).all()
    
    # Annonces du département
    announcements = department.announcements.filter_by(is_active=True).order_by(
        db.desc(department.announcements.property.mapper.class_.created_at)
    ).limit(5).all()
    
    return render_template('departments/detail.html',
                         department=department,
                         members=members,
                         announcements=announcements,
                         is_member=is_member,
                         is_responsible=is_responsible)

@departments_bp.route('/<int:department_id>/join', methods=['POST'])
@login_required
def join(department_id):
    department = Department.query.get_or_404(department_id)
    
    # Vérifier si déjà membre
    existing_membership = DepartmentMember.query.filter_by(
        user_id=current_user.id,
        department_id=department_id
    ).first()
    
    if existing_membership:
        if existing_membership.is_active:
            flash('Vous êtes déjà membre de ce département.', 'info')
        else:
            existing_membership.is_active = True
            db.session.commit()
            flash(f'Vous avez rejoint le département {department.name}!', 'success')
    else:
        membership = DepartmentMember(
            user_id=current_user.id,
            department_id=department_id
        )
        db.session.add(membership)
        db.session.commit()
        flash(f'Vous avez rejoint le département {department.name}!', 'success')
    
    return redirect(url_for('departments.detail', department_id=department_id))

@departments_bp.route('/<int:department_id>/leave', methods=['POST'])
@login_required
def leave(department_id):
    membership = DepartmentMember.query.filter_by(
        user_id=current_user.id,
        department_id=department_id,
        is_active=True
    ).first()
    
    if membership:
        membership.is_active = False
        db.session.commit()
        flash('Vous avez quitté le département.', 'info')
    
    return redirect(url_for('departments.list'))