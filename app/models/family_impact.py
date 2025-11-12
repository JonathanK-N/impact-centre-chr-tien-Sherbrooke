from datetime import datetime
from app import db

class FamilyImpact(db.Model):
    __tablename__ = 'families_impact'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    
    # Localisation
    address = db.Column(db.Text, nullable=False)
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    postal_code = db.Column(db.String(10))
    
    # Horaires
    meeting_day = db.Column(db.String(20))  # 'Lundi', 'Mardi', etc.
    meeting_time = db.Column(db.Time)
    
    # Responsable
    responsible_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    
    # Capacité et statut
    max_capacity = db.Column(db.Integer, default=15)
    is_active = db.Column(db.Boolean, default=True)
    is_full = db.Column(db.Boolean, default=False)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relations
    responsible = db.relationship('User', backref='managed_families')
    members = db.relationship('FamilyMember', back_populates='family', cascade='all, delete-orphan')
    announcements = db.relationship('Announcement', back_populates='family', cascade='all, delete-orphan')
    
    @property
    def current_members_count(self):
        return len([m for m in self.members if m.is_active])
    
    @property
    def available_spots(self):
        return max(0, self.max_capacity - self.current_members_count)
    
    def __repr__(self):
        return f'<FamilyImpact {self.name}>'

class FamilyMember(db.Model):
    __tablename__ = 'family_members'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    family_id = db.Column(db.Integer, db.ForeignKey('families_impact.id'), nullable=False)
    joined_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)
    status = db.Column(db.String(20), default='Pending')  # 'Pending', 'Approved', 'Rejected'
    
    # Relations
    user = db.relationship('User', back_populates='family_memberships')
    family = db.relationship('FamilyImpact', back_populates='members')
    
    __table_args__ = (db.UniqueConstraint('user_id', 'family_id', name='unique_user_family'),)