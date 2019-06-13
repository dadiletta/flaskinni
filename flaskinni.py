import os
from dotenv import load_dotenv
from flask_security import utils

# TODO: Include an explanitory link for reference
dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

import sys
import click
from datetime import datetime
from flask_migrate import Migrate, upgrade
from app import create_app, db, user_datastore
from app.main.models import User, Role, Post, Tag

app = create_app(os.getenv('FLASK_CONFIG') or 'settings')
migrate = Migrate(app, db)


@app.shell_context_processor
def make_shell_context():
    return dict(db=db, User=User, Role=Role)

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
    encrypted_password = utils.encrypt_password(app.config['STARTING_ADMIN_PASS'])
    if not user_datastore.get_user(app.config['STARTING_ADMIN1']):
        user_datastore.create_user(email=app.config['STARTING_ADMIN1'], password=encrypted_password)
    if not user_datastore.get_user(app.config['STARTING_ADMIN2']):
        user_datastore.create_user(email=app.config['STARTING_ADMIN2'], password=encrypted_password)
        

    # Commit any database changes; the User and Roles must exist before we can add a Role to the User
    db.session.commit()

    # Give one User has the "end-user" role, while the other has the "admin" role. (This will have no effect if the
    # Users already have these Roles.) Again, commit any database changes.
    user_datastore.add_role_to_user(app.config['STARTING_ADMIN1'], 'admin')
    confirmed_admin = user_datastore.get_user(app.config['STARTING_ADMIN1'])
    confirmed_admin.confirmed_at = datetime.utcnow()

    user_datastore.add_role_to_user(app.config['STARTING_ADMIN2'], 'admin')
    confirmed_admin = user_datastore.get_user(app.config['STARTING_ADMIN2'])
    confirmed_admin.confirmed_at = datetime.utcnow()

    db.session.commit()

'''
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
'''
