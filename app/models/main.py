from .. import db, uploaded_images
from flask import flash
from flask_admin.contrib import sqla
from flask_security import UserMixin, RoleMixin, current_user, utils
from wtforms import validators, StringField, PasswordField
from datetime import datetime
import humanize


# Create a table to support a many-to-many relationship between Users and Roles
roles_users = db.Table(
    'roles_users',
    db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
    db.Column('role_id', db.Integer(), db.ForeignKey('role.id'))
)

# Role class
class Role(db.Model, RoleMixin):

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

    # Our User has six fields: ID, email, password, active, confirmed_at and roles. The roles field represents a
    # many-to-many relationship using the roles_users table. Each user may have no role, one role, or multiple roles.
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(155))
    last_name = db.Column(db.String(155))
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean())
    confirmed_at = db.Column(db.DateTime())
    posts = db.relationship('Post', backref='user', lazy='dynamic')
    
    roles = db.relationship(
        'Role',
        secondary=roles_users,
        backref=db.backref('users', lazy='dynamic')
    )
    
    # return the date in readable English    
    @property
    def when_registered(self):
        return humanize.naturaltime(self.confirmed_at)

# Customized User model for SQL-Admin
class UserAdmin(sqla.ModelView):

    # Don't display the password on the list of Users
    column_exclude_list = ('password',)

    # Don't include the standard password field when creating or editing a User (but see below)
    form_excluded_columns = ('password',)

    # Automatically display human-readable names for the current and available Roles when creating or editing a User
    column_auto_select_related = True

    # Prevent administration of Users unless the currently logged-in user has the "admin" role
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


# Customized Role model for SQL-Admin
class RoleAdmin(sqla.ModelView):

    # Prevent administration of Roles unless the currently logged-in user has the "admin" role
    def is_accessible(self):
        return current_user.has_role('admin')
        
# Customized Role model for SQL-Admin
class PostAdmin(sqla.ModelView):

    # Prevent administration of Roles unless the currently logged-in user has the "admin" role
    def is_accessible(self):
        return current_user.has_role('admin')

    
##################
##### BLOG  ######

# Create a table to support a many-to-many relationship between Users and Roles
tags_posts = db.Table(
    'tags_posts',
    db.Column('post_id', db.Integer(), db.ForeignKey('post.id')),
    db.Column('tag_id', db.Integer(), db.ForeignKey('tag.id'))
)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    title = db.Column(db.String(80))
    subtitle = db.Column(db.String(80))
    body = db.Column(db.Text)
    image = db.Column(db.String(125))
    slug = db.Column(db.String(125), unique=True)
    publish_date = db.Column(db.DateTime)
    live = db.Column(db.Boolean)
    tags = db.relationship(
        'Tag',
        secondary=tags_posts,
        backref=db.backref('posts', lazy='dynamic')
    )

    # get the whole image path
    @property
    def imgsrc(self):
        if self.image:
            return uploaded_images.url(self.image)
        else:
            return None
    
    # return the date in readable English    
    @property
    def pubdate(self):
        return humanize.naturaltime(self.publish_date)

    def __init__(self, user, title, subtitle, body, slug, image=None, publish_date=None, live=True):
            self.user_id = user.id
            self.title = title
            self.subtitle = subtitle
            self.body = body
            self.image = image
            self.slug = slug
            if publish_date is None:
                self.publish_date = datetime.utcnow()
            self.live = live

    def __repr__(self):
        return '<Post %r>' % self.title


class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))

    def __init__(self, name, user_id=None):
        self.name = name
        self.user_id = user_id

    def __repr__(self):
        return self.name