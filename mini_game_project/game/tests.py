"""
Tests for the game app.

These unit tests validate model behaviors, the score calculation helper and
core view flows. They can be run with ``python manage.py test`` to
verify that the application logic is correct.
"""
import json
from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone

from .models import Player, GameSession
from .utils import compute_score


class ModelTestCase(TestCase):
    """Tests for models and helper functions."""

    def test_player_creation_and_string(self) -> None:
        player = Player.objects.create(name="Alice")
        self.assertEqual(str(player), "Alice")
        self.assertLessEqual(len(player.name), 30)

    def test_compute_score(self) -> None:
        self.assertEqual(compute_score(10, 5, 20), 10 * 10 + 5 * 5 + 20)


class ViewTestCase(TestCase):
    """Tests for view logic and full game loop."""

    def setUp(self) -> None:
        self.client = Client()
        # create player for tests
        self.player = Player.objects.create(name="Bob")

    def test_start_and_finish_flow(self) -> None:
        # Start a new game
        response = self.client.post(reverse('game:start_game'), {'name': 'Bob'})
        # Expect a redirect to play page
        self.assertEqual(response.status_code, 302)
        # Extract session id from last created GameSession
        session = GameSession.objects.latest('id')
        # Finish the game with JSON payload
        payload = {'hits': 10, 'combos': 3, 'duration': 25}
        finish_url = reverse('game:finish', args=[session.id])
        response = self.client.post(
            finish_url,
            data=json.dumps(payload),
            content_type='application/json',
        )
        self.assertEqual(response.status_code, 200)
        session.refresh_from_db()
        # Verify that session has ended and score computed correctly
        self.assertIsNotNone(session.ended_at)
        expected = compute_score(10, 3, 5.0)  # 30-second game, 25s elapsed => 5s left
        self.assertEqual(session.score, expected)

    def test_leaderboard_view(self) -> None:
        # Create a finished session
        GameSession.objects.create(
            player=self.player,
            started_at=timezone.now(),
            ended_at=timezone.now(),
            score=100,
        )
        response = self.client.get(reverse('game:leaderboard'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Top 10')