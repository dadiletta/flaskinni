from functools import wraps
import logging
from datetime import datetime, timezone
from flask import flash, redirect, url_for, current_app
from flask_login import current_user
from sqlalchemy.exc import SQLAlchemyError
from typing import Callable

def handle_db_commit(db):
    """
    Decorator for handling database commits and rollbacks safely.
    
    Usage:
        @handle_db_commit(db)
        def my_view():
            user = User(...)
            db.session.add(user)
            # No need to call commit - decorator handles it
    """
    def decorator(f: Callable):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            try:
                result = f(*args, **kwargs)
                db.session.commit()
                return result
            except SQLAlchemyError as e:
                db.session.rollback()
                current_app.logger.error(f"Database error in {f.__name__}: {str(e)}")
                flash('An error occurred while processing your request.', 'error')
                # You might want to add Sentry.io capture here
                raise
        return decorated_function
    return decorator