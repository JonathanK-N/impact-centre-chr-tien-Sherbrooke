"""Donations blueprint."""

from flask import Blueprint

donations_bp = Blueprint("donations", __name__)

from . import routes  # noqa: E402  pylint: disable=wrong-import-position
