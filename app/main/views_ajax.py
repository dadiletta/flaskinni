"""
WELCOME: ajax business logic - flaskinni/app/main/views_ajax.py
These are methods that handle AJAX request and don't return a rendered template
"""
from flask import render_template, redirect, flash, url_for, session, request, current_app, jsonify
from flask_security.forms import RegisterForm
from flask_security import login_required, roles_required, current_user, roles_accepted
from flask_mail import Message as FlaskMessage
from slugify import slugify
from datetime import datetime

from ..extensions import db, uploaded_images, mail, moment
from ..models import Program, School, Path, Membership, Log, Message, Assignment, User, Role
from .forms import MessageForm, LogForm, RevisionForm
from ..main.forms import EditUser

###############################
####### AJAX HANDLERS #########
###############################

@app.route('/whattimeisit')
def what_time_is_it():
    return jsonify({'timestamp': moment.create(datetime.utcnow()).format('LLLL')})


'''
# EXAMPLE
@app.route('/message/seen_on', methods=['POST'])
@login_required
def mark_seen():
    message_id = int(request.form['message_id'])
    message = Message.query.get(message_id)	
    if message and current_user.id == message.recipient_id and not message.seen_on:
        message.seen_on = datetime.utcnow()
        db.session.add(message)
        db.session.commit()
        return jsonify({'success' : 'Message now seen'})
    return jsonify({'error' : 'message not updated'})

'''