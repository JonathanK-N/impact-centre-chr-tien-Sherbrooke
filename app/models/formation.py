from app import db
from datetime import datetime

class Formation(db.Model):
    __tablename__ = 'formations'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    category = db.Column(db.String(50), nullable=False)  # 'PCNC', 'BAPTEME', 'ATELIER'
    code = db.Column(db.String(20), unique=True)
    thumbnail_url = db.Column(db.String(500))
    banner_image = db.Column(db.String(500))  # Chemin vers l'image uploadée
    duration_total = db.Column(db.Integer)  # en minutes
    is_active = db.Column(db.Boolean, default=True)
    order_index = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relations
    modules = db.relationship('FormationModule', backref='formation', lazy=True, cascade='all, delete-orphan')
    user_progress = db.relationship('UserFormationProgress', backref='formation', lazy=True)

class FormationModule(db.Model):
    __tablename__ = 'formation_modules'
    
    id = db.Column(db.Integer, primary_key=True)
    formation_id = db.Column(db.Integer, db.ForeignKey('formations.id'), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    video_url = db.Column(db.String(500))
    zoom_url = db.Column(db.String(500))  # Lien de conférence Zoom
    video_id = db.Column(db.String(50))  # YouTube video ID
    thumbnail_url = db.Column(db.String(500))
    duration = db.Column(db.Integer)  # en minutes
    order_index = db.Column(db.Integer, default=0)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relations
    user_progress = db.relationship('UserModuleProgress', backref='module', lazy=True)

class UserFormationProgress(db.Model):
    __tablename__ = 'user_formation_progress'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    formation_id = db.Column(db.Integer, db.ForeignKey('formations.id'), nullable=False)
    status = db.Column(db.String(20), default='NOT_STARTED')  # NOT_STARTED, IN_PROGRESS, COMPLETED
    progress_percentage = db.Column(db.Integer, default=0)
    started_at = db.Column(db.DateTime)
    completed_at = db.Column(db.DateTime)
    certificate_url = db.Column(db.String(500))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Contrainte unique
    __table_args__ = (db.UniqueConstraint('user_id', 'formation_id'),)

class UserModuleProgress(db.Model):
    __tablename__ = 'user_module_progress'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    module_id = db.Column(db.Integer, db.ForeignKey('formation_modules.id'), nullable=False)
    status = db.Column(db.String(20), default='NOT_STARTED')  # NOT_STARTED, IN_PROGRESS, COMPLETED
    watch_time = db.Column(db.Integer, default=0)  # temps regardé en secondes
    completed_at = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Contrainte unique
    __table_args__ = (db.UniqueConstraint('user_id', 'module_id'),)