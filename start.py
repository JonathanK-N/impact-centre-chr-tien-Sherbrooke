import os
from app import create_app, db

# Créer l'application
app = create_app('production')

# Initialiser la DB si nécessaire
with app.app_context():
    try:
        db.create_all()
        
        # Créer admin si pas d'utilisateurs
        from app.models.user import User
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
            print("Admin user created")
        
        print("Database ready")
    except Exception as e:
        print(f"Database error: {e}")

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)