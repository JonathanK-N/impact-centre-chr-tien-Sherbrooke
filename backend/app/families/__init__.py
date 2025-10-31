"""Families d'Impact blueprint."""

from flask import Blueprint

families_bp = Blueprint("families", __name__)

from . import routes  # noqa: E402  pylint: disable=wrong-import-position
