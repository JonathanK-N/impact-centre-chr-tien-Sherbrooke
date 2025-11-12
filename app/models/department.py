from datetime import datetime
from app import db

class Department(db.Model):
    __tablename__ = 'departments'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    responsible_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relations
    responsible = db.relationship('User', backref='managed_departments')
    members = db.relationship('DepartmentMember', back_populates='department', cascade='all, delete-orphan')
    announcements = db.relationship('Announcement', back_populates='department', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Department {self.name}>'

class DepartmentMember(db.Model):
    __tablename__ = 'department_members'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    department_id = db.Column(db.Integer, db.ForeignKey('departments.id'), nullable=False)
    joined_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)
    
    # Relations
    user = db.relationship('User', back_populates='department_memberships')
    department = db.relationship('Department', back_populates='members')
    
    __table_args__ = (db.UniqueConstraint('user_id', 'department_id', name='unique_user_department'),)