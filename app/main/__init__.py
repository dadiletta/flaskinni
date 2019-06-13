from flask import Blueprint

main = Blueprint('main', __name__)

from . import views, forms, decorators
# from models import Post, Tag
