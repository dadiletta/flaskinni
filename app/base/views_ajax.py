"""
AJAX Endpoints
================
These are methods that handle AJAX request and don't return a rendered template
"""
from flask import url_for, session, request, current_app, jsonify


from datetime import datetime, timezone
from flask_login import login_required, current_user
from ..extensions import db, moment
from . import base_blueprint as app
from .forms import BuzzForm
from .. import comms

###############################
####### AJAX HANDLERS #########
###############################

@app.route('/api/current-time')
def get_current_time():
    """Return the current UTC time formatted in a human-readable way.
    
    Returns:
        Response: JSONified response containing formatted timestamp
    """
    current_time = datetime.now(timezone.utc)
    return jsonify({
        'timestamp': moment.create(current_time).format('LLLL'),
        'utc_timestamp': current_time.isoformat()
    })

@app.route('/togglesidebar', methods=['POST'])
def toggle_sidebar():
    """AJAX handler that updates session cookie to store user's preference about sidebar

    Returns:
        Reponse: JSONified notification on the current value of `session['toggled']`
    """
    if not 'toggled' in session.keys():
        session['toggled'] = True
    else:
        session['toggled'] = not session['toggled']
    return jsonify({'success' : 'toggle now %r' % session['toggled']})

@app.route('/buzz/create', methods=['POST'])
@login_required  # Ensure only logged-in users can create events
def create_buzz():
    """AJAX handler for creating a new Buzz event.
    
    Expects JSON data containing the Buzz event details.
    Returns:
        Response: JSONified response with success/error message and the created event data
    """
    form = BuzzForm()
    
    if form.validate_on_submit():
        try:
            buzz = Buzz(
                title=form.title.data,
                content=form.content.data,
                created_by=current_user,
                created_at=datetime.utcnow()
            )
            
            db.session.add(buzz)
            db.session.commit()
            
            return jsonify({
                'success': True,
                'message': 'Buzz event created successfully',
                'buzz': {
                    'id': buzz.id,
                    'title': buzz.title,
                    'content': buzz.content,
                    'created_at': moment.create(buzz.created_at).format('LLLL'),
                    'creator': current_user.name
                }
            }), 201
            
        except Exception as e:
            db.session.rollback()
            return jsonify({
                'success': False,
                'message': f'Error creating Buzz event: {str(e)}'
            }), 500
    
    return jsonify({
        'success': False,
        'message': 'Validation failed',
        'errors': form.errors
    }), 400