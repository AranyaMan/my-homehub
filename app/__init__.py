from flask import Flask, session
from flask_sqlalchemy import SQLAlchemy
from .config import load_config
import os
import secrets

db = SQLAlchemy()


def create_app(test_config: dict | None = None):
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    templates_dir = os.path.join(base_dir, 'templates')
    static_dir = os.path.join(base_dir, 'static')

    app = Flask(
        __name__,
        template_folder=templates_dir,
        static_folder=static_dir,
    )

    # Paths
    data_dir = os.path.join(base_dir, 'data')
    uploads_dir = os.path.join(base_dir, 'uploads')
    media_dir = os.path.join(base_dir, 'media')
    pdfs_dir = os.path.join(base_dir, 'pdfs')
    os.makedirs(data_dir, exist_ok=True)
    os.makedirs(uploads_dir, exist_ok=True)
    os.makedirs(media_dir, exist_ok=True)
    os.makedirs(pdfs_dir, exist_ok=True)

    # DB connection (PostgreSQL / Supabase if DATABASE_URL is set, otherwise SQLite fallback)
    database_url = os.environ.get('DATABASE_URL')
    if database_url:
        if database_url.startswith("postgres://"):
            database_url = database_url.replace("postgres://", "postgresql://", 1)
        # Automatically handle unencoded '@' characters in database passwords
        if database_url.count('@') > 1:
            try:
                import urllib.parse
                scheme, rest = database_url.split('://', 1)
                userinfo, hostpath = rest.rsplit('@', 1)
                if ':' in userinfo:
                    username, password = userinfo.split(':', 1)
                    password_encoded = urllib.parse.quote(password, safe='')
                    database_url = f"{scheme}://{username}:{password_encoded}@{hostpath}"
            except Exception:
                pass
        app.config['SQLALCHEMY_DATABASE_URI'] = database_url
        # Disable prepared statements & enable pre-ping for Supabase PgBouncer pooler compatibility
        app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
            'connect_args': {
                'prepare_threshold': None
            },
            'pool_pre_ping': True,
            'pool_recycle': 300,
        }
    else:
        db_path = os.path.join(base_dir, 'data', 'app.db')
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_path
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    # Generate a strong SECRET_KEY if not provided via env
    secret = os.environ.get('SECRET_KEY')
    if not secret:
        import secrets as _secrets
        secret = _secrets.token_hex(32)
    app.config['SECRET_KEY'] = secret
    # Explicitly disable CSRF (forms are simple and app runs on home network)
    app.config['WTF_CSRF_ENABLED'] = False

    # Load config.yml
    app.config['HOMEHUB_CONFIG'] = load_config()

    # Allow tests to override configuration (database, testing flag, etc.)
    if test_config:
        app.config.update(test_config)

    db.init_app(app)

    # Ensure models are imported before creating tables
    with app.app_context():
        from . import models  # noqa: F401 ensures model metadata is registered
        db.create_all()
        # Perform auto-migrations for both SQLite and PostgreSQL
        # This runs for all databases to ensure schema is up to date
        try:
            from sqlalchemy import inspect, text
            inspector = inspect(db.engine)
            
            def has_column(inspector, table, column):
                try:
                    cols = inspector.get_columns(table)
                    return any(c['name'] == column for c in cols)
                except Exception:
                    return False
            
            def add_column_if_missing(table, column, ddl, default=None):
                if not has_column(inspector, table, column):
                    with db.engine.begin() as conn:
                        conn.execute(text(f"ALTER TABLE {table} ADD COLUMN {ddl}"))
                        if default is not None:
                            conn.execute(text(f"UPDATE {table} SET {column} = :val WHERE {column} IS NULL"), {"val": default})
            
            # Shopping item quantity and unit
            add_column_if_missing('shopping_item', 'quantity', 'REAL DEFAULT 1.0', 1.0)
            add_column_if_missing('shopping_item', 'unit', "VARCHAR(32) DEFAULT 'pcs'", 'pcs')
            
            # Inventory item table (for new installs)
            if not has_column(inspector, 'inventory_item', 'id'):
                with db.engine.begin() as conn:
                    conn.execute(text("""
                        CREATE TABLE IF NOT EXISTS inventory_item (
                            id SERIAL PRIMARY KEY,
                            name VARCHAR(256) NOT NULL,
                            quantity REAL DEFAULT 0.0,
                            unit VARCHAR(32) DEFAULT 'pcs',
                            category VARCHAR(64),
                            location VARCHAR(128),
                            min_quantity REAL DEFAULT 0.0,
                            creator VARCHAR(64),
                            timestamp TIMESTAMP,
                            updated_at TIMESTAMP,
                            tags TEXT DEFAULT '[]'
                        )
                    """))
            
            # Other existing migrations (tags, etc.)
            add_column_if_missing('shopping_item', 'tags', "TEXT DEFAULT '[]'", '[]')
            add_column_if_missing('chore', 'tags', "TEXT DEFAULT '[]'", '[]')
            add_column_if_missing('recipe', 'tags', "TEXT DEFAULT '[]'", '[]')
            add_column_if_missing('chore', 'done', 'BOOLEAN DEFAULT FALSE', False)
            add_column_if_missing('chore', 'due_date', 'due_date DATE', None)
            add_column_if_missing('chore', 'due_time', 'due_time TIME', None)
            add_column_if_missing('chore', 'recurring_id', 'INTEGER', None)
            add_column_if_missing('media', 'status', "VARCHAR(32) DEFAULT 'done'", 'done')
            add_column_if_missing('media', 'progress', 'TEXT', None)
            add_column_if_missing('reminder', 'category', 'VARCHAR(64)', None)
            add_column_if_missing('reminder', 'color', 'VARCHAR(16)', None)
            add_column_if_missing('reminder', 'updated_at', 'TIMESTAMP', None)
            add_column_if_missing('reminder', 'time', 'VARCHAR(5)', None)
            add_column_if_missing('reminder', 'recurring_id', 'INTEGER', None)
            add_column_if_missing('qr_code', 'original_input', 'TEXT', None)
            add_column_if_missing('recurring_expense', 'monthly_mode', "VARCHAR(16) DEFAULT 'day_of_month'", 'day_of_month')
            add_column_if_missing('recurring_expense', 'category', 'VARCHAR(64)', None)
            add_column_if_missing('recurring_expense', 'effective_from', 'DATE', None)
            
