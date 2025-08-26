# Reaction Rush Game

Reaction Rush is a fast-paced, replayable mini‑game built with Django. You have
30 seconds to click as many targets as possible. Each hit earns points,
combos grant bonuses, and any remaining time adds to your final score. After
finishing, your score is saved and displayed on the global leaderboard. Can you
reach the top?

## Game Concept

**Reaction Rush (Option A)**: Randomly appearing targets pop up in the play
area. Click them before they disappear to score points. Consecutive hits
within 800 ms count as combos and grant extra points. The game lasts
exactly 30 seconds. This simple mechanic keeps games short (30–90 seconds
including page loads) and encourages replayability while allowing fair
server‑side scoring.

### Scoring Formula

The final score is calculated on the server using a deterministic formula:

- **Hits**: `10 × number_of_hits`
- **Combos**: `5 × number_of_combos`
- **Time Bonus**: `1 × whole_seconds_left`

`final_score = hits * 10 + combos * 5 + floor(time_left)`

For example, 10 hits, 3 combos and 5 seconds remaining yields
`10×10 + 3×5 + 5 = 135` points.

## Quickstart

1. **Clone** this repository and enter the project directory:

   ```bash
   git clone <repo-url>
   cd mini_game_project
   ```

2. **Create a virtual environment** and activate it (Python 3.11+):

   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows use .venv\Scripts\activate
   ```

3. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**. Copy `.env.example` to `.env` and
   adjust values as needed. At minimum, set a unique `DJANGO_SECRET_KEY`.

5. **Run migrations**:

   ```bash
   python manage.py migrate
   ```

6. **Start the development server**:

   ```bash
   python manage.py runserver
   ```

7. Open your browser at [http://localhost:8000](http://localhost:8000) and
   enjoy!

## Environment Variables

The project reads configuration from environment variables. Create a `.env`
file based on `.env.example` and set:

- `DJANGO_SECRET_KEY`: A long, random string for cryptographic signing.
- `DJANGO_DEBUG`: `True` for development, `False` in production.
- `DJANGO_ALLOWED_HOSTS`: Comma‑separated list of hosts (e.g.
  `example.com,www.example.com`).

## Running Tests

Execute the unit tests with:

```bash
python manage.py test
```

This runs model tests, score calculation checks, and view tests to verify
the start/finish flow and leaderboard rendering.

## Deployment Guide

The application can be deployed on any platform that supports Python
and Django. Below is a brief outline for two common scenarios.

### Gunicorn + Nginx

1. Install Gunicorn:

   ```bash
   pip install gunicorn
   ```

2. Run migrations and collect static files:

   ```bash
   python manage.py migrate
   python manage.py collectstatic --no-input
   ```

3. Start Gunicorn:

   ```bash
   gunicorn mini_game_project.wsgi:application --bind 0.0.0.0:8000 --workers 3
   ```

4. Configure Nginx as a reverse proxy to forward requests to Gunicorn and
   serve static files from the `staticfiles` directory. Refer to the
   official Django deployment checklist and adjust the secure settings in
   `settings.py`.

### One‑Click PaaS (e.g. Render, Railway)

1. Create a new web service and connect it to your repository.
2. Set environment variables (`DJANGO_SECRET_KEY`, `DJANGO_DEBUG`,
   `DJANGO_ALLOWED_HOSTS`) in the dashboard.
3. Specify the build command:

   ```bash
   pip install -r requirements.txt && python manage.py migrate && python manage.py collectstatic --no-input
   ```

4. Specify the start command:

   ```bash
   gunicorn mini_game_project.wsgi:application --bind 0.0.0.0:$PORT
   ```

The platform will automatically handle HTTPS, scaling and static file serving.

## Project Structure

```
mini_game_project/
├── manage.py          # Django management utility
├── mini_game_project/ # Project package
│   ├── __init__.py
│   ├── settings.py    # Project settings
│   ├── urls.py        # Root URL configuration
│   ├── wsgi.py        # WSGI entry point
│   └── asgi.py        # ASGI entry point
├── game/              # Game application
│   ├── __init__.py
│   ├── admin.py       # Django admin configuration
│   ├── apps.py        # App configuration
│   ├── forms.py       # Forms
│   ├── models.py      # Data models
│   ├── tests.py       # Unit tests
│   ├── utils.py       # Helper functions
│   ├── views.py       # Request handlers
│   ├── urls.py        # App URL patterns
│   ├── static/game/   # Static assets (JS, CSS)
│   │   ├── game.js
│   │   └── styles.css
│   └── templates/game/# HTML templates
│       ├── base.html
│       ├── home.html
│       ├── play.html
│       ├── results.html
│       ├── leaderboard.html
│       └── profile.html
├── templates/         # Global templates
│   ├── 404.html
│   └── 500.html
├── .env.example       # Example environment variables
├── requirements.txt   # Python dependencies
├── tailwind.config.js # Tailwind CSS config (optional)
├── README.md          # This file
├── Architecture.md    # System design overview
└── SECURITY.md        # Security considerations
```

## Contact

If you encounter any issues or have suggestions for improvement, please
open an issue or submit a pull request. Enjoy playing!