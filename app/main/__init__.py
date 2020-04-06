from flask import Blueprint

main = Blueprint('main', __name__)

from . import views, views_ajax, forms, decorators
