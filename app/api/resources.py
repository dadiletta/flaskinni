from flask import current_app
from flask_restful import Resource, reqparse
'''
from ..models import User, RevokedTokenModel
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, \
    jwt_refresh_token_required, get_jwt_identity, get_raw_jwt


# /registration
class UserRegistrationAPI(Resource):
    def __init__(self):
        # Add payload requirements / expectations: https://blog.miguelgrinberg.com/post/designing-a-restful-api-using-flask-restful
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('username', type = str, required = True,\
                help = 'No username provided', location = 'json')
        self.reqparse.add_argument('password', type = str, required = True,\
                help = 'No password provided', location = 'json')                
        super(UserRegistration, self).__init__()

    def post(self):
        data = parser.parse_args()
        
        if User.query.filter_by(email=data['username']).first():
            return {'message': 'User {} already exists'.format(data['username'])}
        
        new_user = "Make a new user here."
        
        try:
            # save the new user
            access_token = create_access_token(identity = data['username'])
            refresh_token = create_refresh_token(identity = data['username'])
            return {
                'message': 'User {} was created'.format(data['username']),
                'access_token': access_token,
                'refresh_token': refresh_token
                }
        except:
            return {'message': 'Something went wrong'}, 500


# /login
class UserLoginAPI(Resource):
    def __init__(self):
        # Add payload requirements / expectations: https://blog.miguelgrinberg.com/post/designing-a-restful-api-using-flask-restful
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('username', type = str, required = True,\
                help = 'No username provided')
        self.reqparse.add_argument('password', type = str, required = True,\
                help = 'No password provided')                
        super(UserLoginAPI, self).__init__()

    def post(self):
        data = self.reqparse.parse_args()
        current_user = None
        try:         
            current_user = User.query.filter_by(email=data['username']).first()
        except Exception as e:
            current_app.logger.error(f"Failed to query for user: {data}")

        if not current_user:
            return {'message': 'User {} doesn\'t exist'.format(data['username'])}
        
        # TODO: Use flask-security utils to verity hash
        if User.verify_hash(data['password'], current_user.password): # UserModel.verify_hash(data['password'], current_user.password):
            access_token = create_access_token(identity = data['username'])
            refresh_token = create_refresh_token(identity = data['username'])
            return {
                'message': 'Logged in as {}'.format(current_user.email),
                'access_token': access_token,
                'refresh_token': refresh_token
                }
        else:
            return {'message': f"Wrong credentials: {data['password']} -VS- {User.generate_hash(data['password'])} -vs- {current_user.password}"}


# /logout/access
class UserLogoutAccess(Resource):
    @jwt_required
    def post(self):
        jti = get_raw_jwt()['jti']
        try:
            revoked_token = RevokedTokenModel(jti = jti)
            revoked_token.add()
            return {'message': 'Access token has been revoked'}
        except:
            return {'message': 'Something went wrong'}, 500


# /logout/refresh
class UserLogoutRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        jti = get_raw_jwt()['jti']
        try:
            revoked_token = RevokedTokenModel(jti = jti)
            revoked_token.add()
            return {'message': 'Refresh token has been revoked'}
        except:
            return {'message': 'Something went wrong'}, 500


# /token/refresh
class TokenRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        current_user = get_jwt_identity()
        access_token = create_access_token(identity = current_user)
        return {'access_token': access_token}


# /secret
class SecretResource(Resource):
    def __init__(self):
        # Add payload requirements / expectations: https://blog.miguelgrinberg.com/post/designing-a-restful-api-using-flask-restful
        self.reqparse = reqparse.RequestParser()    
        self.reqparse.add_argument('test', type=int, help='Rate to charge for this resource')           
        super(SecretResource, self).__init__()    
    
    @jwt_required
    def get(self):
        return {
            'answer': 42
        }

    def post(self):
        return {
            'test': 99
        }

    def put(self):
        data = self.reqparse.parse_args()
        return {'message123': f'{data}'}

'''