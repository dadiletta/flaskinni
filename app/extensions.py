from flask_security import Security
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_uploads import UploadSet, IMAGES
from flask_migrate import Migrate
from flask_admin import Admin
from flask_ckeditor import CKEditor
from flask_moment import Moment
from flask_assets import Environment
from flask_restful import Api
from flask_jwt_extended import JWTManager

security = Security()
db = SQLAlchemy()
migrate = Migrate()
moment = Moment()
uploaded_images = UploadSet('images', IMAGES)
mail = Mail()
admin = Admin(template_mode='bootstrap3')
ckeditor = CKEditor()
assets = Environment()
api = Api(prefix="api/v1")
jwt = JWTManager()