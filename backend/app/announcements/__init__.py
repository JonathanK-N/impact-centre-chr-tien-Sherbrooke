"""Announcements blueprint."""

from flask import Blueprint

announcements_bp = Blueprint("announcements", __name__)

from . import routes  # noqa: E402  pylint: disable=wrong-import-position
