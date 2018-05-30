from wtforms import validators, StringField, PasswordField
from wtforms.fields.html5 import EmailField
from flask_security.forms import RegisterForm, ConfirmRegisterForm
from extensions import db

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
