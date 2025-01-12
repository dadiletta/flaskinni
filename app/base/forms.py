"""
Base Forms
================
Forms built with WTForms for user authentication and content management.
"""
from flask_wtf import FlaskForm
from wtforms.fields import EmailField, TelField
from wtforms import validators, StringField, PasswordField, TextAreaField, \
    SubmitField, BooleanField
from wtforms_sqlalchemy.fields import QuerySelectMultipleField
from flask_wtf.file import FileField, FileAllowed
import sqlalchemy as sa
from ..extensions import db
from ..models import Tag, User

def tags():
    """Query factory for all available tags."""
    return Tag.query

class LoginForm(FlaskForm):
    """User login form."""
    username = StringField('Username', validators=[validators.DataRequired()])
    password = PasswordField('Password', validators=[validators.DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
    """User registration form with custom validation."""
    username = StringField('Username', validators=[validators.DataRequired()])
    first_name = StringField('First Name', validators=[validators.DataRequired()])
    last_name = StringField('Last Name', validators=[validators.DataRequired()])
    email = EmailField('Email', validators=[validators.DataRequired(), validators.Email()])
    password = PasswordField('Password', validators=[validators.DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[
            validators.DataRequired(),
            validators.EqualTo('password', message='Passwords must match')
        ])
    submit = SubmitField('Register')

    def validate_username(self, username):
        """Check username uniqueness."""
        user = db.session.scalar(
            sa.select(User).where(User.username == username.data))
        if user is not None:
            raise validators.ValidationError('Please use a different username.')

    def validate_email(self, email):
        """Check email uniqueness."""
        user = db.session.scalar(
            sa.select(User).where(User.email == email.data))
        if user is not None:
            raise validators.ValidationError('Please use a different email address.')

class PostForm(FlaskForm):
    """Blog post creation/editing form."""
    image = FileField('Image', validators=[
        FileAllowed(['jpg', 'png'], 'Images only!')
    ])
    title = StringField('Title', [
        validators.DataRequired(),
        validators.Length(max=80)
    ])
    subtitle = StringField('Subtitle', [
        validators.DataRequired(),
        validators.Length(max=80)
    ])        
    body = TextAreaField('Content', validators=[validators.DataRequired()])
    tags = QuerySelectMultipleField('Tag', 
                                  query_factory=tags, 
                                  validators=[validators.DataRequired()])
    new_tag = StringField('New Tag')

class ContactForm(FlaskForm):
    """Contact form with custom name length validation."""
    def check_name_length(form, field):
        if len(field.data) < 4:
            raise validators.ValidationError('Name must have more than 3 characters')

    name = StringField('Your Name:', [validators.DataRequired(), check_name_length])
    email = StringField('Your e-mail address:', [
        validators.DataRequired(), 
        validators.Email('Please enter a valid email address')
    ])
    message = TextAreaField('Your message:', [validators.DataRequired()])
    submit = SubmitField('Send Message')

class SettingsForm(FlaskForm):
    """User settings form."""
    first_name = StringField('First name', [validators.DataRequired()])
    last_name = StringField('Last name', [validators.DataRequired()])
    about = TextAreaField('About me', [validators.Optional()])
    address = TextAreaField('Address', [validators.Optional()])
    phone = TelField('Phone', [validators.Optional()])
    image = FileField('Image', validators=[
        FileAllowed(['jpg', 'png'], 'Images only!')
    ])
    public_profile = BooleanField('Public profile')

class BuzzForm(FlaskForm):
    """Simple form for creating buzz objects."""
    title = StringField('Title', [validators.DataRequired()])
    body = TextAreaField('Body', [validators.DataRequired()])