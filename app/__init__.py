from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from config import config

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()

def create_app(config_name='default'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Veuillez vous connecter pour accéder à cette page.'
    login_manager.login_message_category = 'info'
    
    # Import models
    from app.models import user, department, family_impact, event, announcement, donation, formation, media
    
    # Register blueprints
    from app.routes.auth import auth_bp
    from app.routes.main import main_bp
    from app.routes.admin import admin_bp
    from app.routes.departments import departments_bp
    from app.routes.department import department_bp
    from app.routes.families import families_bp
    from app.routes.events import events_bp
    from app.routes.donations import donations_bp
    from app.routes.media import media_bp
    from app.routes.formations import formations_bp
    
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(main_bp)
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(departments_bp, url_prefix='/departments')
    app.register_blueprint(department_bp, url_prefix='/department')
    app.register_blueprint(families_bp, url_prefix='/families')
    app.register_blueprint(events_bp, url_prefix='/events')
    app.register_blueprint(donations_bp, url_prefix='/donations')
    app.register_blueprint(media_bp, url_prefix='/media')
    app.register_blueprint(formations_bp, url_prefix='/formations')
    
    @login_manager.user_loader
    def load_user(user_id):
        from app.models.user import User
        return User.query.get(int(user_id))
    
    # Template helpers
    @app.template_global()
    def current_year():
        from datetime import datetime
        return datetime.now().year
    
    # Route de santé pour Railway
    @app.route('/health')
    def health_check():
        return 'OK', 200
    
    return app