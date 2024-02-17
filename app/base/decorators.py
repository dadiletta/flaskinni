from functools import wraps
import logging
from sqlalchemy.exc import SQLAlchemyError

def handle_db_commit(db):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            try:
                result = f(*args, **kwargs)
                db.session.commit()
                return result
            except SQLAlchemyError as e:
                db.session.rollback()
                logging.error(f"Database error: {e}")
                # TODO: Add a 500 error page
                # TODO: Sentry.io integration
                # You might want to re-raise the exception after logging it
                # so that the error can be handled further up the stack.
                raise
        return decorated_function
    return decorator