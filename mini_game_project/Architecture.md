# Architecture Overview

This document describes the internal architecture of the Reaction Rush
application at a high level. It covers the data model relationships and the
request/response flow through the system.

## Data Model

The game revolves around two primary entities: `Player` and `GameSession`.
Players are uniquely identified by their name (up to 30 characters). Each
playthrough creates a new game session, which stores the timing and scoring
data. An optional `DailyAggregate` model is provided for future analytics.

### Entity Relationship Diagram

```
          +---------------+           +-----------------------+
          |   Player      |1         *|    GameSession        |
          +---------------+-----------+-----------------------+
          | id (PK)       |           | id (PK)              |
          | name          |           | player_id (FK)        |
          | created_at    |           | started_at            |
          +---------------+           | ended_at              |
                                        | score                |
                                        | duration             |
                                        | hits                 |
                                        | combos               |
                                        | device_info          |
                                        | ip_hash              |
                                        +-----------------------+
```

- **Player**: Represents a user by name. The `created_at` timestamp records
  when the player first registered.
- **GameSession**: Captures a single round of play. Each session links to a
  player via a foreign key and stores the start and end times, final
  score, duration, hit and combo counts, basic device information,
  and a SHA‑256 hash of the originating IP address.
- **DailyAggregate**: Not used directly by views but can be populated by
  management commands to summarize daily performance (e.g. best score,
  average score).

Indexes are defined on score and end time to facilitate efficient
leaderboard queries.

## Request Flow

1. **Home Page (`/`)**: Displays a form where the player enters their name.

2. **Start Game (`POST /start/`)**:
   - Validates the submitted name via `StartGameForm`.
   - Creates or retrieves a `Player` instance.
   - Creates a new `GameSession` with `started_at` set to the current
     time and stores a hash of the client’s IP address.
   - Redirects to `/play/<session_id>/`.

3. **Play Page (`/play/<id>/`)**:
   - Renders the game canvas and HUD elements.
   - Loads `static/game/game.js`, which runs the 30‑second game loop in
     the browser, spawning targets and tracking hits and combos.

4. **Finish Game (`POST /finish/<id>/`)**:
   - Called by the JavaScript when time runs out.
   - Parses a JSON payload containing `hits`, `combos`, and `duration`.
   - Computes the final score server‑side using the deterministic formula.
   - Updates the `GameSession` with end time, score, hits, combos and
     duration, and records the user agent string as device info.
   - Returns a JSON response with a redirect URL to the results page.

5. **Results Page (`/results/<id>/`)**:
   - Displays the final score, hits, combos and duration for the
     completed session.
   - Offers links to replay (`/play/<id>/`) and view the leaderboard
     (`/leaderboard/?player_id=<player_id>`).

6. **Leaderboard (`/leaderboard/`)**:
   - Shows the top ten scores for today, this week, and all time.
   - Accepts an optional `player_id` query parameter to highlight the
     requesting player's best score.

7. **Player Profile (`/profile/<player_id>/`)** (optional):
   - Lists the best scores for the specified player.

Custom handlers for 404 and 500 errors are provided, rendering friendly
error pages.

## Security Considerations

The application hashes IP addresses to avoid storing sensitive data. It
uses Django’s CSRF protection by default and validates scores server‑side
to prevent tampering. For additional recommendations (SSL, secure
cookies, rate limiting), see **SECURITY.md**.