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

security = Security()
"""Flask-Security-Too"""
db = SQLAlchemy()
"""SQLAlchemy database connection"""
migrate = Migrate()
"""Flask-Migrate's alembic tracker to adjust with database changes"""
moment = Moment()
"""Flask-Moment's timezone and datetime humanizer """
mail = Mail()
"""Flask-Mail's SMTP mailer used with Flask-Security-Too"""
admin = Admin(template_mode='bootstrap4')
"""Flask-Admin set to use bootstrap4 """
jwt = JWTManager()
"""Flask-JWT-Extended's token manager"""