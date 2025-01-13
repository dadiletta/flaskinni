from flask import Blueprint
api_blueprint = Blueprint('api_blueprint', __name__)

from .user_resources import UserAPI, SecretResource

def add_resources(api):
    """ API ROUTE INIT """
    # User profile operations
    api.add_resource(UserAPI, '/user')
    
    # Test/protected routes
    api.add_resource(SecretResource, '/secret')

    # Note: Registration, login, logout, and token refresh 
    # are now handled by Supabase's authentication system