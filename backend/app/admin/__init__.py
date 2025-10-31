"""Admin-specific endpoints."""

from flask import Blueprint

admin_bp = Blueprint("admin", __name__)

from . import routes  # noqa: E402  pylint: disable=wrong-import-position
