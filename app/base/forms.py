"""
Base Forms
================
The forms built by `WTForms <https://wtforms.readthedocs.io/en/>`_. 
"""
from flask_wtf import FlaskForm
from wtforms.fields import EmailField, TelField
from wtforms import validators, StringField, PasswordField, TextAreaField, SubmitField, BooleanField
from flask_wtf.file import FileField, FileAllowed
from ..models import Tag
from flask_security.forms import ConfirmRegisterForm

# This queues up all tags with no regard who made them
def tags():
    return Tag.query


class ExtendedRegisterForm(ConfirmRegisterForm):
    """ Expands upon the Flask-Security-Too registration form. """
    first_name = StringField('First Name', [validators.DataRequired()])
    last_name = StringField('Last Name', [validators.DataRequired()])
    email = EmailField('Email address', [validators.DataRequired(), validators.Email()])

    password = PasswordField('Password', [
            validators.DataRequired(),
            validators.Length(min=4, max=80)
        ])
        
    def validate(self):
        success = True
        if not super(ExtendedRegisterForm, self).validate():
            success = False
        return success
    

# We can make our own validators
def CheckNameLength(form, field):
  if len(field.data) < 4:
    raise validators.ValidationError('Name must have more then 3 characters')


class PostForm(FlaskForm):
    """ Blog post form """
    image = FileField('Image', validators=[
        FileAllowed(['jpg', 'png'], 'Images only!')
    ])
    title = StringField('Title', [
            validators.DataRequired(),
            validators.Length(max=80)])
    subtitle = StringField('Subtitle', [
            validators.DataRequired(),
            validators.Length(max=80)])        
    body = TextAreaField('Content', validators=[validators.DataRequired()])
    # tag = QuerySelectField('Tag', query_factory=tags, validators=[validators.DataRequired()])
    # new_tag = StringField('New Tag')


class ContactForm(FlaskForm):
    """ Optional contact form for the home page """
    name = StringField('Your Name:', [validators.DataRequired(), CheckNameLength])
    email = StringField('Your e-mail address:', [validators.DataRequired(), validators.Email('your@email.com')])
    message = TextAreaField('Your message:', [validators.DataRequired()])
    submit = SubmitField('Send Message')


class SettingsForm(FlaskForm):
    """ Modify a user's details and options """
    first_name = StringField('First name', [validators.DataRequired()])
    last_name = StringField('Last name', [validators.DataRequired()])
    about = TextAreaField('About me', [validators.Optional()])
    address = TextAreaField('Address', [validators.Optional()])
    phone = TelField('Phone', [validators.Optional()])
    # TODO: add file size validator
    image = FileField('Image', validators=[
        FileAllowed(['jpg', 'png'], 'Images only!')
    ])
    public_profile = BooleanField('Public profile')


class BuzzForm(FlaskForm):
    """ Simple form to create a buzz object """
    title = StringField('Title', [validators.DataRequired()])
    body = TextAreaField('Body', [validators.DataRequired()])