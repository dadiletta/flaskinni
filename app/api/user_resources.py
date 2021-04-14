from flask import current_app
from flask_restful import Resource, reqparse
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, \
    get_jwt_identity, get_jwt
from flask_security import utils

from ..models import User, RevokedTokenModel
from ..extensions import security, db


# HELPER
_user_parser = reqparse.RequestParser()
_user_parser.add_argument('email',
                          type=str,
                          required=True,
                          help="This field cannot be blank."
                          )
_user_parser.add_argument('password',
                          type=str,
                          required=True,
                          help="This field cannot be blank."
                          )



# /registration
class UserRegistrationAPI(Resource):

    def post(self):
        data = _user_parser.parse_args()
        
        if User.query.filter_by(email=data['email']).first():
            return {'message': f"User {data['email']} already exists"}
        
        encrypted_password = utils.encrypt_password(data['password'])
        # TODO: verify email address format
        security.datastore.create_user(email=data['email'], password=encrypted_password)
        db.session.commit()
        
        try:
            # save the new user
            access_token = create_access_token(identity = data['email'])
            refresh_token = create_refresh_token(identity = data['email'])
            return {
                'message': 'User {} was created'.format(data['email']),
                'access_token': access_token,
                'refresh_token': refresh_token
                }
        except:
            return {'message': 'Something went wrong'}, 500


# /login
class UserLoginAPI(Resource):

    def post(self):
        data = _user_parser.parse_args()
        current_user = None
        try:         
            current_user = User.query.filter_by(email=data['email']).first()
        except Exception as e:
            current_app.logger.error(f"Failed to query for user: {data}")

        if not current_user:
            return {'message': 'User {} doesn\'t exist'.format(data['email'])}
        
        if utils.verify_password(data['password'], current_user.password): # UserModel.verify_hash(data['password'], current_user.password):
            access_token = create_access_token(identity = data['email'])
            refresh_token = create_refresh_token(identity = data['email'])
            return {
                'message': 'Logged in as {}'.format(current_user.email),
                'access_token': access_token,
                'refresh_token': refresh_token
                }
        else:
            return {'message': f"Wrong credentials: {current_user}"}


# /logout/access
class UserLogoutAccess(Resource):
    @jwt_required()
    def post(self):
        jti = get_jwt()['jti']
        try:
            revoked_token = RevokedTokenModel(jti = jti)
            revoked_token.add()
            return {'message': 'Access token has been revoked'}
        except:
            return {'message': 'Something went wrong'}, 500


# /logout/refresh
class UserLogoutRefresh(Resource):
    @jwt_required(refresh=True)
    def post(self):
        jti = get_jwt()['jti']
        try:
            revoked_token = RevokedTokenModel(jti = jti)
            revoked_token.add()
            return {'message': 'Refresh token has been revoked'}
        except:
            return {'message': 'Something went wrong'}, 500


# /token/refresh
class TokenRefresh(Resource):
    @jwt_required(refresh=True)
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
    
    @jwt_required()
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
