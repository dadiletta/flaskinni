from flask import Blueprint

from .resources import UserRegistrationAPI, UserLogin, UserLogoutAccess, UserLogoutRefresh, \
    TokenRefresh, SecretResource

api_blueprint = Blueprint('api_blueprint', __name__)


def add_resources(api):
    """ API ROUTE INIT """
    api.add_resource(UserRegistrationAPI, '/registration')
    api.add_resource(UserLogin, '/login')
    api.add_resource(UserLogoutAccess, '/logout/access')
    api.add_resource(UserLogoutRefresh, '/logout/refresh')
    api.add_resource(TokenRefresh, '/token/refresh')
    api.add_resource(SecretResource, '/secret') # our first challenge
