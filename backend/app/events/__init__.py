"""Events blueprint."""

from flask import Blueprint

events_bp = Blueprint("events", __name__)

from . import routes  # noqa: E402  pylint: disable=wrong-import-position
