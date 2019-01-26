from flask import Blueprint

route_wechat = Blueprint('wechat', __name__)

from web.wechat_controllers.wechat import *
from web.wechat_controllers.personaInformation import *

@route_wechat.route('/')
def index():
    return ''
