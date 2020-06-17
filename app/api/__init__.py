from .resources import UserRegistration, UserLogin, UserLogoutAccess, UserLogoutRefresh, \
    TokenRefresh, SecretResource

def add_resources(api):
    api.add_resource(UserRegistration, '/registration')
    api.add_resource(UserLogin, '/login')
    api.add_resource(UserLogoutAccess, '/logout/access')
    api.add_resource(UserLogoutRefresh, '/logout/refresh')
    api.add_resource(TokenRefresh, '/token/refresh')
    api.add_resource(SecretResource, '/secret')
