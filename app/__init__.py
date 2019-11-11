import datetime
import os
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_security import current_user, login_required, RoleMixin, Security, \
    SQLAlchemyUserDatastore, UserMixin, utils
from flask_uploads import configure_uploads
from flaskext.markdown import Markdown

from .extensions import db, uploaded_images, security, mail, migrate, admin, ckeditor
from .models import User, Role, Post, Tag
from .models.main import UserAdmin, RoleAdmin, PostAdmin # not db tables
from .main.forms import ExtendedRegisterForm

def crash_page(e):
    return render_template('main/500.html'), 500

def page_not_found(e):
    return render_template('main/404.html'), 404

def page_forbidden(e):
    return render_template('main/403.html'), 403


# sort of like an application factory
def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object('settings')
    
    # images
    configure_uploads(app, uploaded_images)
    
    db.init_app(app)
    user_datastore = SQLAlchemyUserDatastore(db, User, Role)
    security.init_app(app, user_datastore, confirm_register_form=ExtendedRegisterForm)
    mail.init_app(app)
    md = Markdown(app, extensions=['fenced_code', 'tables'])
    # migrate.init_app(app, db)
    # Add Flask-Admin views for Users and Roles
    try:
        admin.init_app(app)
        ckeditor.init_app(app)
        admin.add_view(UserAdmin(User, db.session))
        admin.add_view(RoleAdmin(Role, db.session))
        admin.add_view(PostAdmin(Post, db.session))
    except Exception as e:
        pass
        # TODO: log error

    # sentry_sdk.init(dsn="", integrations=[FlaskIntegration()])
    
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    # error handlers
    app.register_error_handler(500, crash_page)
    app.register_error_handler(404, page_not_found)
    app.register_error_handler(403, page_forbidden)
    
    return app


