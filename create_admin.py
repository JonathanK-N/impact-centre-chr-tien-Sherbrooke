#!/usr/bin/env python3
from app import create_app, db
from app.models.user import User

def create_admin():
    app = create_app()
    
    with app.app_context():
        # Vérifier si l'admin existe déjà
        existing_admin = User.query.filter_by(email='admin@impactccsherbrooke.ca').first()
        
        if existing_admin:
            print("✅ Compte admin existe déjà !")
            print(f"Email: {existing_admin.email}")
            print(f"Rôle: {existing_admin.role}")
            return
        
        # Créer le compte admin
        admin = User(
            email='admin@impactccsherbrooke.ca',
            first_name='Admin',
            last_name='Principal',
            role='Admin',
            is_active=True
        )
        admin.set_password('Admin123!')
        
        db.session.add(admin)
        db.session.commit()
        
        print("🎉 Compte administrateur créé avec succès !")
        print("📧 Email: admin@impactccsherbrooke.ca")
        print("🔑 Mot de passe: Admin123!")
        print("🔗 Accès admin: /admin")

if __name__ == '__main__':
    create_admin()