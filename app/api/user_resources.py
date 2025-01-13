from flask import current_app, request
from flask_restful import Resource, reqparse
from ..models import User
from ..extensions import db
from functools import wraps

# Supabase Auth Decorator
def supabase_auth_required():
    def wrapper(fn):
        @wraps(fn)
        def decorated_view(*args, **kwargs):
            # Get the Authorization header
            auth_header = request.headers.get('Authorization')
            if not auth_header or not auth_header.startswith('Bearer '):
                return {'message': 'Missing or invalid authentication token'}, 401
            
            # The actual token validation happens on Supabase's end
            # Here we just need to verify the token was passed correctly
            # Supabase handles the heavy lifting of JWT validation
            return fn(*args, **kwargs)
        return decorated_view
    return wrapper

class UserAPI(Resource):
    def get(self):
        """Get user profile information"""
        @supabase_auth_required()
        def get_profile():
            # The user's Supabase ID will be in their JWT
            # You can extract it from request.headers if needed
            try:
                user_email = request.headers.get('X-Supabase-User-Email')
                user = User.query.filter_by(email=user_email).first()
                if not user:
                    return {'message': 'User not found'}, 404
                return {
                    'email': user.email,
                    'profile': user.profile  # whatever user data you want to return
                }
            except Exception as e:
                current_app.logger.error(f"Failed to get user profile: {e}")
                return {'message': 'Internal server error'}, 500
        return get_profile()

class SecretResource(Resource):
    @supabase_auth_required()
    def get(self):
        return {
            'answer': 42
        }

    @supabase_auth_required()
    def post(self):
        return {
            'test': 99
        }

    @supabase_auth_required()
    def put(self):
        parser = reqparse.RequestParser()
        parser.add_argument('test', type=int, required=True,
                          help='Test value required')
        data = parser.parse_args()
        return {'message': f'Received: {data}'}