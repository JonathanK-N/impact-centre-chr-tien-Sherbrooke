import os
from app import create_app, db

application = create_app(os.getenv('FLASK_CONFIG') or 'default')

# Initialiser la base de données au démarrage
with application.app_context():
    try:
        db.create_all()
    except Exception as e:
        print(f"Erreur lors de l'initialisation de la base de données: {e}")

if __name__ == "__main__":
    application.run()