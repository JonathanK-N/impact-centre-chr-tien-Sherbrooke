"""Authentication blueprint."""

from flask import Blueprint

auth_bp = Blueprint("auth", __name__)

from . import routes  # noqa: E402  pylint: disable=wrong-import-position
