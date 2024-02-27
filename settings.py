"""
Settings File
===============
These files are not intended to be changed much. Instead, you should use a `.env` file as described in `the guide <https://gilmour.online/compsci/web-development/4-install-flaskinni#env-variables>`_. 
"""

import os
from dotenv import load_dotenv # connect me with any .env files

#: Pulls in `environmental variables <https://github.com/theskumar/python-dotenv>`_. 
dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

# TODO: Setup your own .env file
# https://gilmour.online/compsci/web-development/4-install-flaskinni#env-variables

###################
##  FLASK 
###################
SECRET_KEY = os.environ.get("SECRET_KEY", "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX") 
DEBUG=bool(os.environ.get("DEBUG", True))

###################
##  FLASKINNI  
###################
ADMIN_EMAIL = os.environ.get("ADMIN_EMAIL", 'flaskinni@gmail.com')
STARTING_ADMINS = os.environ.get("STARTING_ADMINS", [ADMIN_EMAIL])
STARTING_ADMIN_PASS = os.environ.get("STARTING_ADMIN_PASS", 'flaskinni123')
UPLOAD_EXTENSIONS = os.environ.get("UPLOAD_EXTENSIONS", ['.jpg', '.png', '.gif'])

###################
##  SQLALCHEMY
###################
# TODO: Setup your database
# https://www.digitalocean.com/community/tutorials/how-to-use-a-postgresql-database-in-a-flask-application#step-1-creating-the-postgresql-database-and-user
# https://www.codementor.io/@engineerapart/getting-started-with-postgresql-on-mac-osx-are8jcopb
POSTGRES = {
    'user': os.environ.get("DB_USERNAME", 'postgres'), 
    'pw': os.environ.get("DB_PASSWORD", 'postgres'),
    'db': os.environ.get("DATABASE_NAME", 'db'),
    'host': os.environ.get("DB_HOST", '0.0.0.0'),
    'port': os.environ.get("DB_PORT", '5432')
}
SQLALCHEMY_DATABASE_URI = 'postgresql://%(user)s:\
%(pw)s@%(host)s:%(port)s/%(db)s' % POSTGRES

SQLALCHEMY_TRACK_MODIFICATIONS = os.environ.get("SQLALCHEMY_TRACK_MODIFICATIONS", False)
DEBUG_TB_INTERCEPT_REDIRECTS = False
SESSION_PROTECTION = 'strong'

###################
##  FLASK-SECURITY-TOO
###################
SECURITY_REGISTERABLE = bool(os.environ.get("SECURITY_REGISTERABLE", True))
SECURITY_CONFIRMABLE = bool(os.environ.get("SECURITY_CONFIRMABLE", True))
SECURITY_RECOVERABLE = bool(os.environ.get("SECURITY_RECOVERABLE", True))
SECURITY_PASSWORD_HASH = os.environ.get("SECURITY_PASSWORD_HASH", "pbkdf2_sha512")
SECURITY_PASSWORD_SALT = os.environ.get("SECURITY_PASSWORD_SALT", "XXXXXXXXXXXXX") 
SECURITY_POST_LOGIN_VIEW = '/'   # controls what page you see after login
SECURITY_EMAIL_SENDER = os.environ.get("MAIL_DEFAULT_SENDER", 'flaskinni@flaskinni.org')# fixes error https://github.com/mattupstate/flask-security/issues/685

###################
##  FLASK-MAIL 
###################
# TODO: Setup something like Mailtrap for testing (https://mailtrap.io/) ...
# or Mailgun (https://www.mailgun.com/pricing/)
MAIL_SERVER = os.environ.get("MAIL_SERVER", 'sandbox.smtp.mailtrap.io')
MAIL_PORT = int(os.environ.get("MAIL_PORT", 2525))
MAIL_USE_SSL = bool(os.environ.get("MAIL_USE_SSL", False))
MAIL_USE_TLS = bool(os.environ.get("MAIL_USE_TLS", True))
MAIL_USERNAME = os.environ.get("MAIL_USERNAME", 'Unknown')
MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD", 'Unknown')
MAIL_DEBUG = bool(os.environ.get("MAIL_DEBUG", True))
MAIL_DEFAULT_SENDER = os.environ.get("MAIL_DEFAULT_SENDER", 'flaskinni@gmail.com')

###################
##  FLASK-RESTFUL / JWT
###################
PROPAGATE_EXCEPTIONS = bool(os.environ.get("PROPAGATE_EXCEPTIONS", True))
JWT_BLOCKLIST_TOKEN_CHECKS = os.environ.get("JWT_BLOCKLIST_TOKEN_CHECKS", ['access', 'refresh']) 
