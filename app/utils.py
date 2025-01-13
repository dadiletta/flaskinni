# app/utils.py
"""
Utility Classes
==============
Helper classes that assist our models but don't represent database tables.
These can be safely imported at app initialization without circular dependencies.
"""

from flask_login import AnonymousUserMixin

class Anonymous(AnonymousUserMixin):
    """
    Extended Anonymous User that supports the same interfaces as our User model.
    This allows templates and other code to safely call methods like has_role()
    even when no user is logged in.
    """
    def has_role(self, *args):
        """Always returns False for anonymous users"""
        return False
        
    def is_admin(self):
        """Always returns False for anonymous users"""
        return False
    
    @property
    def roles(self):
        """Returns empty list for anonymous users"""
        return []