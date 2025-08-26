# Manual Test Plan

This document outlines a simple manual testing procedure to verify that
Reaction Rush functions correctly in a development environment.

## Happy Path

1. **Homepage loads**
   - Navigate to `/`.
   - Verify that the welcome text, rules and name form are visible.
   - Ensure the “Start Game” button is disabled unless a name is entered.

2. **Start a new game**
   - Enter a valid name (≤ 30 characters) and submit the form.
   - Confirm that you are redirected to `/play/<id>/` where `<id>` is a
     numeric session identifier.
   - A blank play area and HUD (hits, combos, time left) should be visible.

3. **Play the game**
   - Targets appear at random positions within the game area.
   - Click targets quickly. Hits and combos increment appropriately.
   - The timer counts down from 30 seconds to 0.
   - When the timer reaches 0, no more targets appear and the game ends.

4. **Finish and view results**
   - After the game ends, you should be redirected to `/results/<id>/`.
   - The final score, hits, combos and duration should display.
   - Links to replay and view the leaderboard should work.

5. **Leaderboard**
   - Navigate to `/leaderboard/`.
   - Verify that tables for “Top 10 Today”, “This Week” and “All Time” are shown.
   - Confirm that your recent score appears in the appropriate sections.
   - Click player names to view profiles; ensure that the best scores list
     appears.

## Edge Cases

1. **Duplicate submission**
   - Reload `/results/<id>/` and confirm that the score does not duplicate in
     the leaderboard.

2. **Invalid finish payload**
   - Use browser dev tools or a tool like `curl` to POST invalid JSON to
     `/finish/<id>/` and verify that the server responds with a 400 error.

3. **Missing session**
   - Attempt to access `/play/9999/` or `/results/9999/` where `9999` is a non‑existent ID.
   - Ensure that a 404 page is displayed.

4. **Name validation**
   - Submit an empty name or a name longer than 30 characters.
   - Verify that the form raises a validation error and does not start a game.

5. **Leaderboard empty state**
   - Reset the database or remove GameSession entries and load `/leaderboard/`.
   - Confirm that appropriate “No scores yet.” messages show for each table.

## Notes

This plan focuses on functional aspects. Cross-browser compatibility,
accessibility audits and performance testing should also be considered for
a production release.