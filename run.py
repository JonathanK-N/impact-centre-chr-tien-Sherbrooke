#!/usr/bin/env python3
"""
Script de démarrage pour Impact Centre Chrétien Sherbrooke
"""

import os
from app import create_app

if __name__ == '__main__':
    # Créer l'application
    app = create_app(os.getenv('FLASK_CONFIG') or 'development')
    
    # Lancer l'application
    print("=" * 60)
    print("🏛️  IMPACT CENTRE CHRÉTIEN SHERBROOKE")
    print("=" * 60)
    print("📍 Application disponible sur: http://localhost:5000")
    print("👤 Compte admin: admin@impactcentre.ca / admin123")
    print("=" * 60)
    
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True
    )