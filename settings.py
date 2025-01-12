"""
Settings File
===============
These files are not intended to be changed much. Instead, you should use a `.env` file as described in `the guide <https://gilmour.online/compsci/web-development/4-install-flaskinni#env-variables>`_. 
"""
import os
import datetime

SECRET_KEY = os.environ.get("SECRET_KEY", "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX") 
FLASK_DEBUG=os.environ.get("FLASK_DEBUG", False)

###################
##  FLASKINNI  
###################
ADMIN_EMAIL = os.environ.get("ADMIN_EMAIL", 'flaskinni@gmail.com')
STARTING_ADMINS = os.environ.get("STARTING_ADMINS", [])
STARTING_ADMIN_PASS = os.environ["STARTING_ADMIN_PASS"]
UPLOAD_EXTENSIONS = ['.jpg', '.png', '.gif']

###################
##  SQLALCHEMY
###################
POSTGRES = {
    'user': os.environ.get("DB_USERNAME", 'postgres'),
    'pw': os.environ.get("DB_PASSWORD", ""),  # Default to empty string
    'db': os.environ.get("DATABASE_NAME", 'postgres'),  # Default to 'postgres' for Supabase
    'host': os.environ.get("DB_HOST", 'localhost'),  # Default to localhost for development
    'port': os.environ.get("DB_PORT", '5432')
}
SQLALCHEMY_DATABASE_URI = os.environ.get(
    "DATABASE_URL",
    'postgresql://%(user)s:%(pw)s@%(host)s:%(port)s/%(db)s' % POSTGRES
)

SQLALCHEMY_TRACK_MODIFICATIONS = False
DEBUG_TB_INTERCEPT_REDIRECTS = False
SESSION_PROTECTION = 'strong'

###################
##  SECURITY
###################
# Session configuration
SESSION_PROTECTION = 'strong'
PERMANENT_SESSION_LIFETIME = datetime.timedelta(days=7)  # Session expiry time
SESSION_COOKIE_SECURE = True  # Only send cookies over HTTPS
SESSION_COOKIE_HTTPONLY = True  # Prevent JavaScript from accessing cookies
SESSION_COOKIE_SAMESITE = 'Lax'  # CSRF protection

# Password hashing (using Werkzeug's built-in functions)
PASSWORD_HASH_METHOD = 'pbkdf2:sha256:600000'  # Modern hashing with 600000 iterations
PASSWORD_SALT = os.environ["PASSWORD_SALT"]  # Salt for password hashing

# CSRF Protection
WTF_CSRF_ENABLED = True
WTF_CSRF_SECRET_KEY = os.environ.get("WTF_CSRF_SECRET_KEY", os.urandom(32))
WTF_CSRF_TIME_LIMIT = 3600  # CSRF token expiry in seconds

# Login configuration
LOGIN_DISABLED = False
LOGIN_VIEW = 'auth.login'  # Route for login page
LOGIN_MESSAGE = 'Please log in to access this page.'
LOGIN_MESSAGE_CATEGORY = 'info'

###################
##  FLASK-MAIL 
###################
# TODO: Setup something like Mailtrap for testing (https://mailtrap.io/) ...
# or Mailgun (https://www.mailgun.com/pricing/)
MAIL_SERVER = os.environ.get("MAIL_SERVER", 'sandbox.smtp.mailtrap.io')
MAIL_PORT = int(os.environ.get("MAIL_PORT", 2525))
MAIL_USE_SSL = False if os.environ.get("MAIL_USE_SSL", "False") == "False" else True
MAIL_USE_TLS = True if os.environ.get("MAIL_USE_TLS", "True") == "True" else False
MAIL_USERNAME = os.environ["MAIL_USERNAME"]
MAIL_PASSWORD = os.environ["MAIL_PASSWORD"]
MAIL_DEBUG = True if os.environ.get("MAIL_DEBUG", "True") == "True" else False
MAIL_DEFAULT_SENDER = os.environ["MAIL_DEFAULT_SENDER"]
