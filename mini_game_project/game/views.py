"""
Views for the game application.

These functions handle the HTTP requests for the mini game. They include
the home page, starting a game, playing the game, finishing a session
(where the score is computed and saved), displaying results, showing the
leaderboard, and player profiles. Custom error handlers are also
defined.
"""
from __future__ import annotations

import json
from typing import Any, Dict, Optional

from django.http import HttpRequest, HttpResponse, JsonResponse, HttpResponseBadRequest
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt

from .forms import StartGameForm
from .models import Player, GameSession
from .utils import compute_score


def home(request: HttpRequest) -> HttpResponse:
    """Render the home page with a form to start a new game."""
    form = StartGameForm()
    return render(request, 'game/home.html', {'form': form})


def start_game(request: HttpRequest) -> HttpResponse:
    """Handle the submission of the player's name and initiate a new session.

    On POST, validate the player's name, create or reuse a ``Player``
    instance, create a new ``GameSession`` with the current timestamp,
    record the client's IP address (hashed in ``GameSession.save``), and
    redirect to the play view. On GET, fall back to the home page.
    """
    if request.method == 'POST':
        form = StartGameForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            player, _ = Player.objects.get_or_create(name=name)
            session = GameSession.objects.create(
                player=player,
                started_at=timezone.now(),
            )
            # attach raw_ip temporarily so save() computes ip_hash
            session.raw_ip = request.META.get('REMOTE_ADDR', '')
            session.save()
            return redirect('game:play', session_id=session.pk)
    else:
        form = StartGameForm()
    return render(request, 'game/home.html', {'form': form})


def play(request: HttpRequest, session_id: int) -> HttpResponse:
    """Render the play page where the JavaScript game loop runs."""
    session = get_object_or_404(GameSession, pk=session_id)
    return render(request, 'game/play.html', {'session': session})


@csrf_exempt  # The JS fetch API sends JSON, so we exempt CSRF and rely on token in header
def finish(request: HttpRequest, session_id: int) -> JsonResponse:
    """Finish a game session by validating and persisting the score.

    The client sends a JSON payload with ``hits``, ``combos``, and
    ``duration`` (elapsed seconds). The server recalculates the score
    deterministically and updates the ``GameSession``. If the session
    has already been ended, no changes are made and a simple response
    is returned.
    """
    if request.method != 'POST':
        return HttpResponseBadRequest('Invalid method')  # type: ignore[return-value]
    session = get_object_or_404(GameSession, pk=session_id)
    # Idempotency: don't update finished sessions
    if session.ended_at:
        return JsonResponse({'status': 'finished', 'score': session.score})
    try:
        payload: Dict[str, Any] = json.loads(request.body.decode())
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    hits = int(payload.get('hits', 0))
    combos = int(payload.get('combos', 0))
    duration = float(payload.get('duration', 0))
    # compute remaining time; default game length is 30 seconds
    time_left = max(0.0, 30.0 - duration)
    score = compute_score(hits, combos, time_left)
    # populate session
    session.hits = hits
    session.combos = combos
    session.duration = timezone.timedelta(seconds=duration)
    session.score = score
    session.ended_at = timezone.now()
    # store device info if available (User-Agent header)
    session.device_info = request.META.get('HTTP_USER_AGENT', '')[:255]
    session.save()
    return JsonResponse({
        'status': 'ok',
        'score': score,
        'redirect_url': reverse('game:results', args=[session_id]),
    })


def results(request: HttpRequest, session_id: int) -> HttpResponse:
    """Display the final score and summary for a completed session."""
    session = get_object_or_404(GameSession, pk=session_id)
    return render(request, 'game/results.html', {'session': session})


def leaderboard(request: HttpRequest) -> HttpResponse:
    """Render the leaderboard with top scores for today, this week, and all time.

    Optionally highlight the requesting player's best score if
    ``player_id`` is supplied as a query parameter.
    """
    now = timezone.now()
    start_of_day = now.replace(hour=0, minute=0, second=0, microsecond=0)
    start_of_week = start_of_day - timezone.timedelta(days=start_of_day.weekday())
    top_today = GameSession.objects.filter(ended_at__gte=start_of_day).order_by('-score', 'ended_at')[:10]
    top_week = GameSession.objects.filter(ended_at__gte=start_of_week).order_by('-score', 'ended_at')[:10]
    top_all = GameSession.objects.order_by('-score', 'ended_at')[:10]
    player_id = request.GET.get('player_id')
    my_best = None
    if player_id:
        try:
            my_best = GameSession.objects.filter(player_id=player_id).order_by('-score').first()
        except (ValueError, Player.DoesNotExist):
            my_best = None
    context = {
        'top_today': top_today,
        'top_week': top_week,
        'top_all': top_all,
        'my_best': my_best,
    }
    return render(request, 'game/leaderboard.html', context)


def player_profile(request: HttpRequest, player_id: int) -> HttpResponse:
    """Show a player's profile with their best scores."""
    player = get_object_or_404(Player, pk=player_id)
    sessions = player.sessions.order_by('-score', 'ended_at')[:10]
    return render(request, 'game/profile.html', {'player': player, 'sessions': sessions})


def custom_404(request: HttpRequest, exception: Optional[Exception] = None) -> HttpResponse:
    """Custom handler for 404 errors."""
    return render(request, '404.html', status=404)


def custom_500(request: HttpRequest) -> HttpResponse:
    """Custom handler for 500 errors."""
    return render(request, '500.html', status=500)