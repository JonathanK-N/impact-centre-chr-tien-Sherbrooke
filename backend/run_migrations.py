#!/usr/bin/env python3
"""Script pour initialiser la base de données directement."""

import os
import sys

# Ajouter le répertoire courant au path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from app.extensions import db

def init_db():
    """Initialise la base de données."""
    app = create_app()
    
    with app.app_context():
        # Créer toutes les tables
        db.create_all()
        print("✅ Base de données initialisée avec succès!")
        
        # Importer et exécuter les seeds
        from app.seeds import seed
        seed()
        print("✅ Données de test ajoutées avec succès!")

if __name__ == "__main__":
    init_db()