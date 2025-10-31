#!/usr/bin/env python3
"""Initialize database for production deployment."""

import os
from app import create_app
from app.extensions import db
from app.seeds import seed

def init_database():
    """Initialize database with tables and seed data."""
    app = create_app()
    
    with app.app_context():
        # Create all tables
        db.create_all()
        print("✅ Database tables created")
        
        # Add seed data if no users exist
        from app.models import User
        if User.query.count() == 0:
            seed()
            print("✅ Seed data added")
        else:
            print("ℹ️ Database already has data")

if __name__ == "__main__":
    init_database()