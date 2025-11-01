from datetime import datetime
from app import db

class Announcement(db.Model):
    __tablename__ = 'announcements'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    
    # Type et visibilité
    announcement_type = db.Column(db.String(50), default='General')  # 'General', 'Department', 'Family'
    priority = db.Column(db.String(20), default='Normal')  # 'Low', 'Normal', 'High', 'Urgent'
    
    # Ciblage
    target_department_id = db.Column(db.Integer, db.ForeignKey('departments.id'))
    target_family_id = db.Column(db.Integer, db.ForeignKey('families_impact.id'))
    
    # Auteur
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # Dates
    publish_date = db.Column(db.DateTime, default=datetime.utcnow)
    expiry_date = db.Column(db.DateTime)
    
    # Statut
    is_active = db.Column(db.Boolean, default=True)
    is_pinned = db.Column(db.Boolean, default=False)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relations
    author = db.relationship('User', backref='announcements')
    department = db.relationship('Department', back_populates='announcements')
    family = db.relationship('FamilyImpact', back_populates='announcements')
    
    @property
    def is_expired(self):
        if not self.expiry_date:
            return False
        return datetime.utcnow() > self.expiry_date
    
    @property
    def priority_class(self):
        priority_classes = {
            'Low': 'text-muted',
            'Normal': 'text-dark',
            'High': 'text-warning',
            'Urgent': 'text-danger'
        }
        return priority_classes.get(self.priority, 'text-dark')
    
    def __repr__(self):
        return f'<Announcement {self.title}>'