# Set the path
import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
import sqlalchemy
import private
#from flask import g
from flask import Flask
from extensions import db, security, mail, migrate, admin
from flask_sqlalchemy import SQLAlchemy
from flask_testing import TestCase
from flask_security import current_user, login_required, RoleMixin, Security, \
    SQLAlchemyUserDatastore, UserMixin, utils
from flask_uploads import configure_uploads
from flaskext.markdown import Markdown

# from extensions import db, security, admin

# need to add all models for db.create_all to work
from user.models import *
from blog.models import *

class PapaTest(TestCase):
    
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://%s:%s@%s/' % (private.DB_USERNAME, private.DB_PASSWORD, app.config['DB_HOST'])
    TESTING = True
    
    def create_app(self):
        # THIS NEEDS TO MIRROR YOUR __init__.py's APP INSTANTIATION
        # ... or whatever you need to setup the right test environment
        from flaskinni import app
        app.config.from_object('settings')
        user_datastore = SQLAlchemyUserDatastore(db, User, Role)
        register_extensions(app)
        # images
        configure_uploads(app, uploaded_images)
        # sort of like an application factory
        db.init_app(app)
        security.init_app(app, user_datastore, confirm_register_form=ExtendedRegisterForm)
        mail.init_app(app)
        md = Markdown(app, extensions=['fenced_code', 'tables'])
        # migrate.init_app(app, db)
        # Add Flask-Admin views for Users and Roles
        admin.init_app(app)
        admin.add_view(UserAdmin(User, db.session))
        admin.add_view(RoleAdmin(Role, db.session))
        admin.add_view(PostAdmin(Post, db.session))
        
        
    def setUp(self):
        self.db_uri = 'mysql+pymysql://%s:%s@%s/' % (app.config['DB_USERNAME'], app.config['DB_PASSWORD'], app.config['DB_HOST'])
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['BLOG_DATABASE_NAME'] = 'test_expendable'
        app.config['SQLALCHEMY_DATABASE_URI'] = self.db_uri + app.config['BLOG_DATABASE_NAME']
        engine = sqlalchemy.create_engine(self.db_uri)
        conn = engine.connect()
        conn.execute("commit")
        conn.execute("create database "  + app.config['BLOG_DATABASE_NAME'])
        with app.app_context():
            db.create_all()
            conn.close()
            self.app = app.test_client()

    def tearDown(self):
        db.session.remove()
        engine = sqlalchemy.create_engine(self.db_uri)
        conn = engine.connect()
        conn.execute("commit")
        conn.execute("drop database "  + app.config['BLOG_DATABASE_NAME'])
        conn.close()

    def login(self, email, password):
        return self.app.post('/login', data={
            'email': email, 
            'password': password}, follow_redirects=True)

    def logout(self):
        return self.app.get('/logout', follow_redirects=True)

    def register_user(self, fullname, email, username, password, confirm):
        return self.app.post('/register', data=dict(
            fullname=fullname,
            email=email,
            username=username,
            password=password,
            confirm=confirm
            ),
        follow_redirects=True)

    def publish_post(self, title, body, category, new_category):
        return self.app.post('/post', data=dict(
            title=title,
            body=body,
            category=category,
            new_category=new_category,
            ),
        follow_redirects=True)

    # Notice that our test functions begin with the word test;
    # this allows unittest to automatically identify the method as a test to run.

    def test_login_logout(self):
        rv = self.login(private.STARTING_ADMIN1, private.STARTING_ADMIN_PASS)
        #print(rv)
        assert 'zz123' in str(rv.data)
    
    def test_admin_restriction(self):
        rv = self.app.get('/admin', follow_redirects=True)
        print(rv)
        assert '403' in str(rv.data)    


if __name__ == '__main__':
    unittest.main()