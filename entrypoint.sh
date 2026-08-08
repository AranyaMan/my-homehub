#!/bin/sh
set -e

# ── Validate required env vars ──────────────────────────────────────
if [ -z "$AUTH_USERNAME" ] || [ -z "$AUTH_PASSWORD" ]; then
    echo "ERROR: AUTH_USERNAME and AUTH_PASSWORD must be set."
    echo "       Set them in the Render Dashboard → Environment tab."
    exit 1
fi

# ── Ensure config.yml exists (required by HomeHub) ──────────────────
if [ ! -f /app/config.yml ]; then
    echo "⚠ No config.yml found — copying config-example.yml as default"
    cp /app/config-example.yml /app/config.yml
fi

# ── Generate .htpasswd at runtime ───────────────────────────────────
# Clean any trailing carriage returns or newlines from environment variables
AUTH_USERNAME=$(printf '%s' "$AUTH_USERNAME" | tr -d '\r\n')
AUTH_PASSWORD=$(printf '%s' "$AUTH_PASSWORD" | tr -d '\r\n')

# Uses htpasswd with bcrypt (-B) for Nginx compatibility
htpasswd -B -c /etc/nginx/.htpasswd "$AUTH_USERNAME" "$AUTH_PASSWORD"
chmod 644 /etc/nginx/.htpasswd
echo "✔ Generated /etc/nginx/.htpasswd (chmod 644) for user: $AUTH_USERNAME"

# ── Ensure data directories exist ──────────────────────────────────
mkdir -p /app/uploads /app/media /app/pdfs /app/data

# ── Launch supervisord (manages nginx + gunicorn) ──────────────────
exec /usr/bin/supervisord -c /app/supervisord.conf
