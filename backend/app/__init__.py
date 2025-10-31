"""Flask application factory for Impact Centre Chretien Sherbrooke."""

from __future__ import annotations

import logging
from pathlib import Path
from logging.config import dictConfig

from flask import Flask, jsonify, send_from_directory, abort

from .config import get_config
from .extensions import init_extensions, db


def create_app(config_object=None):
    """Create and configure the Flask application."""
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(config_object or get_config())

    configure_logging(app)
    init_extensions(app)
    register_blueprints(app)
    register_shellcontext(app)
    register_cli(app)
    register_error_handlers(app)
    register_spa_routes(app)

    return app


def configure_logging(app):
    """Configure structured logging for the backend."""
    if app.config.get("LOGGING_CONFIG_DICT"):
        dictConfig(app.config["LOGGING_CONFIG_DICT"])
        return

    dictConfig(
        {
            "version": 1,
            "formatters": {
                "default": {
                    "format": "[%(asctime)s] %(levelname)s in %(module)s: %(message)s",
                }
            },
            "handlers": {
                "console": {
                    "class": "logging.StreamHandler",
                    "formatter": "default",
                }
            },
            "root": {"level": "INFO", "handlers": ["console"]},
        }
    )


def register_blueprints(app):
    """Register API blueprints."""
    from .auth.routes import auth_bp
    from .departments.routes import departments_bp
    from .families.routes import families_bp
    from .events.routes import events_bp
    from .announcements.routes import announcements_bp
    from .donations.routes import donations_bp
    from .media.routes import media_bp
    from .members.routes import members_bp
    from .admin.routes import admin_bp
    from .api.docs import docs_bp

    api_prefix = "/api"
    app.register_blueprint(auth_bp, url_prefix=f"{api_prefix}/auth")
    app.register_blueprint(departments_bp, url_prefix=f"{api_prefix}/departments")
    app.register_blueprint(families_bp, url_prefix=f"{api_prefix}/families")
    app.register_blueprint(events_bp, url_prefix=f"{api_prefix}/events")
    app.register_blueprint(announcements_bp, url_prefix=f"{api_prefix}/announcements")
    app.register_blueprint(donations_bp, url_prefix=f"{api_prefix}/donations")
    app.register_blueprint(media_bp, url_prefix=f"{api_prefix}/media")
    app.register_blueprint(members_bp, url_prefix=f"{api_prefix}/members")
    app.register_blueprint(admin_bp, url_prefix=f"{api_prefix}/admin")
    app.register_blueprint(docs_bp, url_prefix=f"{api_prefix}/docs")


def register_shellcontext(app):
    """Add useful context to the Flask shell."""
    from . import models

    def shell_context():
        return {"db": db, "models": models}

    app.shell_context_processor(shell_context)


def register_cli(app):
    """Add custom CLI commands."""
    from .seeds import seed

    @app.cli.command("seed-db")
    def seed_db():
        """Seed the database with sample data."""
        seed()


def register_error_handlers(app):
    """Standardize JSON error responses."""

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({"message": "Bad request", "details": getattr(error, "description", "")}), 400

    @app.errorhandler(401)
    def unauthorized(error):
        return jsonify({"message": "Unauthorized", "details": getattr(error, "description", "")}), 401

    @app.errorhandler(403)
    def forbidden(error):
        return jsonify({"message": "Forbidden", "details": getattr(error, "description", "")}), 403

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({"message": "Not found", "details": getattr(error, "description", "")}), 404

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({"message": "Unprocessable entity", "details": getattr(error, "description", "")}), 422

    @app.errorhandler(500)
    def internal_error(error):
        logging.exception("Internal server error: %s", error)
        return jsonify({"message": "Internal server error"}), 500


def register_spa_routes(app):
    """Serve the React single-page application build."""
    dist_dir = Path(app.root_path) / "static" / "frontend"

    if not dist_dir.exists():
        app.logger.warning("Frontend build directory %s not found. Run `npm run build` inside frontend/.", dist_dir)

    @app.route("/", defaults={"path": ""})
    @app.route("/<path:path>")
    def serve_spa(path):
        if path.startswith("api/"):
            abort(404)

        target = dist_dir / path

        if path and target.exists():
            return send_from_directory(dist_dir, path)

        index_path = dist_dir / "index.html"
        if index_path.exists():
            return send_from_directory(dist_dir, "index.html")

        return jsonify(
            {
                "message": "Frontend build introuvable.",
                "detail": "Exécutez `npm install && npm run build` dans le dossier frontend/.",
            }
        ), 500
