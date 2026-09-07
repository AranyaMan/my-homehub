from flask import current_app

# Legacy names treated as administrators regardless of the configured admin_name
ADMIN_ALIASES = {'Administrator', 'admin'}


def admin_aliases() -> set[str]:
    """Configured admin name plus the legacy aliases treated as administrators."""
    cfg = current_app.config.get('HOMEHUB_CONFIG', {})
    return {cfg.get('admin_name', 'Administrator')} | ADMIN_ALIASES


def is_admin(user) -> bool:
    """Whether the given user is treated as an administrator."""
    return bool(user) and user in admin_aliases()


def can_edit(user, creator) -> bool:
    """Admins may act on any record; other users may only act on their own."""
    if not user:
        return False
    return user in admin_aliases() or user == (creator or '')
