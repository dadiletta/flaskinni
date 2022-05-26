"""
Base Database Schema
=====================
These users are closely connected with the `Flask Security Too <https://flask-security-too.readthedocs.io/en/stable/quickstart.html#id4>`_. 
"""

import uuid
from .. import db
from flask import url_for
from flask_admin.contrib import sqla
from flask_security import UserMixin, RoleMixin, current_user, utils
from wtforms import PasswordField
from datetime import datetime
import humanize


def uuid_generator():
    return uuid.uuid4().hex

# Create a table to support a many-to-many relationship between Users and Roles
roles_users = db.Table(
    'roles_users',
    db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
    db.Column('role_id', db.Integer(), db.ForeignKey('role.id'))
)

# Role class
class Role(db.Model, RoleMixin):
    __tablename__ = 'role'
    # Our Role has three fields, ID, name and description
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

    # __str__ is required by Flask-Admin, so we can have human-readable values for the Role when editing a User.
    # If we were using Python 2.7, this would be __unicode__ instead.
    def __str__(self):
        return self.name

    # __hash__ is required to avoid the exception TypeError: unhashable type: 'Role' when saving a User
    def __hash__(self):
        return hash(self.name)


# User class
class User(db.Model, UserMixin):
    """
    Both the database schematic and the application object used to store user data and house functions
    """
    __tablename__ = 'user'

    # Our User has six fields: ID, email, password, active, confirmed_at and roles. The roles field represents a
    # many-to-many relationship using the roles_users table. Each user may have no role, one role, or multiple roles.
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(155))
    last_name = db.Column(db.String(155))
    phone = db.Column(db.String(20))
    """While there are many ways to store phone numbers, here a string is being used."""
    address = db.Column(db.Text)
    about = db.Column(db.Text)
    image = db.Column(db.String(125))
    """Name of file that's kept in the user's folder"""
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    fs_uniquifier = db.Column(db.String(255), unique=True, nullable=False, default=uuid_generator)
    """This property is required by Flask-Security-Too"""
    # TOGGLES
    active = db.Column(db.Boolean(), default=True)
    public_profile = db.Column(db.Boolean(), default=True)
    # DATES
    confirmed_at = db.Column(db.DateTime())
    last_seen = db.Column(db.DateTime(), default=None)
    """This property is automatically updated in the `before_request` function as defined in the app's `__init__.py` file."""
    posts = db.relationship('Post', backref='user', lazy='dynamic')
    
    roles = db.relationship(
        'Role',
        secondary=roles_users,
        backref=db.backref('users', lazy='dynamic')
    )
    
    # DUNDER METHOD
    def __repr__(self):
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        else:
            return super().__repr__()

    @property
    def img(self):
        """Builds a path for the saved image

        Returns:
            str: Local URL to the user's profile image
        """
        if self.image:
            return url_for('static', filename=f"uploads/{self.id}/{self.image}")
        else:
            return None

    @property
    def when_registered(self):
        """ Return the date in readable English """
        return humanize.naturaltime(self.confirmed_at) # we use Flask-Moment for template-based solution to the same issue

    def save_to_db(self):
        """ Utility update model to DB """
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_username(cls, username):
        """ Accessor method that works from a static context """
        return cls.query.filter_by(email=username).first()

    @staticmethod
    def generate_hash(password):
        """ Utility to help with API """
        return utils.encrypt_password(password)
    
    @staticmethod
    def verify_hash(password, hash) -> bool:
        """A static utility to match provided hash and checks it against the password

        Args:
            password (str): plain text password
            hash (str): encrypted password stored in user model

        Returns:
            bool: Returns `True` if the password matches the provided hash
        """
        return utils.verify_password(password, hash)    



class Buzz(db.Model):
    """
    This is the event log for the super admin panel 
    """
    id = db.Column(db.Integer, primary_key=True)
    # FK
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)  
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=True)  
    # props
    title = db.Column(db.String(120)) 
    body = db.Column(db.Text)  
    created_on = db.Column(db.DateTime(), default=datetime.utcnow)
    # RELATIONSHIPS
    user = db.relationship('User', backref='buzz') # the initiator of this event
    post = db.relationship('Post', backref='buzz') # in case this event had to do with a post

    def generate_link(self):
        """ 
        Since buzz objects are created for all sorts of reasons, this method generates a link to the most relevant source
        """
        if self.user_id: return url_for('base.profile', user_id=self.user_id)
        return "#"


####################
#####  FLASK-JWT-EXTENDED  
####################
class RevokedTokenModel(db.Model):
    """
    Originally taken from this `JWT guide <https://github.com/oleg-agapov/flask-jwt-auth/blob/master/step_5/models.py>`_.
    """
    __tablename__ = 'revoked_tokens'
    id = db.Column(db.Integer, primary_key = True)
    jti = db.Column(db.String(120))
    
    def add(self):
        db.session.add(self)
        db.session.commit()
    
    @classmethod
    def is_jti_blocklisted(cls, jti):
        query = cls.query.filter_by(jti = jti).first()
        return bool(query)


####################
#####  FLASK-ADMIN  
####################
# Customized User model for SQL-Admin
class UserAdmin(sqla.ModelView):

    #: Don't display the password on the list of Users
    column_exclude_list = ('password',)

    #: Don't include the standard password field when creating or editing a User (but see below)
    form_excluded_columns = ('password',)

    #: Automatically display human-readable names for the current and available Roles when creating or editing a User
    column_auto_select_related = True

    #: Prevent administration of Users unless the currently logged-in user has the "admin" role
    def is_accessible(self):
        return current_user.has_role('admin')

    # On the form for creating or editing a User, don't display a field corresponding to the model's password field.
    # There are two reasons for this. First, we want to encrypt the password before storing in the database. Second,
    # we want to use a password field (with the input masked) rather than a regular text field.
    def scaffold_form(self):

        # Start with the standard form as provided by Flask-Admin. We've already told Flask-Admin to exclude the
        # password field from this form.
        form_class = super(UserAdmin, self).scaffold_form()

        # Add a password field, naming it "password2" and labeling it "New Password".
        form_class.password2 = PasswordField('New Password')
        return form_class

    # This callback executes when the user saves changes to a newly-created or edited User -- before the changes are
    # committed to the database.
    def on_model_change(self, form, model, is_created):

        # If the password field isn't blank...
        if len(model.password2):

            # ... then encrypt the new password prior to storing it in the database. If the password field is blank,
            # the existing password in the database will be retained.
            model.password = utils.encrypt_password(model.password2)

        # https://stackoverflow.com/questions/70978807/with-flask-admin-tab-create-user-use-the-security-database-create-user-method-t
        if model.fs_uniquifier is None:
            model.fs_uniquifier = uuid.uuid4().hex

class BaseAdmin(sqla.ModelView):
    """ Basic display model for Flask-Admin """
    #: Prevent administration of Roles unless the currently logged-in user has the "admin" role
    def is_accessible(self):
        return current_user.has_role('admin')
        