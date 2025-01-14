"""
The primary purpose of this file is the creation of the Flask application object using
the app factory pattern.
"""

from datetime import datetime, timedelta, timezone
from flask import Flask, render_template, make_response, jsonify, request, current_app
from flask_login import LoginManager, current_user
from flask_principal import identity_loaded, UserNeed, RoleNeed
from werkzeug.local import LocalProxy
from flask_restful import Api
from supabase import create_client, Client

from .extensions import db, mail, migrate, moment, principal
from .utils import Anonymous

# relay for logger
logger = LocalProxy(lambda: current_app.logger)

### Error page handlers
def crash_page(e):
    if 'api' in request.url_root:
        return make_response(jsonify("500 Server error"), 500)
    return render_template('base/500.html'), 500

def page_not_found(e):
    return render_template('base/404.html'), 404

def page_forbidden(e):
    if 'api' in request.url_root:
        return make_response(jsonify("403 Forbidden"), 403)
    return render_template('base/403.html'), 403

def create_app():
    """
    Application factory function that creates and configures a Flask application instance.

    The factory pattern adds flexibility to the application by allowing us to create 
    multiple instances with different configurations. This is especially useful for testing
    and handling different deployment environments (development, production, etc).

    Credit to Miguel Grinberg and his Flask Mega-Tutorial for teaching me this pattern:
    https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world

    Returns:
        Flask: A configured Flask application instance
    """
    # Flask init
    app = Flask(__name__)
    app.config.from_object('settings')

    # Initialize Supabase
    supabase: Client = create_client(
        app.config['SUPABASE_URL'],
        app.config['SUPABASE_SERVICE_KEY']
    )
    app.supabase = supabase

    # Initialize Flask extensions
    db.init_app(app)
    mail.init_app(app)
    migrate.init_app(app, db, compare_type=True)
    moment.init_app(app)
    principal.init_app(app)

    # Initialize Flask-Login
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'base.login'
    login_manager.login_message = 'Please log in to access this page.'
    login_manager.anonymous_user = Anonymous


    # Initialize database and roles
    with app.app_context():
        from .models import Role, User, Post, Tag
        try:
            db.create_all()
            app.logger.info("Database tables created successfully")
        except Exception as e:
            app.logger.error(f"Error creating database tables: {e}")
            raise
        
        # Create default roles if they don't exist
        try:
            admin_role, _ = Role.get_or_create('admin', 'Administrator')
            user_role, _ = Role.get_or_create('end-user', 'End user')
            app.logger.info("Roles initialized successfully")
        except Exception as e:
            app.logger.error(f"Error initializing roles: {e}")
            db.session.rollback()
            raise

        # Create admin users from config
        for email in app.config['STARTING_ADMINS'].split(','):
            if email:
                user = User.query.filter_by(email=email).first()
                if not user:
                    try:
                        user = User.create_with_auth(
                            email=email,
                            password=app.config['STARTING_ADMIN_PASS'],
                            active=True
                        )
                        user.roles.append(admin_role)
                    except Exception as e:
                        app.logger.error(f"Failed to create admin user {email}: {e}")
                        db.session.rollback()
                        continue

        db.session.commit()


    # Register blueprints
    from .base import base_blueprint
    app.register_blueprint(base_blueprint)

    from .api import api_blueprint, add_resources
    restful = Api(api_blueprint, prefix="/api/v1")
    add_resources(restful)
    app.register_blueprint(api_blueprint)

    # Register error handlers
    app.register_error_handler(500, crash_page)
    app.register_error_handler(404, page_not_found)
    app.register_error_handler(403, page_forbidden)


    @identity_loaded.connect_via(app)
    def on_identity_loaded(sender, identity):
        # Set the identity user object
        identity.user = current_user

        # Add the UserNeed to the identity
        if hasattr(current_user, 'id'):
            identity.provides.add(UserNeed(current_user.id))

        # Add each role to the identity
        if hasattr(current_user, 'roles'):
            for role in current_user.roles:
                identity.provides.add(RoleNeed(role.name))

    @login_manager.user_loader
    def load_user(user_id):
        return db.session.get(User, int(user_id))  # Updated to SQLAlchemy 2.0 style

    @app.before_request
    def before_request():
        if current_user.is_authenticated:
            first_time = True if not current_user.last_seen else False
            if current_user.last_seen is None or \
                datetime.now(timezone.utc) - current_user.last_seen > timedelta(hours=1):
                current_user.last_seen = datetime.now(timezone.utc)
                db.session.commit()

    return app