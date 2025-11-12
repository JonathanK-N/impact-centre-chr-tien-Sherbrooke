from app import db
from datetime import datetime

class MediaResource(db.Model):
    __tablename__ = 'media_resources'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    media_type = db.Column(db.String(20), nullable=False)  # Video, Audio, Document
    url = db.Column(db.String(500), nullable=False)
    thumbnail_url = db.Column(db.String(500))
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relations
    author = db.relationship('User', backref='media_resources')