# Ensure tables exist
            with db.engine.begin() as conn:
                conn.execute(text("CREATE TABLE IF NOT EXISTS member_status (id SERIAL PRIMARY KEY, name VARCHAR(64), text TEXT, updated_at TIMESTAMP)"))
                conn.execute(text("CREATE TABLE IF NOT EXISTS grocery_history (id SERIAL PRIMARY KEY, item VARCHAR(256), creator VARCHAR(64), timestamp TIMESTAMP)"))
                conn.execute(text("CREATE TABLE IF NOT EXISTS app_setting (key VARCHAR(64) PRIMARY KEY, value TEXT)"))
            
            # Create default users from environment variables if none exist
            # This allows configuring users via Render.com environment variables
            if User.query.count() == 0:
                # Get admin password from environment
                admin_password = os.environ.get('ADMIN_PASSWORD')
                aranya_password = os.environ.get('ARANYA_PASSWORD')
                bidisha_password = os.environ.get('BIDISHA_PASSWORD')  # Note: using BIDISHA_PASSWORD as requested
                
                # Create users if passwords are provided
                users_to_create = []
                
                if admin_password:
                    users_to_create.append(('Admin', admin_password))
                if aranya_password:
                    users_to_create.append(('Aranya', aranya_password))
                if bidisha_password:
                    users_to_create.append(('Bidisha', bidisha_password))
                
                # If no specific passwords provided, create default users with a warning
                # In production, you should always set these via environment variables
                if not users_to_create:
                    app.logger.warning("No user passwords found in environment variables. Creating default users with password 'changeme123' - PLEASE CHANGE IN PRODUCTION!")
                    default_password = 'changeme123'
                    users_to_create = [('Admin', default_password), ('Aranya', default_password), ('Bidisha', default_password)]
                
                # Create the users
                for username, password in users_to_create:
                    user = User(username=username)
                    user.set_password(password)
                    db.session.add(user)
                
                try:
                    db.session.commit()
                    app.logger.info(f"Created {len(users_to_create)} default users from environment variables")
                except Exception as e:
                    db.session.rollback()
                    app.logger.error(f"Failed to create default users: {e}")

        except Exception as e:
            # Log but don't crash on migration errors
            app.logger.warning(f"Auto-migration skipped or failed: {e}")

    from .blueprints import main_bp
    # Register modular route modules to attach endpoints to main_bp
    from .blueprints import auth  # noqa: F401
    from .blueprints import dashboard  # noqa: F401
    from .blueprints import notes  # noqa: F401
    from .blueprints import uploads  # noqa: F401
    from .blueprints import shortener  # noqa: F401
    from .blueprints import shopping  # noqa: F401
    from .blueprints import recipes  # noqa: F401
    from .blueprints import expiry  # noqa: F401
    from .blueprints import media_pdfs  # noqa: F401
    from .blueprints import expenses  # noqa: F401
    from .blueprints import chores  # noqa: F401
    from .blueprints import qr  # noqa: F401
    from .blueprints import weather  # noqa: F401
    from .blueprints import inventory  # noqa: F401
    app.register_blueprint(main_bp)

    @app.context_processor
    def inject_auth_state():
        return {
            'is_authed': bool(session.get('authed'))
        }
    
    # Add Jinja2 filter for JSON parsing
    @app.template_filter('from_json')
    def from_json_filter(s):
        import json
        try:
            return json.loads(s) if s else []
        except (ValueError, TypeError):
            return []

    return app
