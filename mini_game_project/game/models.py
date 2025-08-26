"""
Models for the game application.

The game app defines a simple leaderboard-based mini-game. A ``Player`` is
identified by a name. Each time a user plays, a ``GameSession`` is
created to track when the game started and ended, the resulting score,
basic device information, and a hashed representation of the IP address.
Optionally, daily aggregates may be computed for analysis.
"""
from __future__ import annotations

import hashlib
from django.db import models


class Player(models.Model):
    """A human player identified by name.

    The name is limited to 30 characters and indexed for quick lookup.
    """

    name = models.CharField(max_length=30, unique=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']
        indexes = [models.Index(fields=['name'])]

    def __str__(self) -> str:
        return self.name


class GameSession(models.Model):
    """Represents a single play session for a player.

    Each session stores the start and end timestamps, the final score,
    the duration, the number of hits and combos achieved, basic device
    information, and a hash of the user's IP address. Scores are indexed
    so that leaderboards can be generated efficiently.
    """

    player = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='sessions')
    started_at = models.DateTimeField()
    ended_at = models.DateTimeField(null=True, blank=True)
    score = models.PositiveIntegerField(default=0)
    duration = models.DurationField(null=True, blank=True)
    hits = models.PositiveIntegerField(default=0)
    combos = models.PositiveIntegerField(default=0)
    device_info = models.CharField(max_length=255, blank=True)
    ip_hash = models.CharField(max_length=64, editable=False)

    class Meta:
        ordering = ['-score', 'ended_at']
        indexes = [
            models.Index(fields=['-score', 'ended_at']),
            models.Index(fields=['ended_at']),
        ]

    def __str__(self) -> str:
        return f'{self.player.name} session {self.pk}'

    def save(self, *args, **kwargs) -> None:
        """Override save to ensure the IP hash is set.

        If ``raw_ip`` has been provided on the instance (e.g., via a view)
        but ``ip_hash`` is empty, we compute the SHA-256 hash of the IP
        address. This avoids storing personally identifiable information.
        """
        if not self.ip_hash and hasattr(self, 'raw_ip') and self.raw_ip:
            self.ip_hash = hashlib.sha256(self.raw_ip.encode('utf-8')).hexdigest()
        super().save(*args, **kwargs)


class DailyAggregate(models.Model):
    """Stores aggregate statistics for each day.

    While optional for the core game, this model can be used to pre-compute
    daily leaderboards or analytics. Values are recalculated via a
    management command or scheduled task. It's not used directly by
    views in this implementation.
    """

    date = models.DateField(unique=True)
    best_score = models.PositiveIntegerField(default=0)
    avg_score = models.FloatField(default=0.0)

    class Meta:
        ordering = ['-date']

    def __str__(self) -> str:
        return str(self.date)