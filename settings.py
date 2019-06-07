import os
import private

SECRET_KEY = private.SECRET_KEY

DEBUG=private.DEBUG
POSTGRES = {
    'user': private.DB_USERNAME,
    'pw': private.DB_PASSWORD,
    'db': private.DATABASE_NAME,
    'host': os.environ.get("DB_HOST", os.getenv('IP', '0.0.0.0')),
    'port': os.environ.get("DB_PORT", '5432')
}
SQLALCHEMY_DATABASE_URI = 'postgresql://%(user)s:\
%(pw)s@%(host)s:%(port)s/%(db)s' % POSTGRES

SQLALCHEMY_TRACK_MODIFICATIONS = os.environ.get("SQLALCHEMY_TRACK_MODIFICATIONS", True)
UPLOADED_IMAGES_DEST = private.UPLOADED_IMAGES_DEST
UPLOADED_IMAGES_URL = private.UPLOADED_IMAGES_URL

DEBUG_TB_INTERCEPT_REDIRECTS = False
SESSION_PROTECTION = 'strong'
# activate flask elements
SECURITY_REGISTERABLE = os.environ.get("SECURITY_REGISTERABLE", True)
SECURITY_CONFIRMABLE = os.environ.get("SECURITY_CONFIRMABLE", True)
SECURITY_RECOVERABLE = os.environ.get("SECURITY_RECOVERABLE", True)
SECURITY_PASSWORD_HASH = private.SECURITY_PASSWORD_HASH
SECURITY_PASSWORD_SALT = private.SECURITY_PASSWORD_SALT
SECURITY_POST_LOGIN_VIEW = '/'   # controls what page you see after login
SECURITY_EMAIL_SENDER = private.ADMIN_EMAIL # fixes error https://github.com/mattupstate/flask-security/issues/685

MAIL_SERVER = private.MAIL_SERVER
MAIL_PORT = private.MAIL_PORT
MAIL_USE_SSL = private.MAIL_USE_SSL
MAIL_USE_TLS = private.MAIL_USE_TLS
MAIL_USERNAME = private.MAIL_USERNAME
MAIL_PASSWORD = private.MAIL_PASSWORD
MAIL_DEBUG = private.DEBUG
MAIL_DEFAULT_SENDER = private.ADMIN_EMAIL

'''
# Google Cloud Project ID. This can be found on the 'Overview' page at
# https://console.developers.google.com
PROJECT_ID = private.GOOGLE_PROJECT_ID

# OAuth2 configuration.
# This can be generated from the Google Developers Console at
# https://console.developers.google.com/project/_/apiui/credential.
# Note that you will need to add all URLs that your application uses as
# authorized redirect URIs. For example, typically you would add the following:
#
#  * http://localhost:8080/oauth2callback
#  * https://<your-app-id>.appspot.com/oauth2callback.
#
# If you receive a invalid redirect URI error review you settings to ensure
# that the current URI is allowed.
GOOGLE_OAUTH2_CLIENT_ID = \
    private.GOOGLE_OAUTH2_CLIENT_ID
GOOGLE_OAUTH2_CLIENT_SECRET = private.GOOGLE_OAUTH2_CLIENT_SECRET
'''