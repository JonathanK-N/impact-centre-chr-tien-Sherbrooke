from datetime import datetime
from app import db

class Event(db.Model):
    __tablename__ = 'events'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    
    # Date et heure
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime)
    
    # Localisation
    location = db.Column(db.String(200))
    address = db.Column(db.Text)
    
    # Type et visibilité
    event_type = db.Column(db.String(50), default='General')  # 'General', 'Department', 'Family'
    target_department_id = db.Column(db.Integer, db.ForeignKey('departments.id'))
    target_family_id = db.Column(db.Integer, db.ForeignKey('families_impact.id'))
    
    # Capacité et inscription
    max_participants = db.Column(db.Integer)
    registration_required = db.Column(db.Boolean, default=False)
    registration_deadline = db.Column(db.DateTime)
    
    # Organisateur
    organizer_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    
    # Statut
    is_active = db.Column(db.Boolean, default=True)
    is_cancelled = db.Column(db.Boolean, default=False)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relations
    organizer = db.relationship('User', backref='organized_events')
    target_department = db.relationship('Department', backref='events')
    target_family = db.relationship('FamilyImpact', backref='events')
    participants = db.relationship('EventParticipant', back_populates='event', cascade='all, delete-orphan')
    
    @property
    def current_participants_count(self):
        return len([p for p in self.participants if p.status == 'Confirmed'])
    
    @property
    def available_spots(self):
        if not self.max_participants:
            return None
        return max(0, self.max_participants - self.current_participants_count)
    
    @property
    def is_full(self):
        if not self.max_participants:
            return False
        return self.current_participants_count >= self.max_participants
    
    def __repr__(self):
        return f'<Event {self.title}>'

class EventParticipant(db.Model):
    __tablename__ = 'event_participants'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'), nullable=False)
    registered_at = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20), default='Confirmed')  # 'Confirmed', 'Cancelled', 'Waiting'
    
    # Relations
    user = db.relationship('User', back_populates='event_participations')
    event = db.relationship('Event', back_populates='participants')
    
    __table_args__ = (db.UniqueConstraint('user_id', 'event_id', name='unique_user_event'),)