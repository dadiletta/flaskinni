"""
The primary purpose of this page is an `app factory <https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-xv-a-better-application-structure>`_. 

"""

from datetime import datetime
from flask import Flask, render_template, make_response, jsonify, request
from flask_security import current_user, SQLAlchemySessionUserDatastore, utils
from flaskext.markdown import Markdown
from flask_restful import Api

from .extensions import db, security, mail, migrate, admin, \
    moment, jwt
from .base.forms import ExtendedRegisterForm


### Error page tools to use in the factor below
def crash_page(e):
    if 'api' in request.url_root:
        return make_response(jsonify("500 Server error"), 500)
    return render_template('base/500.html'), 500

def page_not_found(e):
    return render_template('base/404.html'), 404

def page_forbidden(e):
    if 'api' in request.url_root: # I wish this worked
        return make_response(jsonify("403 Forbidden"), 403)
    return render_template('base/403.html'), 403

###### FACTORY ##
def create_app(config_name):
    """ Application factory: Assembles and returns clones of your app """
    # Flask init
    app = Flask(__name__) # most of the work done right here. Thanks, Flask!
    app.config.from_object('settings') # load my settings which pull from .env
    
    ''' 
    FLASK EXTENTIONS
    '''
    db.init_app(app) # load my database extension
    from .models import User, Role, Post, Buzz, UserAdmin, BaseAdmin # not db tables
    user_datastore = SQLAlchemySessionUserDatastore(db.session, User, Role)
    # load my security extension
    security.init_app(app, user_datastore, confirm_register_form=ExtendedRegisterForm)
    mail.init_app(app) # load my mail extensioin 
    # load my writing tool extension 
    md = Markdown(app, extensions=['fenced_code', 'tables'])
    migrate.init_app(app, db) # load my database updater tool
    moment.init_app(app) # time formatting
    jwt.init_app(app)   


    admin.init_app(app)
    # FLASKINNI'S BASE OBJECTS
    admin.add_view(UserAdmin(User, db.session, endpoint='user_admin', menu_icon_type='fa', menu_icon_value='fa-user-circle'))
    admin.add_view(BaseAdmin(Post, db.session, endpoint='post_admin', menu_icon_type='fa', menu_icon_value='fa-file-text')) 
    # don't really need admin views of these objects
    # admin.add_view(BaseAdmin(Role, db.session))
    # admin.add_view(BaseAdmin(Buzz, db.session))
    
    # TODO: Add your models below so you can manage data from Flask-Admin's convenient tools



    # TODO: Setup sentry.io!
    # sentry_sdk.init(dsn="", integrations=[FlaskIntegration()])
    
    # activate the flaskinni blueprint (blog, user settings, and other basic routes)
    from .base import base_blueprint
    app.register_blueprint(base_blueprint)

    # activate API blueprint: https://stackoverflow.com/questions/38448618/using-flask-restful-as-a-blueprint-in-large-application
    from .api import api_blueprint, add_resources   
    restful = Api(api_blueprint, prefix="/api/v1") 
    add_resources(restful)
    app.register_blueprint(api_blueprint) # registering the blueprint effectively runs init_app on the restful extension

    # Callback function to check if a JWT exists in the redis blocklist
    @jwt.token_in_blocklist_loader
    def check_if_token_is_revoked(jwt_header, jwt_payload):
        jti = jwt_payload["jti"]
        return models.RevokedTokenModel.is_jti_blocklisted(jti)

    # --- NEW BLUEPRINTS GO BELOW THIS LINE ---
    # TODO: Add your own blueprint 

    # custom error handlers, these call the functions at the top of the file
    app.register_error_handler(500, crash_page)
    app.register_error_handler(404, page_not_found)
    app.register_error_handler(403, page_forbidden)


    # Executes before the first request is processed.
    @app.before_first_request
    def before_first_request():
        """ Before the first run, we assure the database is built and admin access is secure.  """

        # Create any database tables that don't exist yet.
        db.create_all()

        # Create the Roles "admin" and "end-user" -- unless they already exist
        user_datastore.find_or_create_role(name='admin', description='Administrator')
        user_datastore.find_or_create_role(name='end-user', description='End user')

        # Create two Users for testing purposes -- unless they already exists.
        # In each case, use Flask-Security utility function to encrypt the password.
        encrypted_password = utils.hash_password(app.config['STARTING_ADMIN_PASS'])

        for email in app.config['STARTING_ADMINS']:
            if not user_datastore.find_user(email=email):
                user_datastore.create_user(email=email, password=encrypted_password)
       

        # Commit any database changes; the User and Roles must exist before we can add a Role to the User
        db.session.commit()

        for email in app.config['STARTING_ADMINS']:
            confirmed_admin = user_datastore.find_user(email=email)
            confirmed_admin.confirmed_at = datetime.utcnow()
            user_datastore.add_role_to_user(confirmed_admin, 'admin')

        db.session.commit()

        
    @app.before_request
    def before_request():
        """ What we do before every single handled request """
        if current_user.is_authenticated:
            first_time = True if not current_user.last_seen else False
            current_user.last_seen = datetime.utcnow()
            db.session.commit()

    return app


