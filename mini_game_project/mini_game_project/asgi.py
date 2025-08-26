"""
ASGI config for mini_game_project.

This file exposes the ASGI callable as a module-level variable named
``application``.
"""
import os
from django.core.asgi import get_asgi_application  # type: ignore

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mini_game_project.settings')

application = get_asgi_application()