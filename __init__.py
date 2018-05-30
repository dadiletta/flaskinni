# Example of combining Flask-Security and Flask-Admin.
# by Steve Saporta
# April 15, 2014
#
# Uses Flask-Security to control access to the application, with "admin" and "end-user" roles.
# Uses Flask-Admin to provide an admin UI for the lists of users and roles.
# SQLAlchemy ORM, Flask-Mail and WTForms are used in supporting roles, as well.

from flask import Flask, render_template, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_security import current_user, login_required, RoleMixin, Security, \
    SQLAlchemyUserDatastore, UserMixin, utils
from flask_uploads import configure_uploads
from flaskext.markdown import Markdown
from extensions import db, uploaded_images
from user.models import User, Role, UserAdmin, RoleAdmin, PostAdmin
from user.forms import ExtendedRegisterForm
from inni.models import Post
import os
import datetime
import private

# sort of like an application factory
def register_extensions(app):
    from extensions import security, mail, migrate, admin, ckeditor
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

# Initialize Flask and set some config values
app = Flask(__name__)
app.config.from_object('settings')
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
register_extensions(app)
# images
configure_uploads(app, uploaded_images)

################
# CUSTOM FILTERS
# Example:
# https://stackoverflow.com/questions/19394844/how-to-get-the-user-object-from-the-user-key-in-flask-template
def get_user_by_user_key(user_key):
    # your logic code here, e.g.
    user = user_datastore.find_user(id=user_key)
    if user.first_name:
        return user.first_name + " " + user.last_name
    else:
        return "Anonymous"

app.jinja_env.filters['get_name_by_key'] = get_user_by_user_key

############
# APP ROUTES
from inni.views import *

# Executes before the first request is processed.
@app.before_first_request
def before_first_request():

    # Create any database tables that don't exist yet.
    db.create_all()

    # Create the Roles "admin" and "end-user" -- unless they already exist
    user_datastore.find_or_create_role(name='admin', description='Administrator')
    user_datastore.find_or_create_role(name='end-user', description='End user')

    # Create two Users for testing purposes -- unless they already exists.
    # In each case, use Flask-Security utility function to encrypt the password.
    encrypted_password = utils.encrypt_password(private.STARTING_ADMIN_PASS)
    if not user_datastore.get_user(private.STARTING_ADMIN1):
        user_datastore.create_user(email=private.STARTING_ADMIN1, password=encrypted_password)
    if not user_datastore.get_user(private.STARTING_ADMIN2):
        user_datastore.create_user(email=private.STARTING_ADMIN2, password=encrypted_password)
        

    # Commit any database changes; the User and Roles must exist before we can add a Role to the User
    db.session.commit()

    # Give one User has the "end-user" role, while the other has the "admin" role. (This will have no effect if the
    # Users already have these Roles.) Again, commit any database changes.
    user_datastore.add_role_to_user(private.STARTING_ADMIN1, 'admin')
    confirmed_admin = user_datastore.get_user(private.STARTING_ADMIN1)
    confirmed_admin.confirmed_at = datetime.datetime.utcnow()

    user_datastore.add_role_to_user(private.STARTING_ADMIN2, 'admin')
    confirmed_admin = user_datastore.get_user(private.STARTING_ADMIN2)
    confirmed_admin.confirmed_at = datetime.datetime.utcnow()

    db.session.commit()

# to avoid reload issues on CSS updates
# http://flask.pocoo.org/snippets/40/
@app.context_processor
def override_url_for():
    return dict(url_for=dated_url_for)

def dated_url_for(endpoint, **values):
    if endpoint == 'static':
        filename = values.get('filename', None)
        if filename:
            file_path = os.path.join(app.root_path,
                                     endpoint, filename)
            values['q'] = int(os.stat(file_path).st_mtime)
    return url_for(endpoint, **values)
    

# If running locally, listen on all IP addresses, port 8080
if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=int('8080'),
        debug=app.config['DEBUG']
    )
