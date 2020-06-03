"""
WELCOME: communication utilities - app/comms.py
"""
from flask import current_app, render_template, url_for, flash
from flask_mail import Message as FlaskMessage
from . import logger

from .extensions import mail, db

###############################
#####  HELPER FUNCTIONS  ######
###############################

# send text message

# send email
def send_email(recipients, subject, body, **kwargs):
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
