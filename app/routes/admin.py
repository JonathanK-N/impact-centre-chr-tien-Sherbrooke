from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from functools import wraps
from werkzeug.utils import secure_filename
import os
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

@admin_bp.route('/families/create', methods=['GET', 'POST'])
@login_required
@admin_required
def create_family():
    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        meeting_day = request.form.get('meeting_day')
        meeting_time = request.form.get('meeting_time')
        address = request.form.get('address')
        city = request.form.get('city')
        postal_code = request.form.get('postal_code')
        capacity = request.form.get('capacity')
        responsible_id = request.form.get('responsible_id')
        
        family = FamilyImpact(
            name=name,
            description=description,
            meeting_day=meeting_day,
            meeting_time=meeting_time,
            address=address,
            city=city,
            postal_code=postal_code,
            capacity=int(capacity) if capacity else None,
            responsible_id=responsible_id if responsible_id else None
        )
        
        db.session.add(family)
        db.session.commit()
        
        flash(f'Famille d\'Impact "{name}" créée avec succès!', 'success')
        return redirect(url_for('admin.families'))
    
    # Utilisateurs pouvant être responsables
    potential_responsibles = User.query.filter_by(is_active=True).order_by(
        User.last_name, User.first_name
    ).all()
    
    return render_template('admin/create_family.html', 
                         potential_responsibles=potential_responsibles)

@admin_bp.route('/events')
@login_required
@admin_required
def events():
    events = Event.query.order_by(db.desc(Event.start_date)).all()
    return render_template('admin/events.html', events=events)

@admin_bp.route('/events/create', methods=['GET', 'POST'])
@login_required
@admin_required
def create_event():
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        location = request.form.get('location')
        start_date = request.form.get('start_date')
        end_date = request.form.get('end_date')
        capacity = request.form.get('capacity')
        event_type = request.form.get('event_type')
        target_department_id = request.form.get('target_department_id')
        target_family_id = request.form.get('target_family_id')
        
        from datetime import datetime
        event = Event(
            title=title,
            description=description,
            location=location,
            start_date=datetime.fromisoformat(start_date),
            end_date=datetime.fromisoformat(end_date) if end_date else None,
            capacity=int(capacity) if capacity else None,
            event_type=event_type,
            target_department_id=target_department_id if target_department_id else None,
            target_family_id=target_family_id if target_family_id else None,
            created_by_id=current_user.id
        )
        
        db.session.add(event)
        db.session.commit()
        
        flash(f'Événement "{title}" créé avec succès!', 'success')
        return redirect(url_for('admin.events'))
    
    departments = Department.query.filter_by(is_active=True).all()
    families = FamilyImpact.query.filter_by(is_active=True).all()
    
    return render_template('admin/create_event.html',
                         departments=departments,
                         families=families)

@admin_bp.route('/media')
@login_required
@admin_required
def media():
    from app.models.media import MediaResource
    media_items = MediaResource.query.order_by(db.desc(MediaResource.created_at)).all()
    return render_template('admin/media.html', media_items=media_items)

@admin_bp.route('/media/create', methods=['GET', 'POST'])
@login_required
@admin_required
def create_media():
    if request.method == 'POST':
        from app.models.media import MediaResource
        
        title = request.form.get('title')
        description = request.form.get('description')
        media_type = request.form.get('media_type')
        url = request.form.get('url')
        thumbnail_url = request.form.get('thumbnail_url')
        
        media = MediaResource(
            title=title,
            description=description,
            media_type=media_type,
            url=url,
            thumbnail_url=thumbnail_url,
            author_id=current_user.id
        )
        
        db.session.add(media)
        db.session.commit()
        
        flash(f'Média "{title}" ajouté avec succès!', 'success')
        return redirect(url_for('admin.media'))
    
    return render_template('admin/create_media.html')

@admin_bp.route('/formations')
@login_required
@admin_required
def formations():
    from app.models.formation import Formation
    formations = Formation.query.order_by(Formation.category, Formation.order_index).all()
    return render_template('admin/formations.html', formations=formations)

