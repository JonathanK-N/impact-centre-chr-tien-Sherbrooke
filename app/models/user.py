from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    
    # Informations personnelles
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    phone = db.Column(db.String(20))
    address = db.Column(db.Text)
    birth_date = db.Column(db.Date)
    gender = db.Column(db.String(10))  # 'M', 'F', 'Autre'
    marital_status = db.Column(db.String(20))  # 'Célibataire', 'Marié(e)', 'Divorcé(e)', 'Veuf/Veuve'
    
    # Statut dans l'église
    membership_status = db.Column(db.String(20), default='Nouveau')  # 'Nouveau', 'En formation', 'Baptisé', 'Membre officiel'
    church_role = db.Column(db.String(100))  # 'Choriste', 'Intercesseur', etc.
    
    # Rôles système
    role = db.Column(db.String(20), default='Membre')  # 'Admin', 'Responsable Département', 'Responsable Famille', 'Membre'
    is_active = db.Column(db.Boolean, default=True)
    
    # Métadonnées
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relations
    department_memberships = db.relationship('DepartmentMember', back_populates='user', cascade='all, delete-orphan')
    family_memberships = db.relationship('FamilyMember', back_populates='user', cascade='all, delete-orphan')
    event_participations = db.relationship('EventParticipant', back_populates='user', cascade='all, delete-orphan')
    donations = db.relationship('Donation', back_populates='user', cascade='all, delete-orphan')
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    def has_role(self, role):
        return self.role == role
    
    def is_admin(self):
        return self.role == 'Admin'
    
    def is_department_responsible(self):
        from app.models.department import Department
        return Department.query.filter_by(responsible_id=self.id, is_active=True).first() is not None
    
    def __repr__(self):
        return f'<User {self.email}>'