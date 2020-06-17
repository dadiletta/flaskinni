from flask_restful import Resource, reqparse
from ..models import User, RevokedTokenModel
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, \
    jwt_refresh_token_required, get_jwt_identity, get_raw_jwt

parser = reqparse.RequestParser()
parser.add_argument('username', help = 'This field cannot be blank', required = True)
parser.add_argument('password', help = 'This field cannot be blank', required = True)


class UserAPI(Resource):
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


class UserLogin(Resource):
    def post(self):
        data = parser.parse_args()
        current_user = User.query.filter_by(email=data['username']).first()

        if not current_user:
            return {'message': 'User {} doesn\'t exist'.format(data['username'])}
        
        # TODO: Use flask-security utils to verity hash
        if False: # UserModel.verify_hash(data['password'], current_user.password):
            access_token = create_access_token(identity = data['username'])
            refresh_token = create_refresh_token(identity = data['username'])
            return {
                'message': 'Logged in as {}'.format(current_user.username),
                'access_token': access_token,
                'refresh_token': refresh_token
                }
        else:
            return {'message': 'Wrong credentials'}


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


class TokenRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        current_user = get_jwt_identity()
        access_token = create_access_token(identity = current_user)
        return {'access_token': access_token}


class SecretResource(Resource):
    @jwt_required
    def get(self):
        return {
            'answer': 42
        }
