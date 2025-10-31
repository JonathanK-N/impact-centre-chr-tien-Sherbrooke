"""Simple OpenAPI specification exposure."""

from flask import Blueprint, jsonify

docs_bp = Blueprint("docs", __name__)


OPENAPI_SPEC = {
    "openapi": "3.0.2",
    "info": {
        "title": "Impact Centre Chretien Sherbrooke API",
        "version": "1.0.0",
        "description": "REST API for community management.",
    },
    "paths": {
        "/api/auth/register": {"post": {"summary": "Register a member"}},
        "/api/auth/login": {"post": {"summary": "Login and receive tokens"}},
        "/api/auth/me": {"get": {"summary": "Current user profile"}},
        "/api/departments": {"get": {"summary": "List departments"}, "post": {"summary": "Create department"}},
        "/api/families": {"get": {"summary": "List families"}, "post": {"summary": "Create family"}},
        "/api/events": {"get": {"summary": "List events"}, "post": {"summary": "Create event"}},
        "/api/announcements": {"get": {"summary": "List announcements"}, "post": {"summary": "Create announcement"}},
        "/api/media": {"get": {"summary": "List media items"}, "post": {"summary": "Create media item"}},
        "/api/donations": {"get": {"summary": "List donations"}, "post": {"summary": "Create donation record"}},
        "/api/members": {"get": {"summary": "List members"}, "post": {"summary": "Reserved for future use"}},
        "/api/admin/dashboard": {"get": {"summary": "Administrative dashboard insights"}},
    },
}


@docs_bp.get("/openapi.json")
def openapi():
    """Return a lightweight OpenAPI specification."""
    return jsonify(OPENAPI_SPEC)


@docs_bp.get("/")
def docs_home():
    """Provide quick instructions to use Swagger UI locally."""
    return jsonify(
        {
            "message": "Use any Swagger UI (e.g., https://editor.swagger.io/) and load /api/docs/openapi.json",
            "spec_url": "/api/docs/openapi.json",
        }
    )