@admin_bp.route('/formations/create', methods=['GET', 'POST'])
@login_required
@admin_required
def create_formation():
    if request.method == 'POST':
        from app.models.formation import Formation
        
        title = request.form.get('title')
        description = request.form.get('description')
        category = request.form.get('category')
        code = request.form.get('code')
        thumbnail_url = request.form.get('thumbnail_url')
        duration_total = request.form.get('duration_total')
        
        formation = Formation(
            title=title,
            description=description,
            category=category,
            code=code,
            thumbnail_url=thumbnail_url,
            duration_total=int(duration_total) if duration_total else None
        )
        
        db.session.add(formation)
        db.session.commit()
        
        flash(f'Formation "{title}" créée avec succès!', 'success')
        return redirect(url_for('admin.formations'))
    
    return render_template('admin/create_formation.html')

@admin_bp.route('/formations/<int:formation_id>/edit', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_formation(formation_id):
    from app.models.formation import Formation, FormationModule
    formation = Formation.query.get_or_404(formation_id)
    
    if request.method == 'POST':
        formation.title = request.form.get('title')
        formation.description = request.form.get('description')
        formation.category = request.form.get('category')
        formation.code = request.form.get('code')
        formation.thumbnail_url = request.form.get('thumbnail_url')
        formation.duration_total = int(request.form.get('duration_total')) if request.form.get('duration_total') else None
        
        # Gestion de l'upload de bannière
        if 'banner_image' in request.files:
            file = request.files['banner_image']
            if file and file.filename:
                filename = secure_filename(file.filename)
                upload_path = os.path.join('app/static/uploads/formations', filename)
                os.makedirs(os.path.dirname(upload_path), exist_ok=True)
                file.save(upload_path)
                formation.banner_image = f'/static/uploads/formations/{filename}'
        
        db.session.commit()
        flash('Formation mise à jour avec succès!', 'success')
        return redirect(url_for('admin.formations'))
    
    modules = FormationModule.query.filter_by(formation_id=formation_id).order_by(FormationModule.order_index).all()
    return render_template('admin/edit_formation.html', formation=formation, modules=modules)

@admin_bp.route('/formations/<int:formation_id>/modules/create', methods=['GET', 'POST'])
@login_required
@admin_required
def create_module(formation_id):
    from app.models.formation import Formation, FormationModule
    formation = Formation.query.get_or_404(formation_id)
    
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        video_url = request.form.get('video_url')
        zoom_url = request.form.get('zoom_url')
        video_id = request.form.get('video_id')
        duration = request.form.get('duration')
        order_index = request.form.get('order_index')
        
        module = FormationModule(
            formation_id=formation_id,
            title=title,
            description=description,
            video_url=video_url,
            zoom_url=zoom_url,
            video_id=video_id,
            duration=int(duration) if duration else None,
            order_index=int(order_index) if order_index else 0,
            thumbnail_url=f'https://img.youtube.com/vi/{video_id}/mqdefault.jpg' if video_id else None
        )
        
        db.session.add(module)
        db.session.commit()
        
        flash('Module ajouté avec succès!', 'success')
        return redirect(url_for('admin.edit_formation', formation_id=formation_id))
    
    return render_template('admin/create_module.html', formation=formation)

@admin_bp.route('/modules/<int:module_id>/edit', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_module(module_id):
    from app.models.formation import FormationModule
    module = FormationModule.query.get_or_404(module_id)
    
    if request.method == 'POST':
        module.title = request.form.get('title')
        module.description = request.form.get('description')
        module.video_url = request.form.get('video_url')
        module.zoom_url = request.form.get('zoom_url')
        module.video_id = request.form.get('video_id')
        module.duration = int(request.form.get('duration')) if request.form.get('duration') else None
        module.order_index = int(request.form.get('order_index')) if request.form.get('order_index') else 0
        
        if module.video_id:
            module.thumbnail_url = f'https://img.youtube.com/vi/{module.video_id}/mqdefault.jpg'
        
        db.session.commit()
        flash('Module mis à jour avec succès!', 'success')
        return redirect(url_for('admin.edit_formation', formation_id=module.formation_id))
    
    return render_template('admin/edit_module.html', module=module)

@admin_bp.route('/media/<int:media_id>/edit', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_media(media_id):
    from app.models.media import MediaResource
    media = MediaResource.query.get_or_404(media_id)
    
    if request.method == 'POST':
        media.title = request.form.get('title')
        media.description = request.form.get('description')
        media.media_type = request.form.get('media_type')
        media.url = request.form.get('url')
        media.thumbnail_url = request.form.get('thumbnail_url')
        
        db.session.commit()
        flash('Média mis à jour avec succès!', 'success')
        return redirect(url_for('admin.media'))
    
    return render_template('admin/edit_media.html', media=media)

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