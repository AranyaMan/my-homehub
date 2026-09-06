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
    # Otherwise, allow access to setup and login routes only
    if User.query.first():
        # Per-user authentication mode - exempt login, setup, and static endpoints
        if not session.get('user_id') and not endpoint.startswith('static') and endpoint not in ('main.login', 'main.setup'):
            return redirect(url_for('main.login'))
    else:
        # No users yet - only allow access to setup and login routes
        if not endpoint.startswith('static') and endpoint not in ('main.login', 'main.setup'):
            return redirect(url_for('main.setup'))


@main_bp.route('/setup', methods=['GET', 'POST'])
def setup():
    # Only allow setup if no users exist
    if User.query.first():
        return redirect(url_for('main.login'))
    
    if request.method == 'POST':
        # Get form data for all three users
        admin_username = bleach.clean(request.form.get('admin_username', 'Admin').strip())
        admin_password = bleach.clean(request.form.get('admin_password', ''))
        aranya_username = bleach.clean(request.form.get('aranya_username', 'Aranya').strip())
        aranya_password = bleach.clean(request.form.get('aranya_password', ''))
        bidisha_username = bleach.clean(request.form.get('bidisha_username', 'Bidisha').strip())
        bidisha_password = bleach.clean(request.form.get('bidisha_password', ''))
        
        # Validate inputs
        errors = []
        if not admin_username:
            errors.append("Admin username is required")
        if not admin_password:
            errors.append("Admin password is required")
        if not aranya_username:
            errors.append("Aranya username is required")
        if not aranya_password:
            errors.append("Aranya password is required")
        if not bidisha_username:
            errors.append("Bidisha username is required")
        if not bidisha_password:
            errors.append("Bidisha password is required")
        
        # Check for duplicate usernames
        usernames = [admin_username, aranya_username, bidisha_username]
        if len(usernames) != len(set(usernames)):
            errors.append("Usernames must be unique")
        
        if not errors:
            # Create the three users
            users_to_create = [
                (admin_username, admin_password),
                (aranya_username, aranya_password),
                (bidisha_username, bidisha_password)
            ]
            
            try:
                for username, password in users_to_create:
                    user = User(username=username)
                    user.set_password(password)
                    db.session.add(user)
                db.session.commit()
                flash('Setup complete! You can now log in.', 'success')
                return redirect(url_for('main.login'))
            except Exception as e:
                db.session.rollback()
                flash('An error occurred during setup. Please try again.', 'error')
                current_app.logger.error(f"Setup error: {e}")
        else:
            for error in errors:
                flash(error, 'error')
    
    return render_template('setup.html', config=current_app.config.get('HOMEHUB_CONFIG', {}))


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
        # If no users exist, redirect to setup
        return redirect(url_for('main.setup'))


@main_bp.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('username', None)
    session.pop('authed', None)  # Clean up old auth flag
    flash('Logged out.', 'info')
    return redirect(url_for('main.login'))
