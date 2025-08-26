"""
URL configuration for the game app.

Routes all the view functions defined in ``views.py``. Namespaces are used
to avoid conflicts with other apps.
"""
from django.urls import path
from . import views

app_name = 'game'

urlpatterns = [
    path('', views.home, name='home'),
    path('start/', views.start_game, name='start_game'),
    path('play/<int:session_id>/', views.play, name='play'),
    path('finish/<int:session_id>/', views.finish, name='finish'),
    path('results/<int:session_id>/', views.results, name='results'),
    path('leaderboard/', views.leaderboard, name='leaderboard'),
    path('profile/<int:player_id>/', views.player_profile, name='player_profile'),
]