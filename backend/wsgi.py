"""WSGI entrypoint for production servers."""

from .app import app

__all__ = ["app"]
