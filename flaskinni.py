import os # give me tools to get my own IP and manage my computer
from dotenv import load_dotenv # connect me with any .env files
from flask_security import utils # a tool to encrypt passwords

# TODO: Include an explanitory link for reference
dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

import sys
import click # this lets me use "flask ..." commands
from datetime import datetime # the time
from flask_migrate import Migrate, upgrade # database updater
from app import create_app, db  # load my app factory
from app.models import User, Role, Post, Tag # get my local objects

app = create_app(os.getenv('FLASK_CONFIG') or 'settings') # triggers app factory
migrate = Migrate(app, db) # activate my database upgrader tool

# if I talk to my app through CLI, pre-load some stuff
@app.shell_context_processor
def make_shell_context():
    # TODO: proper imports
    return dict(db=db, User=User, Role=Role)

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
