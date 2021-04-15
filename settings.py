import os

###################
##  FLASK 
###################
SECRET_KEY = os.environ.get("SECRET_KEY", "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX") 
DEBUG=os.environ.get("DEBUG", True) 

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
POSTGRES = {
    'user': os.environ.get("DB_USERNAME", 'postgres'), 
    'pw': os.environ.get("DB_PASSWORD", 'postgres'),
    'db': os.environ.get("DATABASE_NAME", 'db'),
    'host': os.environ.get("DB_HOST", '0.0.0.0'),
    'port': os.environ.get("DB_PORT", '5432')
}
SQLALCHEMY_DATABASE_URI = 'postgresql://%(user)s:\
%(pw)s@%(host)s:%(port)s/%(db)s' % POSTGRES

SQLALCHEMY_TRACK_MODIFICATIONS = os.environ.get("SQLALCHEMY_TRACK_MODIFICATIONS", True)
DEBUG_TB_INTERCEPT_REDIRECTS = False
SESSION_PROTECTION = 'strong'

###################
##  JWT 
###################
PROPAGATE_EXCEPTIONS = os.environ.get("PROPAGATE_EXCEPTIONS", True)
JWT_BLOCKLIST_TOKEN_CHECKS = os.environ.get("JWT_BLOCKLIST_TOKEN_CHECKS", ['access', 'refresh'])

###################
##  FLASK-SECURITY 
###################
SECURITY_REGISTERABLE = os.environ.get("SECURITY_REGISTERABLE", True)
SECURITY_CONFIRMABLE = os.environ.get("SECURITY_CONFIRMABLE", True)
SECURITY_RECOVERABLE = os.environ.get("SECURITY_RECOVERABLE", True)  
SECURITY_PASSWORD_HASH = os.environ.get("SECURITY_PASSWORD_HASH", "pbkdf2_sha512")
SECURITY_PASSWORD_SALT = os.environ.get("SECURITY_PASSWORD_HASH", "XXXXXXXXXXXXX") 
SECURITY_POST_LOGIN_VIEW = '/'   # controls what page you see after login
SECURITY_EMAIL_SENDER = os.environ.get("MAIL_DEFAULT_SENDER", 'flaskinni@flaskinni.org')# fixes error https://github.com/mattupstate/flask-security/issues/685

###################
##  FLASK-MAIL 
###################
MAIL_SERVER = os.environ.get("MAIL_SERVER", 'smtp.gmail.com')
MAIL_PORT = os.environ.get("MAIL_PORT", 465)
MAIL_USE_SSL = os.environ.get("MAIL_USE_SSL", True)
MAIL_USE_TLS = os.environ.get("MAIL_USE_TLS", False)
MAIL_USERNAME = os.environ.get("MAIL_USERNAME", 'flaskinni@gmail.com')
MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD", 'xxxxxxxxxxx')
MAIL_DEBUG = os.environ.get("MAIL_DEBUG", True)
MAIL_DEFAULT_SENDER = os.environ.get("MAIL_DEFAULT_SENDER", 'flaskinni@gmail.com')

###################
##  FLASK-RESTFUL / JWT
###################
PROPAGATE_EXCEPTIONS = os.environ.get("JWT_BLACKLIST_ENABLED", True) 
JWT_BLOCKLIST_TOKEN_CHECKS = os.environ.get("JWT_BLOCKLIST_TOKEN_CHECKS", ['access', 'refresh']) 
