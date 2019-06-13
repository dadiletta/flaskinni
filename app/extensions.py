from flask_security import Security
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_uploads import UploadSet, IMAGES
from flask_migrate import Migrate
from flask_admin import Admin
from flask_ckeditor import CKEditor

security = Security()
db = SQLAlchemy()
migrate = Migrate()
uploaded_images = UploadSet('images', IMAGES)
mail = Mail()
admin = Admin(template_mode='bootstrap3')
ckeditor = CKEditor()