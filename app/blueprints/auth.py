from flask import current_app, request, session, redirect, url_for, render_template, flash
from ..blueprints import main_bp
from .. import db
from ..models import User
import hashlib
import bleach


@main_bp.before_app_request
def reload_config_and_auth():
    try:
        current_app.config['HOMEHUB_CONFIG'] = load_config()
    except Exception:
        pass
    cfg = current_app.config.get('HOMEHUB_CONFIG', {})
    endpoint = request.endpoint or ''
    
    # Check if we have any users in the database - if so, require authentication
    # Otherwise, fall back to site-wide password for backward compatibility during setup
    if User.query.first():
        # Per-user authentication mode
        if not session.get('user_id') and not endpoint.startswith('static') and endpoint not in ('main.login', 'main.register'):
            return redirect(url_for('main.login'))
    else:
        # Site-wide password mode (backward compatibility)
        if cfg.get('password_hash'):
            if not session.get('authed') and not endpoint.startswith('static') and endpoint not in ('main.login',):
                return redirect(url_for('main.login'))
        else:
            if endpoint == 'main.login':
                return redirect(url_for('main.index'))


@main_bp.route('/login', methods=['GET', 'POST'])
def login():
    # If we have users, use per-user authentication
    if User.query.first():
        if request.method == 'POST':
            username = bleach.clean(request.form.get('username', ''))
            password = bleach.clean(request.form.get('password', ''))
            
            user = User.query.filter_by(username=username).first()
            
            if user and user.check_password(password):
                session['user_id'] = user.id
                session['username'] = user.username
                flash('Logged in successfully.', 'success')
                return redirect(url_for('main.index'))
            
            flash('Invalid username or password', 'error')
        
        return render_template('login.html', config=current_app.config.get('HOMEHUB_CONFIG', {}), hide_user_ui=True)
    else:
        # Fallback to site-wide password for initial setup
        config = current_app.config.get('HOMEHUB_CONFIG', {})
        if not config.get('password_hash'):
            return redirect(url_for('main.index'))
        if request.method == 'POST':
            supplied = bleach.clean(request.form.get('password', ''))
            if hashlib.sha256(supplied.encode()).hexdigest() == config.get('password_hash'):
                session['authed'] = True
                flash('Logged in successfully.', 'success')
                return redirect(url_for('main.index'))
            flash('Invalid password', 'error')
        return render_template('login.html', config=config, hide_user_ui=True)


@main_bp.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('username', None)
    session.pop('authed', None)  # Clean up old auth flag
    flash('Logged out.', 'info')
    return redirect(url_for('main.login'))
