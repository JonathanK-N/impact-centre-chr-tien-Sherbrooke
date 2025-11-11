from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from sqlalchemy import desc
from app import db
from app.models.formation import Formation, FormationModule, UserFormationProgress, UserModuleProgress
from datetime import datetime

formations_bp = Blueprint('formations', __name__, url_prefix='/formations')

@formations_bp.route('/')
def index():
    """Page principale des formations"""
    # Formations PCNC
    pcnc_formations = Formation.query.filter_by(
        category='PCNC', 
        is_active=True
    ).order_by(Formation.order_index).all()
    
    # Formation Baptême
    bapteme_formation = Formation.query.filter_by(
        category='BAPTEME', 
        is_active=True
    ).first()
    
    # Ateliers
    ateliers = Formation.query.filter_by(
        category='ATELIER', 
        is_active=True
    ).order_by(Formation.order_index).all()
    
    # Progression de l'utilisateur si connecté
    user_progress = {}
    if current_user.is_authenticated:
        progress_records = UserFormationProgress.query.filter_by(
            user_id=current_user.id
        ).all()
        user_progress = {p.formation_id: p for p in progress_records}
    
    return render_template('formations/index.html',
                         pcnc_formations=pcnc_formations,
                         bapteme_formation=bapteme_formation,
                         ateliers=ateliers,
                         user_progress=user_progress)

@formations_bp.route('/<int:formation_id>')
def detail(formation_id):
    """Page détail d'une formation avec ses modules"""
    formation = Formation.query.get_or_404(formation_id)
    modules = FormationModule.query.filter_by(
        formation_id=formation_id,
        is_active=True
    ).order_by(FormationModule.order_index).all()
    
    # Progression de l'utilisateur
    user_progress = None
    module_progress = {}
    if current_user.is_authenticated:
        user_progress = UserFormationProgress.query.filter_by(
            user_id=current_user.id,
            formation_id=formation_id
        ).first()
        
        module_records = UserModuleProgress.query.filter_by(
            user_id=current_user.id
        ).filter(
            UserModuleProgress.module_id.in_([m.id for m in modules])
        ).all()
        module_progress = {p.module_id: p for p in module_records}
    
    return render_template('formations/detail.html',
                         formation=formation,
                         modules=modules,
                         user_progress=user_progress,
                         module_progress=module_progress)

@formations_bp.route('/<int:formation_id>/module/<int:module_id>')
def watch_module(formation_id, module_id):
    """Page de visionnage d'un module"""
    formation = Formation.query.get_or_404(formation_id)
    module = FormationModule.query.get_or_404(module_id)
    
    # Vérifier que le module appartient à la formation
    if module.formation_id != formation_id:
        flash('Module non trouvé dans cette formation.', 'error')
        return redirect(url_for('formations.detail', formation_id=formation_id))
    
    # Marquer comme commencé si utilisateur connecté
    if current_user.is_authenticated:
        # Progression de la formation
        formation_progress = UserFormationProgress.query.filter_by(
            user_id=current_user.id,
            formation_id=formation_id
        ).first()
        
        if not formation_progress:
            formation_progress = UserFormationProgress(
                user_id=current_user.id,
                formation_id=formation_id,
                status='IN_PROGRESS',
                started_at=datetime.utcnow()
            )
            db.session.add(formation_progress)
        
        # Progression du module
        module_progress = UserModuleProgress.query.filter_by(
            user_id=current_user.id,
            module_id=module_id
        ).first()
        
        if not module_progress:
            module_progress = UserModuleProgress(
                user_id=current_user.id,
                module_id=module_id,
                status='IN_PROGRESS'
            )
            db.session.add(module_progress)
        
        db.session.commit()
    
    # Autres modules de la formation
    other_modules = FormationModule.query.filter_by(
        formation_id=formation_id,
        is_active=True
    ).order_by(FormationModule.order_index).all()
    
    return render_template('formations/watch.html',
                         formation=formation,
                         module=module,
                         other_modules=other_modules)

@formations_bp.route('/api/module/<int:module_id>/complete', methods=['POST'])
@login_required
def complete_module(module_id):
    """Marquer un module comme terminé"""
    module = FormationModule.query.get_or_404(module_id)
    
    # Mettre à jour la progression du module
    module_progress = UserModuleProgress.query.filter_by(
        user_id=current_user.id,
        module_id=module_id
    ).first()
    
    if not module_progress:
        module_progress = UserModuleProgress(
            user_id=current_user.id,
            module_id=module_id
        )
        db.session.add(module_progress)
    
    module_progress.status = 'COMPLETED'
    module_progress.completed_at = datetime.utcnow()
    
    # Vérifier si toute la formation est terminée
    formation = module.formation
    all_modules = FormationModule.query.filter_by(
        formation_id=formation.id,
        is_active=True
    ).all()
    
    completed_modules = UserModuleProgress.query.filter_by(
        user_id=current_user.id,
        status='COMPLETED'
    ).filter(
        UserModuleProgress.module_id.in_([m.id for m in all_modules])
    ).count()
    
    # Mettre à jour la progression de la formation
    formation_progress = UserFormationProgress.query.filter_by(
        user_id=current_user.id,
        formation_id=formation.id
    ).first()
    
    if not formation_progress:
        formation_progress = UserFormationProgress(
            user_id=current_user.id,
            formation_id=formation.id,
            started_at=datetime.utcnow()
        )
        db.session.add(formation_progress)
    
    progress_percentage = int((completed_modules / len(all_modules)) * 100)
    formation_progress.progress_percentage = progress_percentage
    
    if completed_modules == len(all_modules):
        formation_progress.status = 'COMPLETED'
        formation_progress.completed_at = datetime.utcnow()
        # TODO: Générer le certificat
    else:
        formation_progress.status = 'IN_PROGRESS'
    
    db.session.commit()
    
    return jsonify({
        'success': True,
        'module_completed': True,
        'formation_progress': progress_percentage,
        'formation_completed': formation_progress.status == 'COMPLETED'
    })

@formations_bp.route('/api/module/<int:module_id>/progress', methods=['POST'])
@login_required
def update_progress(module_id):
    """Mettre à jour le temps de visionnage"""
    data = request.get_json()
    watch_time = data.get('watch_time', 0)
    
    module_progress = UserModuleProgress.query.filter_by(
        user_id=current_user.id,
        module_id=module_id
    ).first()
    
    if not module_progress:
        module_progress = UserModuleProgress(
            user_id=current_user.id,
            module_id=module_id
        )
        db.session.add(module_progress)
    
    module_progress.watch_time = max(module_progress.watch_time, watch_time)
    module_progress.status = 'IN_PROGRESS'
    db.session.commit()
    
    return jsonify({'success': True})