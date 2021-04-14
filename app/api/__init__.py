from flask import Blueprint
api_blueprint = Blueprint('api_blueprint', __name__)

from .user_resources import UserRegistrationAPI, UserLoginAPI, UserLogoutAccess, UserLogoutRefresh, \
    TokenRefresh, SecretResource


def add_resources(api):
    """ API ROUTE INIT """
    api.add_resource(UserRegistrationAPI, '/registration')
    api.add_resource(UserLoginAPI, '/login')
    api.add_resource(UserLogoutAccess, '/logout/access')
    api.add_resource(UserLogoutRefresh, '/logout/refresh')
    api.add_resource(TokenRefresh, '/token/refresh')
    api.add_resource(SecretResource, '/secret') # super fun test routes

