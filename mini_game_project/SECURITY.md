# Security Notes

This document outlines the security measures implemented in the Reaction Rush
application and provides guidance on additional hardening steps for
deployment.

## Anti‑Cheat Measures

- **Server‑Side Score Calculation**: Clients send only minimal metrics
  (`hits`, `combos`, `duration`). The final score is recalculated on
  the server using a deterministic formula (`hits × 10 + combos × 5 +
  floor(time_left)`). This prevents tampering with the displayed score.

- **Idempotent Finish Endpoint**: If a session has already been
  finalized, subsequent requests to `POST /finish/<id>/` return the
  stored score without modifying the record. This prevents duplicate
  submissions.

- **Input Validation**: Numeric values are cast to the appropriate
  types and clamped where necessary (e.g. remaining time cannot be
  negative).

- **IP Hashing**: The user’s raw IP address is never stored. Instead,
  a SHA‑256 hash is computed in `GameSession.save()` if `raw_ip` is
  provided. This obfuscates sensitive information while still allowing
  coarse rate limiting or analytics.

- **Rate Limiting**: Django does not include built‑in rate limiting, but
  endpoints are simple and can be protected behind a reverse proxy like
  Nginx or via Django middleware such as `django-ratelimit`. Configure a
  per‑IP limit on `POST /start/` and `POST /finish/<id>/` to mitigate
  abuse.

## Django Security Settings

For production deployments, enable the following settings in
`mini_game_project/settings.py`:

- `SESSION_COOKIE_SECURE = True`
- `CSRF_COOKIE_SECURE = True`
- `SECURE_BROWSER_XSS_FILTER = True`
- `SECURE_CONTENT_TYPE_NOSNIFF = True`
- `SECURE_SSL_REDIRECT = True`
- `X_FRAME_OPTIONS = 'DENY'`

Consult the [Django deployment checklist](https://docs.djangoproject.com/en/dev/howto/deployment/checklist/)
for further guidance.

## Dependencies

Keep your dependencies up to date. Use `pip list --outdated` to
identify packages that require updates and apply patches promptly.

## Authentication and Authorization

This game does not implement user accounts beyond a simple name. If you
extend it to include login or user profiles, use Django’s built‑in
authentication system and enforce strong password policies.

## Additional Recommendations

- Use HTTPS everywhere and obtain TLS certificates via Let’s Encrypt.
- Regularly back up your database and static assets.
- Monitor logs for unusual activity and consider alerting on repeated
  failed requests.