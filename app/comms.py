"""
WELCOME: communication utilities - app/comms.py
"""
from flask import current_app, render_template, url_for
from flask_mail import Message as FlaskMessage
from flask_security import current_user
from werkzeug.local import LocalProxy

from .models import Buzz
from .extensions import mail, db

logger = LocalProxy(lambda: current_app.logger)

###############################
#####  HELPER FUNCTIONS  ######
###############################
def send_email(recipients, subject, body, **kwargs):
    """ Generates a Flask-Mail object and sends """
    msg = FlaskMessage(subject, recipients=recipients)
    msg.body = body
    if kwargs.get('html', False):
        msg.html = kwargs['html']
    if kwargs.get('cc', False):
        msg.cc = kwargs['cc']
    try:
        with current_app.app_context():
            mail.send(msg)
    except Exception as e:
        logger.error("Error sending email: " + str(e))

def log_buzz(title, body, **kwargs):
    """ Generates a buzz object """
    try:
        buzz = Buzz(title=title, body=body)
        if current_user.is_authenticated:
            buzz.user_id = current_user.id
        db.session.add(buzz)
        logger.info(f"Buzzed: {buzz.title}")
    except Exception as e:
        logger.error(f"Error while buzzing: {e}")

# TODO: send a text message using Twilio 
