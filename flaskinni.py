"""
Flaskinni's Launcher
=====================
This module spits out instances of our app. 
"""

import os # give me tools to get my own IP and manage my computer
import logging
from dotenv import load_dotenv # connect me with any .env files
from flask_migrate import Migrate, upgrade # database updater

from app import create_app, db  # load my app factory

#: Pulls in `environmental variables <https://github.com/theskumar/python-dotenv>`_. 
dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

#: triggers app factory
app = create_app(os.getenv('FLASK_CONFIG') or 'settings') 
migrate = Migrate(app, db) # activate my database upgrader tool

# activate logging
# setup logging config
from logging.config import dictConfig

dictConfig({
    'version': 1,
    'formatters': {'default': {
        'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
    }},
    'handlers': {'wsgi': {
        'class': 'logging.StreamHandler',
        'stream': 'ext://flask.logging.wsgi_errors_stream',
        'formatter': 'default'
    }},
    'root': {
        'level': 'INFO',
        'handlers': ['wsgi']
    }
})
root_path = str(os.path.abspath((os.path.dirname(__file__))))
handler = logging.FileHandler(root_path + '/errors.log', mode='a', encoding=None, delay=False)  # errors logged to this file
app.logger.setLevel(logging.INFO)
app.logger.addHandler(handler)  # attach the handler to the app's logger
app.logger.info('App started.')


# if I talk to my app through CLI, pre-load some stuff
@app.shell_context_processor
def make_shell_context():
    from app.models import User, Role
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
