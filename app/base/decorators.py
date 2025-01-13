from functools import wraps
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
                # TODO: add Sentry.io capture here
                raise
        return decorated_function
    return decorator

def roles_required(*roles: str) -> Callable:
    """
    Decorator that specifies that ALL specified roles are required to access a view.
    
    This decorator should be used when a user must have ALL of the specified roles.
    It's more restrictive than roles_accepted.
    
    Args:
        *roles: Variable number of role names required for access.
               All roles must be present for access to be granted.
    
    Returns:
        Callable: A decorator that checks for required roles.
    
    Usage:
        @app.route('/admin')
        @roles_required('admin', 'supervisor')
        def admin_view():
            # User must have BOTH admin AND supervisor roles
            return 'Admin view'
    
    Raises:
        Redirects to index with flash message if authentication fails
    """
    def wrapper(fn: Callable) -> Callable:
        @wraps(fn)
        def decorated_view(*args, **kwargs):
            if not current_user.is_authenticated:
                flash('Please log in to access this page.', 'warning')
                return redirect(url_for('base.login'))
            
            user_roles = {role.name for role in getattr(current_user, 'roles', [])}
            required_roles = set(roles)
            
            if not required_roles.issubset(user_roles):
                missing_roles = required_roles - user_roles
                current_app.logger.warning(
                    f"User {current_user.id} attempted to access {fn.__name__} "
                    f"but lacks required roles: {missing_roles}"
                )
                flash('You do not have permission to access this resource.', 'danger')
                return redirect(url_for('base.index'))
                
            return fn(*args, **kwargs)
        return decorated_view
    return wrapper

def roles_accepted(*roles: str) -> Callable:
    """
    Decorator that specifies that ANY of the specified roles are acceptable.
    
    This decorator should be used when a user only needs ONE of the specified roles.
    It's less restrictive than roles_required.
    
    Args:
        *roles: Variable number of role names, any of which grants access.
               Only one role needs to match for access to be granted.
    
    Returns:
        Callable: A decorator that checks for accepted roles.
    
    Usage:
        @app.route('/dashboard')
        @roles_accepted('editor', 'author', 'admin')
        def dashboard():
            # User needs only ONE of: editor OR author OR admin role
            return 'Dashboard'
    
    Raises:
        Redirects to index with flash message if authentication fails
    """
    def wrapper(fn: Callable) -> Callable:
        @wraps(fn)
        def decorated_view(*args, **kwargs):
            if not current_user.is_authenticated:
                flash('Please log in to access this page.', 'warning')
                return redirect(url_for('base.login'))
            
            user_roles = {role.name for role in getattr(current_user, 'roles', [])}
            
            if not any(role in user_roles for role in roles):
                current_app.logger.warning(
                    f"User {current_user.id} attempted to access {fn.__name__} "
                    f"but has none of the accepted roles: {roles}"
                )
                flash('You do not have permission to access this resource.', 'danger')
                return redirect(url_for('base.index'))
                
            return fn(*args, **kwargs)
        return decorated_view
    return wrapper