"""Department management blueprint."""

from flask import Blueprint

departments_bp = Blueprint("departments", __name__)

from . import routes  # noqa: E402  pylint: disable=wrong-import-position
