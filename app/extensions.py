from flask_security import Security
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_migrate import Migrate
from flask_admin import Admin
from flask_ckeditor import CKEditor
from flask_moment import Moment
from flask_assets import Environment
from flask_jwt_extended import JWTManager

security = Security()
db = SQLAlchemy()
migrate = Migrate()
moment = Moment()
mail = Mail()
admin = Admin(template_mode='bootstrap4')
ckeditor = CKEditor()
assets = Environment()
jwt = JWTManager()