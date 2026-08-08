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
# Clean existing htpasswd file
rm -f /etc/nginx/.htpasswd

# 1. Add primary user (AUTH_USERNAME / AUTH_PASSWORD)
if [ -n "$AUTH_USERNAME" ] && [ -n "$AUTH_PASSWORD" ]; then
    AUTH_USERNAME=$(printf '%s' "$AUTH_USERNAME" | tr -d '\r\n')
    AUTH_PASSWORD=$(printf '%s' "$AUTH_PASSWORD" | tr -d '\r\n')
    htpasswd -b -c -B /etc/nginx/.htpasswd "$AUTH_USERNAME" "$AUTH_PASSWORD"
    echo "✔ Added primary user: $AUTH_USERNAME"
fi

# 2. Add additional family users if AUTH_USERS is set
# Example format in Render env var: AUTH_USERS="mom:pass1,dad:pass2,alex:pass3"
if [ -n "$AUTH_USERS" ]; then
    # Create file if it didn't exist yet
    [ ! -f /etc/nginx/.htpasswd ] && touch /etc/nginx/.htpasswd
    
    OLD_IFS="$IFS"
    IFS=','
    for pair in $AUTH_USERS; do
        u=$(echo "$pair" | cut -d':' -f1 | tr -d '\r\n ')
        p=$(echo "$pair" | cut -d':' -f2 | tr -d '\r\n ')
        if [ -n "$u" ] && [ -n "$p" ]; then
            htpasswd -b -B /etc/nginx/.htpasswd "$u" "$p"
            echo "✔ Added family member: $u"
        fi
    done
    IFS="$OLD_IFS"
fi

chmod 644 /etc/nginx/.htpasswd

# ── Ensure data directories exist ──────────────────────────────────
mkdir -p /app/uploads /app/media /app/pdfs /app/data

# ── Launch supervisord (manages nginx + gunicorn) ──────────────────
exec /usr/bin/supervisord -c /app/supervisord.conf
