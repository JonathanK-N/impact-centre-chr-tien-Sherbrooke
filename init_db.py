from app import create_app, db
from app.models.user import User

app = create_app('production')

with app.app_context():
    db.create_all()
    
    if not User.query.first():
        admin = User(
            email='admin@impactcentre.ca',
            first_name='Admin',
            last_name='Système',
            role='Admin'
        )
        admin.set_password('admin123')
        db.session.add(admin)
        db.session.commit()
        print("Admin créé")
    
    print("DB initialisée")