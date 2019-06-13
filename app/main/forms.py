from flask_wtf import FlaskForm
from wtforms.fields.html5 import EmailField
from wtforms import validators, StringField, PasswordField, TextAreaField, SubmitField
from flask_wtf.file import FileField, FileAllowed
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from flask_ckeditor import CKEditorField
from .models import Tag
from flask_security.forms import RegisterForm, ConfirmRegisterForm
from .. import db

# This queues up all tags with no regard who made them
def tags():
    return Tag.query


class ExtendedRegisterForm(ConfirmRegisterForm):
    first_name = StringField('First Name', [validators.Required()])
    last_name = StringField('Last Name', [validators.Required()])
    email = EmailField('Email address', [validators.DataRequired(), validators.Email()])

    password = PasswordField('Password', [
            validators.Required(),
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
    image = FileField('Image', validators=[
        FileAllowed(['jpg', 'png'], 'Images only!')
    ])
    title = StringField('Title', [
            validators.Required(),
            validators.Length(max=80)])
    subtitle = StringField('Subtitle', [
            validators.Required(),
            validators.Length(max=80)])        
    body = CKEditorField('Content', validators=[validators.Required()])
    # tag = QuerySelectField('Tag', query_factory=tags, validators=[validators.Required()])
    # new_tag = StringField('New Tag')
    
class ContactForm(FlaskForm):
    name = StringField('Your Name:', [validators.DataRequired(), CheckNameLength])
    email = StringField('Your e-mail address:', [validators.DataRequired(), validators.Email('your@email.com')])
    message = TextAreaField('Your message:', [validators.DataRequired()])
    submit = SubmitField('Send Message')