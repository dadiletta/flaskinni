import datetime
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_security import current_user, login_required, RoleMixin, Security, \
    SQLAlchemyUserDatastore, UserMixin, utils
from flask_uploads import configure_uploads
from flaskext.markdown import Markdown

from .extensions import db, uploaded_images, security, mail, migrate, admin, ckeditor
from .main.models import User, Role, UserAdmin, RoleAdmin, PostAdmin, Post
from .main.forms import ExtendedRegisterForm

user_datastore = SQLAlchemyUserDatastore(db, User, Role)

# sort of like an application factory
def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object('settings')
    
    # images
    configure_uploads(app, uploaded_images)
    
    db.init_app(app)
    security.init_app(app, user_datastore, confirm_register_form=ExtendedRegisterForm)
    mail.init_app(app)
    md = Markdown(app, extensions=['fenced_code', 'tables'])
    # migrate.init_app(app, db)
    # Add Flask-Admin views for Users and Roles
    admin.init_app(app)
    ckeditor.init_app(app)
    admin.add_view(UserAdmin(User, db.session))
    admin.add_view(RoleAdmin(Role, db.session))
    admin.add_view(PostAdmin(Post, db.session))
    
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)
    
    return app


