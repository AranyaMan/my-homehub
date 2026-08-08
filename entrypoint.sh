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
rm -f /etc/nginx/.htpasswd
touch /etc/nginx/.htpasswd

# 1. Add primary user (AUTH_USERNAME / AUTH_PASSWORD)
if [ -n "$AUTH_USERNAME" ] && [ -n "$AUTH_PASSWORD" ]; then
    u=$(printf '%s' "$AUTH_USERNAME" | tr -d '\r\n ')
    p=$(printf '%s' "$AUTH_PASSWORD" | tr -d '\r\n ')
    htpasswd -b -c -B /etc/nginx/.htpasswd "$u" "$p"
    echo "✔ Added user: $u"
fi

# 2. Add users from AUTH_USERS="user1:pass1,user2:pass2"
if [ -n "$AUTH_USERS" ]; then
    OLD_IFS="$IFS"
    IFS=','
    for pair in $AUTH_USERS; do
        u=$(echo "$pair" | cut -d':' -f1 | tr -d '\r\n ')
        p=$(echo "$pair" | cut -d':' -f2 | tr -d '\r\n ')
        if [ -n "$u" ] && [ -n "$p" ]; then
            htpasswd -b -B /etc/nginx/.htpasswd "$u" "$p"
            echo "✔ Added user: $u"
        fi
    done
    IFS="$OLD_IFS"
fi

# 3. Automatically treat any custom KEY=VALUE env var as USERNAME=PASSWORD
# (e.g. KEY: Dustu, VALUE: Bidisha@123)
env | while IFS='=' read -r key val; do
    key=$(echo "$key" | tr -d '\r\n ')
    val=$(echo "$val" | tr -d '\r\n ')
    case "$key" in
        AUTH_USERNAME|AUTH_PASSWORD|AUTH_USERS|SECRET_KEY|FLASK_ENV|PORT|RENDER*|PATH|HOME|HOSTNAME|PWD|SHLVL|SW_CACHE_VERSION|_|APP_VERSION)
            # Skip built-in system variables
            ;;
        *)
            if [ -n "$key" ] && [ -n "$val" ]; then
                htpasswd -b -B /etc/nginx/.htpasswd "$key" "$val"
                echo "✔ Auto-detected custom login for user: $key"
            fi
            ;;
    esac
done

chmod 644 /etc/nginx/.htpasswd

# ── Ensure data directories exist ──────────────────────────────────
mkdir -p /app/uploads /app/media /app/pdfs /app/data

# ── Launch supervisord (manages nginx + gunicorn) ──────────────────
exec /usr/bin/supervisord -c /app/supervisord.conf
