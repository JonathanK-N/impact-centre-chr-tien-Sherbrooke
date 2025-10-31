"""Members blueprint."""

from flask import Blueprint

members_bp = Blueprint("members", __name__)

from . import routes  # noqa: E402  pylint: disable=wrong-import-position
