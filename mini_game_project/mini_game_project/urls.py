"""
Root URL configuration for mini_game_project.

This module routes URLs to the appropriate view handlers. For more
information please see the Django documentation:
https://docs.djangoproject.com/en/dev/topics/http/urls/
"""
from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('game.urls', namespace='game')),
]

# Custom error handlers pointing to views in the game app
handler404 = 'game.views.custom_404'  # type: ignore
handler500 = 'game.views.custom_500'  # type: ignore