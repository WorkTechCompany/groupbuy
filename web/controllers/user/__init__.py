from flask import Blueprint

route_user = Blueprint("user_page", __name__)

from web.controllers.user.user import *


@route_user.route('/')
def index():
    return ''