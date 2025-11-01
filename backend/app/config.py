"""Application configuration objects."""

from __future__ import annotations

import os
from datetime import timedelta

BASE_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
INSTANCE_DIR = os.path.join(BASE_DIR, "instance")
os.makedirs(INSTANCE_DIR, exist_ok=True)


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key")
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL",
        f"sqlite:///{os.path.join(INSTANCE_DIR, 'impact.db')}",
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "dev-jwt-secret")
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    PROPAGATE_EXCEPTIONS = True
    SWAGGER_UI_URL = "/api/docs"
    API_TITLE = "Impact Centre Chretien Sherbrooke API"
    API_VERSION = "1.0.0"
    # Allow future Firestore configuration placeholders
    FIRESTORE_PROJECT_ID = os.getenv("FIRESTORE_PROJECT_ID", "")
    FIRESTORE_CREDENTIALS_PATH = os.getenv("FIRESTORE_CREDENTIALS_PATH", "")


class DevelopmentConfig(Config):
    DEBUG = True


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite://"
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=5)


class ProductionConfig(Config):
    DEBUG = False
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=12)


config_by_name = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
}


def get_config():
    """Resolve configuration based on the FLASK_ENV environment variable."""
    env = os.getenv("FLASK_ENV", "development")
    return config_by_name.get(env, DevelopmentConfig)
