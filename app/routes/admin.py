from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from functools import wraps
from app import db
from app.models.user import User
from app.models.department import Department, DepartmentMember
from app.models.family_impact import FamilyImpact, FamilyMember
from app.models.event import Event, EventParticipant
from app.models.announcement import Announcement
from app.models.donation import Donation

admin_bp = Blueprint('admin', __name__)

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_admin():
            flash('Accès refusé. Droits d\'administrateur requis.', 'error')
            return redirect(url_for('main.dashboard'))
        return f(*args, **kwargs)
    return decorated_function

@admin_bp.route('/')
@login_required
@admin_required
def dashboard():
    # Statistiques générales
    stats = {
        'total_users': User.query.filter_by(is_active=True).count(),
        'total_departments': Department.query.filter_by(is_active=True).count(),
        'total_families': FamilyImpact.query.filter_by(is_active=True).count(),
        'total_events': Event.query.filter_by(is_active=True).count(),
        'total_donations': Donation.query.filter_by(payment_status='Completed').count(),
        'total_amount_donated': db.session.query(db.func.sum(Donation.amount)).filter_by(
            payment_status='Completed'
        ).scalar() or 0
    }
    
    # Nouveaux membres (derniers 30 jours)
    from datetime import datetime, timedelta
    thirty_days_ago = datetime.utcnow() - timedelta(days=30)
    new_members = User.query.filter(
        User.created_at >= thirty_days_ago,
        User.is_active == True
    ).order_by(db.desc(User.created_at)).limit(10).all()
    
    # Événements à venir
    upcoming_events = Event.query.filter(
        Event.start_date >= datetime.utcnow(),
        Event.is_active == True
    ).order_by(Event.start_date).limit(5).all()
    
    # Dons récents
    recent_donations = Donation.query.filter_by(
        payment_status='Completed'
    ).order_by(db.desc(Donation.donation_date)).limit(10).all()
    
    return render_template('admin/dashboard.html',
                         stats=stats,
                         new_members=new_members,
                         upcoming_events=upcoming_events,
                         recent_donations=recent_donations)

@admin_bp.route('/users')
@login_required
@admin_required
def users():
    page = request.args.get('page', 1, type=int)
    search = request.args.get('search', '')
    role_filter = request.args.get('role', '')
    status_filter = request.args.get('status', '')
    
    query = User.query
    
    if search:
        query = query.filter(
            db.or_(
                User.first_name.contains(search),
                User.last_name.contains(search),
                User.email.contains(search)
            )
        )
    
    if role_filter:
        query = query.filter_by(role=role_filter)
    
    if status_filter:
        if status_filter == 'active':
            query = query.filter_by(is_active=True)
        elif status_filter == 'inactive':
            query = query.filter_by(is_active=False)
    
    users = query.order_by(User.last_name, User.first_name).paginate(
        page=page, per_page=20, error_out=False
    )
    
    return render_template('admin/users.html', users=users, 
                         search=search, role_filter=role_filter, status_filter=status_filter)

@admin_bp.route('/departments')
@login_required
@admin_required
def departments():
    departments = Department.query.order_by(Department.name).all()
    return render_template('admin/departments.html', departments=departments)

@admin_bp.route('/departments/create', methods=['GET', 'POST'])
@login_required
@admin_required
def create_department():
    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        responsible_id = request.form.get('responsible_id')
        
        department = Department(
            name=name,
            description=description,
            responsible_id=responsible_id if responsible_id else None
        )
        
        db.session.add(department)
        db.session.commit()
        
        flash(f'Département "{name}" créé avec succès!', 'success')
        return redirect(url_for('admin.departments'))
    
    # Utilisateurs pouvant être responsables
    potential_responsibles = User.query.filter_by(is_active=True).order_by(
        User.last_name, User.first_name
    ).all()
    
    return render_template('admin/create_department.html', 
                         potential_responsibles=potential_responsibles)

@admin_bp.route('/families')
@login_required
@admin_required
def families():
    families = FamilyImpact.query.order_by(FamilyImpact.name).all()
    return render_template('admin/families.html', families=families)

@admin_bp.route('/events')
@login_required
@admin_required
def events():
    events = Event.query.order_by(db.desc(Event.start_date)).all()
    return render_template('admin/events.html', events=events)

@admin_bp.route('/announcements')
@login_required
@admin_required
def announcements():
    announcements = Announcement.query.order_by(
        db.desc(Announcement.created_at)
    ).all()
    return render_template('admin/announcements.html', announcements=announcements)

@admin_bp.route('/announcements/create', methods=['GET', 'POST'])
@login_required
@admin_required
def create_announcement():
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        announcement_type = request.form.get('announcement_type')
        priority = request.form.get('priority')
        target_department_id = request.form.get('target_department_id')
        target_family_id = request.form.get('target_family_id')
        is_pinned = bool(request.form.get('is_pinned'))
        
        announcement = Announcement(
            title=title,
            content=content,
            announcement_type=announcement_type,
            priority=priority,
            target_department_id=target_department_id if target_department_id else None,
            target_family_id=target_family_id if target_family_id else None,
            author_id=current_user.id,
            is_pinned=is_pinned
        )
        
        db.session.add(announcement)
        db.session.commit()
        
        flash('Annonce créée avec succès!', 'success')
        return redirect(url_for('admin.announcements'))
    
    departments = Department.query.filter_by(is_active=True).all()
    families = FamilyImpact.query.filter_by(is_active=True).all()
    
    return render_template('admin/create_announcement.html',
                         departments=departments,
                         families=families)

@admin_bp.route('/donations')
@login_required
@admin_required
def donations():
    page = request.args.get('page', 1, type=int)
    donations = Donation.query.order_by(
        db.desc(Donation.donation_date)
    ).paginate(page=page, per_page=50, error_out=False)
    
    # Statistiques
    total_amount = db.session.query(db.func.sum(Donation.amount)).filter_by(
        payment_status='Completed'
    ).scalar() or 0
    
    return render_template('admin/donations.html', 
                         donations=donations, 
                         total_amount=total_amount)