"""
Extensions Container
=====================
To avoid circular import errors, we have this handy module to instantiate and contain our extensions. 
"""
from flask_security import Security
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_migrate import Migrate
from flask_admin import Admin
from flask_moment import Moment
from flask_jwt_extended import JWTManager

#: Flask-Security-Too
security = Security()
#: SQLAlchemy database connection
db = SQLAlchemy()
#: Flask-Migrate's alembic tracker to adjust with database changes
migrate = Migrate()
#: Flask-Moment's timezone and datetime humanizer 
moment = Moment()
#: Flask-Mail's SMTP mailer used with Flask-Security-Too
mail = Mail()
#: Flask-Admin set to use bootstrap4 
admin = Admin(template_mode='bootstrap4')
#: Flask-JWT-Extended's token manager
jwt = JWTManager()