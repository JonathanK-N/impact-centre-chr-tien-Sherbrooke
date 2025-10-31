"""Authorization decorators for role-based access control."""

from functools import wraps

from flask import jsonify
from flask_jwt_extended import get_jwt

from ..models import Role


def role_required(*allowed_roles):
    """Restrict endpoint access to the given roles."""

    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            claims = get_jwt()
            role = claims.get("role")
            if role not in {r.value if isinstance(r, Role) else r for r in allowed_roles}:
                return jsonify({"message": "Insufficient permissions"}), 403
            return fn(*args, **kwargs)

        return wrapper

    return decorator


def roles_to_str(*roles):
    """Normalize role values to strings for documentation."""
    return [r.value if isinstance(r, Role) else r for r in roles]
