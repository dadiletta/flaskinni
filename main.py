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


root_path = str(os.path.abspath((os.path.dirname(__file__))))
handler = logging.FileHandler(root_path + '/errors.log', mode='a', encoding=None, delay=False)  # errors logged to this file
app.logger.setLevel(logging.INFO)
app.logger.addHandler(handler)  # attach the handler to the app's logger
gunicorn_logger = logging.getLogger('gunicorn.error')
app.logger.handlers = gunicorn_logger.handlers
app.logger.setLevel(gunicorn_logger.level)
app.logger.info('App started.')


# if I talk to my app through CLI, pre-load some stuff
@app.shell_context_processor
def make_shell_context():
    from app.models import User, Role
    return dict(db=db, User=User, Role=Role)
