"""
WSGI config for mini_game_project.

This file exposes the WSGI callable as a module-level variable named
``application``. It is used by Django's development server and any WSGI
compliant web server such as Gunicorn.
"""
import os
from django.core.wsgi import get_wsgi_application  # type: ignore

# Set the default settings module for the 'django' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mini_game_project.settings')

application = get_wsgi_application()