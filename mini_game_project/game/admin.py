"""
Admin configuration for the game app.

Register the models so that administrators can manage players and
sessions from the Django admin interface. Custom list displays are
provided to improve readability.
"""
from django.contrib import admin
from .models import Player, GameSession, DailyAggregate


@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'created_at')
    search_fields = ('name',)
    ordering = ('name',)


@admin.register(GameSession)
class GameSessionAdmin(admin.ModelAdmin):
    list_display = ('id', 'player', 'score', 'hits', 'combos', 'started_at', 'ended_at')
    list_filter = ('started_at', 'ended_at')
    search_fields = ('player__name',)
    readonly_fields = ('ip_hash',)


@admin.register(DailyAggregate)
class DailyAggregateAdmin(admin.ModelAdmin):
    list_display = ('date', 'best_score', 'avg_score')
    ordering = ('-date',)